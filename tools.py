from tavily import TavilyClient

from config import settings
from models import SearchResult, Result, Report, Perspective, Source

def search_web(query: str) -> SearchResult:
    # Search web
    client = TavilyClient(api_key=settings.tavily_api_key)
    response = client.search(query)
    
    # Extract results
    results = []
    for result in response["results"]:
        results.append(
            Result(
                url=result["url"],
                title=result["title"],
                content=result["content"]
            )
        )

    return SearchResult(
        query=query,
        results=results
    )

def write_report(goal: str, perspectives: list[dict], conclusion: str, sources: list[dict]) -> Report:
    return Report(
        goal=goal,
        perspectives=[Perspective(**p) for p in perspectives],
        conclusion=conclusion,
        sources=[Source(**s) for s in sources]
    )

TOOLS = {
    "search_web": search_web,
    "write_report": write_report
}
