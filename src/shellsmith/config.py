from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    basyx_env_host: str = "http://localhost:8081"
    neo4j_uri: str = "neo4j://localhost:7687"

    @property
    def host(self):
        return self.basyx_env_host

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="SHELLSMITH_",
        extra="ignore",
    )


config = Settings()
