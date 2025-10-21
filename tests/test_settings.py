"""
Unit tests for the Settings configuration.
"""
import pytest # noqa: F401
from gev_ai.settings.settings import Settings


class TestSettings:
    """Test the Settings configuration class."""

    def test_settings_default_values(self):
        """Test that Settings has correct default values."""
        settings = Settings()

        assert isinstance(settings.shell, str)
        assert isinstance(settings.app_data, str)

    def test_settings_can_be_initialized_with_values(self):
        """Test that Settings can be initialized with custom values."""
        settings = Settings(
            google_api_key="test_key_123",
            shell="/bin/bash",
            app_data="/home/user/.gev_ai"
        )
        assert settings.google_api_key == "test_key_123"
        assert settings.shell == "/bin/bash"
        assert settings.app_data == "/home/user/.gev_ai"

    def test_settings_is_pydantic_basemodel(self):
        """Test that Settings inherits from pydantic BaseSettings."""
        settings = Settings()
        assert hasattr(settings, "model_dump")
        assert hasattr(settings, "model_validate")
