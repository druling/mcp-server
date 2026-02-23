from pydantic import BaseModel, Field


class EmailValidation(BaseModel):
    """Email validation result"""
    email: str = Field(description="Email address that was validated")
    is_valid: bool = Field(description="Whether the email is valid")

