from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
	google_api_key: str = "sample_api_key"
	shell: str = ""
	app_data: str = ""

	model_config = SettingsConfigDict(env_file=".env")


settings: Settings = Settings()
