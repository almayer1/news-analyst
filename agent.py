from openai import OpenAI
from json_repair import repair_json
import json

from config import settings
from models import Report, Action, AgentState
from tools import TOOLS
from exceptions import IterationLimitReached

SYSTEM_PROMPT = """
GOAL: You are a News Analyst. When given a topic you research the topic using your tools and collected data until you feel you have sufficient data then write_report

RULES:
- You must ALWAYS search before writing a report
- NEVER cite a "fake" source
- ONLY use URLs from the collected data as sources
- search AT LEAST 3 times with different angles before writing
- ONLY call your next needed tool

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
- only repsond with one tool and args combo
"""

client = OpenAI(
    base_url=settings.llm_base_url,
    api_key=settings.llm_api_key
)

def run(goal: str) -> Report | None:
    state = AgentState(
        goal=goal,
        history=[],
        iteration=0,
    )
    # while not done and iteration are less than 10
    while not state.done and state.iteration < settings.max_iterations:
        state.iteration += 1
        # Think
        action = think(state)
        
        # Act
        result = TOOLS[action.tool](**action.args)

        #Observe
        if action.tool == "write_report":
            return result
        elif action.tool == "search_web": 
            state.history.append(result)

    raise IterationLimitReached("Agent exceeded max iterations without writing a report")

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

    # Try 3 attempts
    e = ""
    for attempt in range(3):
        # Get response
        response = client.chat.completions.create(
            model=settings.llm_model,
            messages=messages
        )
        try:
            action = json.loads(response.choices[0].message.content)
            # LLM responds with correct JSON
            return Action(**action)
        except Exception as e:
            try:
                # Try to repair
                fixed = repair_json(response.choices[0].message.content)
                return Action(**json.loads(fixed))
            except Exception:
                # Try again
                continue  

    raise ValueError(f"LLM returned invalid response: {e}")
