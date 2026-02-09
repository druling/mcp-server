from src.core.enums.BaseEnum import BaseEnum


class CustomHeader(BaseEnum):
    """
    Enum for custom headers used in HTTP requests.
    """
    X_INTERNAL_AUTH = "x-internal-auth"