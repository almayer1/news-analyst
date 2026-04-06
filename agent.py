from openai import OpenAI
import json

from config import settings
from models import Report, Action, AgentState
from tools import TOOLS

SYSTEM_PROMPT = """
GOAL: You are a News Analyst. When given a topic you research the topic using your tools and collected data until you feel you have sufficient data then write_report

TOOLS: format -> "tool_name", args(parameter: parameter_type). Note
- "search_web", args(query: str). Allows you to search the web
    - {"tool": "search_web", "args": {"query": "..."}}
- "write_report", args(goal: str, perspectives: list, conclusion: str, sources: list).Write a report based on researched data
    - {"tool": "write_report", "args": {"goal": "...", "perspectives": [{"name": "...", "summary": "..."}, ...], "conclusion": "...", "sources": [{"url": "...", "title": "..."}, ...]}}

COLLECTED DATA: 
- JSON passed by user

RESPONSE: 
- VERY IMPORTANT respond only in JSON
- response: {"tool": tool_name, "args": arguments} 
"""

client = OpenAI(
    base_url=settings.llm_base_url,
    api_key=settings.llm_api_key
)

def run(goal: str) -> Report:
    state = AgentState(
        goal=goal,
        results=[],
        iteration=0,
    )
    # while not done and iteration are less than 10

    # Think (query, history)
    action = think(state)

    # Act (tools_list)

    result = TOOLS[f"{action.tool}"](**action.args)

    # Observe ()

    pass

def think(state: AgentState) -> Action:
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT}, 
        {"role": "user", "content": f"Goal: {state.goal}"}
    ]

    # History
    history = state.history
    for result in history:
        assitant = {"role": "assistant", "content": json.dumps({"tool": "search_web", "args": {"query": result.query}})}
        user = {"role": "user", "content": f"{json.dumps(result.model_dump())}"}
        messages.append(assitant)
        messages.append(user)

    response = client.chat.completions.create(
        model=settings.llm_model,
        messages=messages
    )
    try:
        action = json.loads(response.choices[0].message.content)
        return Action(**action)
    except Exception as e:
        raise ValueError(f"LLM returned invalid response: {e}")
