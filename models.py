from pydantic import BaseModel

class Source(BaseModel):
    url: str
    title: str

class Perspective(BaseModel):
    name: str
    summary: str

class Result(Source):
    content: str

class SearchResult(BaseModel):
    query: str
    results: list[Result]

class AgentState(BaseModel):
    goal: str
    results: list[SearchResult]
    iteration: int
    done: bool = False

class Report(BaseModel):
    topic: str
    perspectives: list[Perspective]
    conclusion: str
    sources: list[Source]

