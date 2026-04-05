from pydantic import BaseModel

class Source(BaseModel):
    url: str
    title: str

class Perspective(BaseModel):
    name: str
    summary: str

class SearchResult(BaseModel):
    query: str
    source: Source
    summary: str

class AgentState(BaseModel):
    goal: str
    results: list[SearchResult]
    iteration: int
    done: bool

class Report(BaseModel):
    topic: str
    perspectives: list[Perspective]
    conclusion: str
    sources: list[Source]

