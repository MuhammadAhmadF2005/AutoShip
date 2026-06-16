# AutoShip: Viva Documentation

This document provides a comprehensive explanation of the **AutoShip** project, covering its architecture, technology stack, and step-by-step logic from code submission to analysis results.

---

## 1. Project Overview
**AutoShip** is a full-stack web application designed to help developers ensure their Python code meets quality and complexity standards. It provides an IDE-like interface (using Monaco Editor) where users can write or paste code, run automated checks (Pylint and Radon), and track their progress over time through a persistent dashboard.

---

## 2. Technology Stack
The project is built using modern web and backend technologies:
- **Backend Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python)
- **Database/ORM**: [SQLite](https://www.sqlite.org/) with [SQLAlchemy](https://www.sqlalchemy.org/)
- **Templating**: [Jinja2](https://jinja.palletsprojects.com/)
- **Code Analysis Tools**:
    - **[Pylint](https://pylint.readthedocs.io/)**: For static code analysis and PEP 8 compliance.
    - **[Radon](https://radon.readthedocs.io/)**: For calculating Cyclomatic Complexity (CC).
- **Frontend Editor**: [Monaco Editor](https://microsoft.github.io/monaco-editor/) (the engine behind VS Code)
- **UI/UX**: Custom CSS with Dark/Light mode support and GSAP-inspired animations.
- **Deployment**: [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/).

---

## 3. Project Structure
The repository is organized into several key modules:

- **`app/main.py`**: The heart of the application. It contains the FastAPI routes, the logic for running external analysis tools, and template rendering.
- **`app/models.py`**: Defines the `AnalysisResult` database model for storing history.
- **`app/database.py`**: Handles the SQLAlchemy connection and session management.
- **`app/templates/`**: HTML files for the Dashboard, Analysis page, History, and Results.
- **`app/static/`**: Global CSS styles and frontend assets.
- **`Dockerfile` & `docker-compose.yml`**: Configuration for containerizing the application.

---

## 4. Execution Flow (Start to Finish)

### Phase 1: User Input
1.  **Landing Page**: The user visits the dashboard (`/`), which fetches statistics (total analyses, pass rate, average scores) from the SQLite database.
2.  **Code Submission**: On the `/analyze` page, the user writes Python code in the **Monaco Editor**. This editor provides syntax highlighting and a professional coding experience.
3.  **Form Options**: The user can toggle Pylint, Radon complexity analysis, and choose whether to save the result to their history.

### Phase 2: Processing (Backend)
1.  **Trigger**: When "Run Analysis" is clicked, the code is sent via a POST request to the `/analyze` endpoint.
2.  **Temporary Storage**: The backend receives the code, normalizes line endings, and writes it to a **temporary `.py` file** using Python's `tempfile` module.
3.  **Subprocess Execution**:
    -   **Pylint**: The app runs `subprocess.run([sys.executable, "-m", "pylint", ...])`. It parses the output string using regex to extract the score (e.g., `8.5/10`) and individual linting issues.
    -   **Radon**: The app runs `radon cc -a`. It parses the output to identify the complexity grade (A to F) for each function/class.
4.  **Score Calculation**: The system determines if the code "Passes" based on a user-defined threshold (default 7.0) and whether the complexity grade is acceptable (A, B, or C).

### Phase 3: Persistence & Display
1.  **Database Storage**: If "Save to history" was checked, a new `AnalysisResult` record is created in `autoship.local.db`.
2.  **Result Rendering**: The backend renders the `results.html` template, passing the scores, raw issue lists, and pass/fail status.
3.  **History Tracking**: Users can visit `/history` to see a table of all previous runs, allowing them to track their code quality trends.

---

## 5. Key Features & Design
-   **Theme Switcher**: A dynamic Dark/Light mode that syncs with the Monaco Editor's theme (`vs` vs `monokai`).
-   **Interactive Progress**: When analyzing, a simulated progress tracker keeps the user engaged while subprocesses run in the background.
-   **Responsive Layout**: A modern sidebar-based navigation that works across different screen sizes.
-   **SEO Optimized**: Includes proper semantic HTML and meta tags for better discoverability.

---

## 6. How to Run
1.  **Local Development**:
    ```bash
    pip install -r requirements.txt
    python -m uvicorn app.main:app --reload
    ```
2.  **Docker**:
    ```bash
    docker-compose up --build
    ```
    The application will be available at `http://localhost:8000`.

---
*Created for the AutoShip Project Viva.*
