import os
import tempfile
import subprocess
import re
import sys
from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.database import engine, Base, get_db
from app.models import AnalysisResult

# Create all tables (in a real app, use Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AutoShip", version="1.0.0")

# Setup templates and static files correctly with absolute / relative path fallback
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"request": request, "active_page": "dashboard"})

@app.post("/analyze", response_class=HTMLResponse)
def analyze(request: Request, code: str = Form(...), db: Session = Depends(get_db)):
    # 1. Write user code to a temporary file
    with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode="w", encoding="utf-8") as tf:
        tf.write(code)
        temp_path = tf.name

    pylint_score = 0.0
    lint_issues = []
    cc_issues = []
    max_cc_grade = "A"

    try:
        # 2. Run pylint
        # Using subprocess.run. Pylint often returns non-zero exit code if issues are found, so check=False
        pylint_proc = subprocess.run(
            [sys.executable, "-m", "pylint", "--disable=C0114,C0116,C0103", temp_path],
            capture_output=True,
            text=True
        )
        pylint_output = pylint_proc.stdout
        
        # Parse output
        for line in pylint_output.split("\n"):
            line = line.strip()
            if not line or line.startswith("-------------"):
                continue
            if line.startswith("Your code has been rated at"):
                # matches "Your code has been rated at X.XX/10..."
                match = re.search(r"rated at ([-+]?\d*\.\d+|\d+)/10", line)
                if match:
                    pylint_score = float(match.group(1))
            elif line.startswith(temp_path):
                # Clean up the output to not show the temp path
                issue_cleaned = line.replace(temp_path, "code.py", 1)
                lint_issues.append(issue_cleaned)
            elif line.startswith("*"):
                pass
            else:
                lint_issues.append(line)
        
        if pylint_score < 0:
            pylint_score = 0.0

        # 3. Run radon cc (cyclomatic complexity)
        # Output format: filename
        #     F 11:0 function_name - A
        radon_proc = subprocess.run(
            [sys.executable, "-m", "radon", "cc", "-a", temp_path],
            capture_output=True,
            text=True
        )
        radon_output = radon_proc.stdout

        grades = []
        for line in radon_output.split("\n"):
            line = line.strip()
            if not line or line == temp_path:
                continue
            
            # Simple parse for lines like "F 3:0 hello_world - A" or "10 blocks (classes, functions, methods) analyzed."
            if " - " in line:
                parts = line.split(" - ")
                if len(parts) >= 2:
                    grade = parts[-1].strip()
                    grades.append(grade)
            
            cc_issues.append(line)

        # Sort grades mapping A=1, B=2, C=3... F=6
        grade_order = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6}
        if grades:
            # max() by default sorts lexicographically, A < B, but we want the 'worst' grade -> highest letter
            max_cc_grade = max(grades, key=lambda g: grade_order.get(g, 0))

    finally:
        # Clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)

    # 4. Calculate Pass/Fail
    # Rule based on user approval: Pass if pylint_score >= 7.0 and Max CC Grade in 'A', 'B', 'C'
    is_pass = False
    if pylint_score >= 7.0 and max_cc_grade in ["A", "B", "C"]:
        is_pass = True

    # 5. Save to database
    snip = code[:300]
    db_result = AnalysisResult(
        code_snippet=snip,
        pylint_score=pylint_score,
        complexity_rating=max_cc_grade,
        is_pass=is_pass
    )
    db.add(db_result)
    db.commit()
    db.refresh(db_result)

    # 6. Render results
    return templates.TemplateResponse(request=request, name="results.html", context={
        "request": request, 
        "result": db_result,
        "lint_issues": [li for li in lint_issues if "rated at" not in li],
        "cc_issues": cc_issues
    })


@app.get("/history", response_class=HTMLResponse)
def history(request: Request, db: Session = Depends(get_db)):
    results = db.query(AnalysisResult).order_by(desc(AnalysisResult.timestamp)).all()
    return templates.TemplateResponse(request=request, name="history.html", context={"request": request, "results": results})
