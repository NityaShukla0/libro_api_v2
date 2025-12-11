# app/config/feature_flags.py
from app.config.settings import settings

class FeatureFlags:
    """
    Central place to manage feature flags.
    Use the settings from .env via Settings.
    """
    ENABLE_BORROW = settings.ENABLE_BORROW
    ENABLE_RETURN = settings.ENABLE_RETURN
    ENABLE_CACHE = settings.ENABLE_CACHE
    ENABLE_USERS = settings.ENABLE_USERS
    ENABLE_BOOKS = settings.ENABLE_BOOKS