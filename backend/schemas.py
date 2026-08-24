from pydantic import BaseModel, Field

class Transaction(BaseModel):
    amount: float = Field(gt=0)
    transaction_hour: int = Field(ge=0, le=23)
    distance_from_usual_location: float = Field(ge=0)
    device_risk_score: float = Field(ge=0, le=1)
    location_risk_score: float = Field(ge=0, le=1)
    previous_failed_transactions: int = Field(ge=0)
    previous_fraud_history: int = Field(ge=0, le=1)
    recent_transaction_count: int = Field(ge=0)
    account_age_days: int = Field(gt=0)
    merchant_category: str
    payment_method: str
