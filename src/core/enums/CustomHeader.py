from src.core.enums.BaseEnum import BaseEnum


class CustomHeader(BaseEnum):
    """
    Enum for custom headers used in HTTP requests.
    """
    X_INTERNAL_AUTH = "x-internal-auth"
    X_PROFILE_ID = "x-profile-id"
    X_SECRET_ID = "x-secret-id"
    X_ENTITY_ID = "x-entity-id"
    X_ENTITY_TYPE = "x-entity-type"