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
from sqlalchemy import desc, func
from datetime import datetime, date

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
def root(request: Request, db: Session = Depends(get_db)):
    # Calculate stats
    total_analyses = db.query(AnalysisResult).count()
    
    avg_score = db.query(func.avg(AnalysisResult.pylint_score)).scalar() or 0.0
    
    pass_count = db.query(AnalysisResult).filter(AnalysisResult.is_pass == True).count()
    pass_rate = (pass_count / total_analyses * 100) if total_analyses > 0 else 0.0
    
    today = date.today()
    today_analyses = db.query(AnalysisResult).filter(
        func.date(AnalysisResult.timestamp) == today
    ).count()
    
    recent_analyses = db.query(AnalysisResult).order_by(desc(AnalysisResult.timestamp)).limit(5).all()
    
    # Last 10 scores for trend chart, ordered chronologically (oldest to newest)
    last_10 = db.query(AnalysisResult).order_by(desc(AnalysisResult.timestamp)).limit(10).all()
    trend_data = [{"score": r.pylint_score, "id": r.id} for r in reversed(last_10)]
    
    context = {
        "request": request, 
        "active_page": "dashboard",
        "total": total_analyses,
        "avg_score": avg_score,
        "pass_rate": pass_rate,
        "today_count": today_analyses,
        "recent": recent_analyses,
        "trend_data": trend_data
    }
    return templates.TemplateResponse(request=request, name="index.html", context=context)

@app.get("/analyze", response_class=HTMLResponse)
def analyze_page(request: Request):
    return templates.TemplateResponse(request=request, name="analyze.html", context={"request": request, "active_page": "analyze"})

@app.post("/analyze", response_class=HTMLResponse)
def analyze(
    request: Request, 
    code: str = Form(...),
    run_pylint: bool = Form(False),
    run_radon: bool = Form(False),
    save_history: bool = Form(False),
    pass_threshold: float = Form(7.0),
    db: Session = Depends(get_db)
):
    # 1. Write user code to a temporary file, normalizing line endings
    code = code.replace('\r\n', '\n').replace('\r', '\n')
    if not code.endswith('\n'):
        code += '\n'
    with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode="w", encoding="utf-8", newline='') as tf:
        tf.write(code)
        temp_path = tf.name

    pylint_score = 0.0
    lint_issues = []
    cc_issues = []
    max_cc_grade = "A"

    try:
        # 2. Run pylint
        if run_pylint:
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
                    match = re.search(r"rated at ([-+]?\d*\.\d+|\d+)/10", line)
                    if match:
                        pylint_score = float(match.group(1))
                elif line.startswith(temp_path):
                    issue_cleaned = line.replace(temp_path, "code.py", 1)
                    lint_issues.append(issue_cleaned)
                elif line.startswith("*"):
                    pass
                else:
                    lint_issues.append(line)
            
            if pylint_score < 0:
                pylint_score = 0.0
        else:
            pylint_score = 10.0

        # 3. Run radon cc (cyclomatic complexity)
        if run_radon:
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
                
                if " - " in line:
                    parts = line.split(" - ")
                    if len(parts) >= 2:
                        grade = parts[-1].strip()
                        grades.append(grade)
                
                cc_issues.append(line)

            grade_order = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6}
            if grades:
                max_cc_grade = max(grades, key=lambda g: grade_order.get(g, 0))
        else:
            max_cc_grade = "A"

    finally:
        # Clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)

    # 4. Calculate Pass/Fail
    is_pass = False
    if pylint_score >= pass_threshold and max_cc_grade in ["A", "B", "C"]:
        is_pass = True

    # 5. Save to database
    db_result = None
    if save_history:
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

    lines_analyzed = len(code.split('\n'))
    
    # Render results. Pass a mock ID if not saved.
    mock_timestamp = datetime.utcnow()
    result_data = {
        "id": db_result.id if db_result else "Unsaved",
        "timestamp": db_result.timestamp if db_result else mock_timestamp,
        "pylint_score": pylint_score,
        "complexity_rating": max_cc_grade,
        "is_pass": is_pass
    }

    return templates.TemplateResponse(request=request, name="results.html", context={
        "request": request, 
        "result": result_data,
        "lint_issues": [li for li in lint_issues if "rated at" not in li],
        "cc_issues": cc_issues,
        "lines_analyzed": lines_analyzed,
        "run_pylint": run_pylint,
        "run_radon": run_radon
    })


@app.get("/history", response_class=HTMLResponse)
def history(request: Request, db: Session = Depends(get_db)):
    results = db.query(AnalysisResult).order_by(desc(AnalysisResult.timestamp)).all()
    return templates.TemplateResponse(request=request, name="history.html", context={"request": request, "results": results})
