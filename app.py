from fastapi import FastAPI

from models import RequestResearch
from agent import run
from store import init_db, save_report, get_reports

app = FastAPI()
init_db()

@app.post("/research")
def research(request: RequestResearch):
    report = run(request.goal) 
    save_report(report)
    return report
    
@app.get("/reports")
def reports():
    reports = get_reports()
    return reports
