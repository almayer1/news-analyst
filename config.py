from pydantic_settings import BaseSettings

class Settings():
    # LLM
    llm_base_url: str = "http://localhost:11434/v1"
    llm_api_key: str = "ollama"
    llm_model: str = "llama3.2"

    # Tavily
    tavily_api_url: str = "placeholder"
