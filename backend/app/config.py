from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    github_token: str = ""
    openrouter_api_key: str = ""
    # Default to a free open-source model (no monthly cost). Swap to
    # anthropic/claude-sonnet-5 (or any paid model) anytime via env — quality ceiling
    # is higher, but for an MVP the free tier is the right default.
    openrouter_model: str = "nvidia/nemotron-3-super-120b-a12b:free"
    # Comma-separated free-model fallbacks for when the primary is rate-limited (429).
    openrouter_fallback_models: str = "google/gemma-4-31b-it:free,poolside/laguna-s-2.1:free"
    llm_provider: str = "openrouter"
    github_api_base: str = "https://api.github.com"


settings = Settings()
