from enum import Enum

from src.core.exceptions import ValidationError


class BaseEnum(Enum):
    def __str__(self):
        return self.value

    @property
    def value(self) -> str:
        return super().value

    @classmethod
    def choices(cls):
        """Generate choices for use in Django models."""
        return [(item.value, item.name) for item in cls]

    @classmethod
    def from_string(cls, value: str):
        """Convert string to enum value with case-insensitive matching."""
        if not isinstance(value, str):
            raise ValidationError(f"Expected string, got {type(value).__name__}")

        value = value.lower().strip()

        # Try exact match first
        for enum_member in cls:
            if enum_member.value.lower() == value:
                return enum_member

        # If no match found, raise error with available options
        available_values = cls.get_all_values()
        raise ValidationError(
            f"Unknown value '{value}' for enum {cls.__name__}. "
            f"Supported: {', '.join(available_values)}"
        )

    @classmethod
    def get_all_values(cls):
        """Return all possible string values for this enum."""
        return [e.value for e in cls]
