from functools import lru_cache
from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="TAINUX_", case_sensitive=False)

    log_level: str = "INFO"
    default_namespace: str = "default"
    allowed_namespaces: str = ""
    diagnostics_mode: str = "rules"
    cors_allow_origins_raw: str = "*"

    @property
    def cors_allow_origins(self) -> List[str]:
        if self.cors_allow_origins_raw.strip() == "*":
            return ["*"]
        return [item.strip() for item in self.cors_allow_origins_raw.split(",") if item.strip()]

    @property
    def allowed_namespaces_list(self) -> List[str]:
        if not self.allowed_namespaces.strip():
            return []
        return [item.strip() for item in self.allowed_namespaces.split(",") if item.strip()]

    @field_validator("diagnostics_mode")
    @classmethod
    def validate_mode(cls, value: str) -> str:
        valid = {"rules", "hybrid"}
        if value not in valid:
            raise ValueError(f"diagnostics_mode must be one of {sorted(valid)}")
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
