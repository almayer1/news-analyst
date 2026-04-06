from fastapi import FastAPI
import json

from models import RequestResearch
from agent import run

app = FastAPI()

@app.post("/research")
def research(request: RequestResearch):
    return run(request.goal) 
    
