from pydantic import BaseModel, field_validator


class RemAccount(BaseModel):
    account_address: str
    balance: float
    energy: int
    bandwidth: int

    @field_validator('balance', 'energy', 'bandwidth')
    @classmethod
    def check_positive(cls, v):
        if v < 0:
            raise ValueError('Must be positive')
        return v