# News Analyst Agent

An autonomous AI agent that researches any topic by searching the web multiple times from diverse angles, then synthesizes the results into a structured, evidence-based report with multiple perspectives and cited sources.

## How It Works

The agent uses the **ReAct loop** (Reason + Act) to autonomously decide what to search, how many times, and when it has enough information to write a report:

```
Goal → THINK → ACT (search_web) → OBSERVE → THINK → ACT → ... → write_report → DONE
```

The LLM controls the flow — it decides how many searches to run and when to stop. A hard iteration cap prevents infinite loops.

## Example Output

**Topic:** United States involvement with poverty in Africa

**Perspectives:**
- **Official Development Assistance** — The US provided $3.2 billion to sub-Saharan Africa in 2004 to relieve poverty and promote economic growth
- **Withdrawal of Aid** — Some reports suggest withdrawal of US aid could push 5.7 million Africans into extreme poverty by 2026
- **Economic Influence** — The US has been criticized for perpetuating poverty through cotton subsidies and export dumping
- **Poverty Reduction** — Experts project Africa's poverty rate will fall to 29% by 2030 with rising life expectancy

**Sources:** Brookings, Cato Institute, US Government, and others

## Stack

| Layer | Tech |
|---|---|
| LLM | Ollama (llama3.2) — runs locally |
| Web Search | Tavily API |
| API | FastAPI |
| Frontend | Streamlit |
| Storage | SQLite |
| Data Models | Pydantic |
| Package Manager | uv |

## Architecture

```
streamlit_app.py    — UI: submit topics, view past reports
app.py              — FastAPI: POST /research, GET /reports
agent.py            — ReAct loop, LLM reasoning, tool dispatch
tools.py            — search_web() via Tavily, write_report()
store.py            — SQLite: save and retrieve reports
models.py           — Pydantic models: Report, AgentState, SearchResult
config.py           — Settings via .env
```

## Setup

**Prerequisites:** [Ollama](https://ollama.com) and [uv](https://astral.sh/uv) installed

```bash
# Clone and install
git clone <repo>
cd news-analyst
uv sync

# Pull the model
ollama pull llama3.2

# Configure environment
# Create a .env file with:
# TAVILY_API_KEY=your_key_here
# LLM_BASE_URL=http://localhost:11434/v1
```

Get a free Tavily API key at [tavily.com](https://tavily.com) (1000 searches/month free).

## Running

Start Ollama:
```bash
ollama serve
```

Start the API (in a separate terminal):
```bash
uv run uvicorn app:app --reload
```

Start the UI (in a separate terminal):
```bash
uv run streamlit run streamlit_app.py
```

Open `http://localhost:8501` for the UI or `http://localhost:8000/docs` to test the API directly.

## Key Design Decisions

- **ReAct pattern** — the LLM decides the research strategy, not hardcoded logic
- **Tool dispatch via dict** — `TOOLS = {"search_web": ..., "write_report": ...}` makes adding new tools trivial
- **JSON repair + retry** — handles malformed LLM responses gracefully before raising errors
- **Evidence-weighted perspectives** — the agent is prompted to represent views by weight of evidence, not artificially equal treatment
- **SQLite persistence** — reports are saved for retrieval without the overhead of a full database
