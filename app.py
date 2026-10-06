import os
from datetime import date
from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine, text

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL", "").strip()
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set. Add the Render PostgreSQL Internal Database URL as DATABASE_URL.")

engine = create_engine(DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1), pool_pre_ping=True)

def init_db():
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS reports (
                id BIGSERIAL PRIMARY KEY,
                work_date DATE NOT NULL,
                weather VARCHAR(20),
                company VARCHAR(200),
                work_content TEXT,
                people INTEGER,
                note TEXT,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
        """))

init_db()

@app.get("/")
def index():
    return render_template("index.html", today=date.today().isoformat())

@app.post("/submit")
def submit():
    people_raw = request.form.get("people", "").strip()
    people = int(people_raw) if people_raw else None

    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO reports
            (work_date, weather, company, work_content, people, note)
            VALUES
            (:work_date, :weather, :company, :work_content, :people, :note)
        """), {
            "work_date": request.form.get("work_date"),
            "weather": request.form.get("weather", ""),
            "company": request.form.get("company", ""),
            "work_content": request.form.get("work", ""),
            "people": people,
            "note": request.form.get("note", "")
        })
    return redirect(url_for("done"))

@app.get("/done")
def done():
    return render_template("done.html")

@app.get("/reports")
def reports():
    with engine.connect() as conn:
        rows = conn.execute(text("""
            SELECT id, work_date, weather, company, work_content, people, note, created_at
            FROM reports
            ORDER BY work_date DESC, id DESC
            LIMIT 500
        """)).mappings().all()
    return render_template("reports.html", reports=rows)

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    app.run(host="0.0.0.0", port=port, debug=False)
