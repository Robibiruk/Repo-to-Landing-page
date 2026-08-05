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
    # A/B'd 2026-08-05: nemotron passes the critic; poolside is reliable but weak; gemma 429s.
    openrouter_fallback_models: str = "poolside/laguna-s-2.1:free,google/gemma-4-31b-it:free"
    llm_provider: str = "openrouter"
    # Share-loop badge target: where "Built with RepoPages" links. Empty = badge is not a link.
    # Set to the product/gallery URL once live (today: the project's GitHub repo).
    repopages_url: str = ""
    # CORS: comma-separated origins (localhost + deployed frontend URL).
    cors_origins: str = "http://localhost:5173,http://localhost:3000"
    # Quality gate: after generation, a critic scores the copy and drives a targeted rewrite.
    quality_gate: bool = True
    # Max targeted refine rounds after a failed critique (bounds latency/cost on the free tier).
    max_refine_rounds: int = 1

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]
    github_api_base: str = "https://api.github.com"


settings = Settings()
