from sqlite3 import Connection
import sqlite3
import json

from models import Report, Perspective, Source

def get_db() -> Connection:
    return sqlite3.connect("reports.db")

def init_db():
    conn = get_db()

    conn.execute(""" 
        CREATE TABLE IF NOT EXISTS reports(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            goal TEXT,
            perspectives TEXT,
            conclusion TEXT,
            sources TEXT
        )
    """)
    conn.commit()

def save_report(report: Report) -> int:
    conn = get_db()
    goal = report.goal
    conclusion = report.conclusion
    perspectives = json.dumps([p.model_dump() for p in report.perspectives])
    sources = json.dumps([s.model_dump() for s in report.sources])

    cursor = conn.execute("""
        INSERT INTO reports (goal, perspectives, conclusion, sources)
        VALUES (?, ?, ?, ?)
    """, (goal, perspectives, conclusion, sources,))
    conn.commit()

    return cursor.lastrowid


def get_reports() -> list[Report]:
    conn = get_db()
    cursor = conn.execute("""
        SELECT * 
        FROM reports
    """)
    
    results = cursor.fetchall()
    reports = []
    for report in results:
        id, goal, perspectives, conclusion, sources = report
        perspectives = [Perspective(**p) for p in json.loads(perspectives)]
        sources = [Source(**s) for s in json.loads(sources)]
        reports.append(
            Report(
                goal=goal,
                perspectives=perspectives,
                conclusion=conclusion,
                sources=sources
            )
        )
    return reports


def get_report(report_id: int):
    pass