from pydantic import BaseModel

class Source(BaseModel):
    url: str
    title: str

class Perspective(BaseModel):
    name: str
    summary: str

class Result(Source):
    content: str

class Action(BaseModel):
    tool: str
    args: dict

class SearchResult(BaseModel):
    query: str
    results: list[Result]

class AgentState(BaseModel):
    goal: str
    history: list[SearchResult]
    iteration: int
    done: bool = False

class Report(BaseModel):
    goal: str
    perspectives: list[Perspective]
    conclusion: str
    sources: list[Source]

