from pydantic import BaseModel


class CreditData(BaseModel):
    usage_id: str
    profile_id: str
    amount: int
