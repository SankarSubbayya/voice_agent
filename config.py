"""
Configuration management for ReturnFlow Voice Agent.

Loads environment variables from .env file and provides
centralized access to configuration settings.
"""

import os
from pathlib import Path
from typing import Optional


class Config:
    """Configuration manager for the application."""

    def __init__(self):
        """Initialize configuration from environment variables."""
        self._load_env_file()

    def _load_env_file(self):
        """Load environment variables from .env file if it exists."""
        env_file = Path(__file__).parent / '.env'

        if env_file.exists():
            with open(env_file) as f:
                for line in f:
                    line = line.strip()
                    # Skip comments and empty lines
                    if not line or line.startswith('#'):
                        continue
                    # Parse KEY=VALUE
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        # Only set if not already in environment
                        if key not in os.environ:
                            os.environ[key] = value

    # ==========================================================================
    # GENERAL SETTINGS
    # ==========================================================================

    @property
    def environment(self) -> str:
        """Get current environment (development, staging, production)."""
        return os.getenv('ENVIRONMENT', 'development')

    @property
    def debug(self) -> bool:
        """Check if debug mode is enabled."""
        return os.getenv('DEBUG', 'false').lower() in ('true', '1', 'yes')

    @property
    def use_mock_apis(self) -> bool:
        """Check if mock APIs should be used."""
        return os.getenv('USE_MOCK_APIS', 'true').lower() in ('true', '1', 'yes')

    @property
    def use_mock_database(self) -> bool:
        """Check if mock database should be used."""
        return os.getenv('USE_MOCK_DATABASE', 'true').lower() in ('true', '1', 'yes')

    @property
    def use_mock_carriers(self) -> bool:
        """Check if mock carrier APIs should be used."""
        return os.getenv('USE_MOCK_CARRIERS', 'true').lower() in ('true', '1', 'yes')

    # ==========================================================================
    # VOICE & SPEECH
    # ==========================================================================

    @property
    def vocalbridge_api_key(self) -> Optional[str]:
        """Get VocalBridge API key."""
        return os.getenv('VOCALBRIDGE_API_KEY')

    @property
    def vocalbridge_endpoint(self) -> str:
        """Get VocalBridge API endpoint."""
        return os.getenv('VOCALBRIDGE_ENDPOINT', 'https://api.vocalbridge.ai/v1')

    @property
    def google_speech_api_key(self) -> Optional[str]:
        """Get Google Speech API key."""
        return os.getenv('GOOGLE_SPEECH_API_KEY')

    @property
    def aws_access_key_id(self) -> Optional[str]:
        """Get AWS access key ID."""
        return os.getenv('AWS_ACCESS_KEY_ID')

    @property
    def aws_secret_access_key(self) -> Optional[str]:
        """Get AWS secret access key."""
        return os.getenv('AWS_SECRET_ACCESS_KEY')

    @property
    def aws_region(self) -> str:
        """Get AWS region."""
        return os.getenv('AWS_REGION', 'us-east-1')

    # ==========================================================================
    # CARRIERS
    # ==========================================================================

    @property
    def ups_api_key(self) -> Optional[str]:
        """Get UPS API key."""
        return os.getenv('UPS_API_KEY')

    @property
    def usps_user_id(self) -> Optional[str]:
        """Get USPS user ID."""
        return os.getenv('USPS_USER_ID')

    @property
    def fedex_api_key(self) -> Optional[str]:
        """Get FedEx API key."""
        return os.getenv('FEDEX_API_KEY')

    # ==========================================================================
    # PAYMENTS
    # ==========================================================================

    @property
    def stripe_api_key(self) -> Optional[str]:
        """Get Stripe API key."""
        return os.getenv('STRIPE_API_KEY')

    @property
    def paypal_client_id(self) -> Optional[str]:
        """Get PayPal client ID."""
        return os.getenv('PAYPAL_CLIENT_ID')

    # ==========================================================================
    # NOTIFICATIONS
    # ==========================================================================

    @property
    def twilio_account_sid(self) -> Optional[str]:
        """Get Twilio account SID."""
        return os.getenv('TWILIO_ACCOUNT_SID')

    @property
    def twilio_auth_token(self) -> Optional[str]:
        """Get Twilio auth token."""
        return os.getenv('TWILIO_AUTH_TOKEN')

    @property
    def twilio_phone_number(self) -> Optional[str]:
        """Get Twilio phone number."""
        return os.getenv('TWILIO_PHONE_NUMBER')

    @property
    def sendgrid_api_key(self) -> Optional[str]:
        """Get SendGrid API key."""
        return os.getenv('SENDGRID_API_KEY')

    # ==========================================================================
    # DATABASE
    # ==========================================================================

    @property
    def database_url(self) -> Optional[str]:
        """Get database URL."""
        return os.getenv('DATABASE_URL')

    @property
    def redis_url(self) -> Optional[str]:
        """Get Redis URL."""
        return os.getenv('REDIS_URL')

    # ==========================================================================
    # SECURITY
    # ==========================================================================

    @property
    def secret_key(self) -> str:
        """Get secret key for sessions."""
        return os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

    @property
    def jwt_secret(self) -> str:
        """Get JWT secret for authentication."""
        return os.getenv('JWT_SECRET', 'dev-jwt-secret-change-in-production')

    # ==========================================================================
    # BUSINESS LOGIC
    # ==========================================================================

    @property
    def default_return_window_days(self) -> int:
        """Get default return window in days."""
        return int(os.getenv('DEFAULT_RETURN_WINDOW_DAYS', '30'))

    @property
    def fraud_risk_threshold(self) -> float:
        """Get fraud risk threshold."""
        return float(os.getenv('FRAUD_RISK_THRESHOLD', '0.7'))

    # ==========================================================================
    # LOGGING
    # ==========================================================================

    @property
    def log_level(self) -> str:
        """Get logging level."""
        return os.getenv('LOG_LEVEL', 'INFO')

    @property
    def log_file(self) -> Optional[str]:
        """Get log file path."""
        return os.getenv('LOG_FILE')

    # ==========================================================================
    # HELPERS
    # ==========================================================================

    def is_production(self) -> bool:
        """Check if running in production."""
        return self.environment == 'production'

    def has_vocalbridge(self) -> bool:
        """Check if VocalBridge API key is configured."""
        return self.vocalbridge_api_key is not None and len(self.vocalbridge_api_key) > 0

    def has_real_carriers(self) -> bool:
        """Check if real carrier APIs are configured."""
        return (self.ups_api_key or self.usps_user_id or self.fedex_api_key) is not None

    def validate(self) -> list[str]:
        """
        Validate configuration and return list of warnings/errors.

        Returns:
            List of validation messages
        """
        warnings = []

        if self.is_production():
            if self.secret_key == 'dev-secret-key-change-in-production':
                warnings.append("WARNING: Using development secret key in production!")

            if self.use_mock_apis:
                warnings.append("WARNING: Mock APIs enabled in production!")

            if not self.has_vocalbridge():
                warnings.append("INFO: VocalBridge API key not configured")

        return warnings


# Global configuration instance
config = Config()


# Convenience function
def get_config() -> Config:
    """Get the global configuration instance."""
    return config
