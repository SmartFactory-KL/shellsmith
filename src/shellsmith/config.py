"""Configuration for accessing AAS and Neo4j environments."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """App configuration loaded from environment variables.

    Loads environment variables from a `.env` file with the prefix `SHELLSMITH_`.
    Defaults are provided for local development. Extra fields are ignored.

    Attributes:
        basyx_env_host: The base URL of the BaSyx AAS Environment.
        neo4j_uri: The connection URI for the Neo4j database.

    Properties:
        host: Alias for `basyx_env_host`.
    """

    basyx_env_host: str = "http://localhost:8081"
    neo4j_uri: str = "neo4j://localhost:7687"

    @property
    def host(self) -> str:
        """Returns the base URL of the BaSyx AAS environment.

        Returns:
            The BaSyx AAS environment host.
        """
        return self.basyx_env_host

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="SHELLSMITH_",
        extra="ignore",
    )


config = Settings()

DEFAULT_TIMEOUT = 5.0
