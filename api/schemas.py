from pydantic import BaseModel, Field
from typing import Literal, Optional


class ChurnInput(BaseModel):
    tenure: int = Field(..., ge=0, le=100)
    MonthlyCharges: float = Field(..., ge=0)
    TotalCharges: Optional[float] = Field(None, ge=0)
    SeniorCitizen: int = Field(..., ge=0, le=1)

    gender: Literal['Male', 'Female']
    Partner: Literal['Yes', 'No']
    Dependents: Literal['Yes', 'No']
    PhoneService: Literal['Yes', 'No']
    MultipleLines: Literal['Yes', 'No', 'No phone service']
    InternetService: Literal['DSL', 'Fiber optic', 'No']
    OnlineSecurity: Literal['Yes', 'No', 'No internet service']
    OnlineBackup: Literal['Yes', 'No', 'No internet service']
    DeviceProtection: Literal['Yes', 'No', 'No internet service']
    TechSupport: Literal['Yes', 'No', 'No internet service']
    StreamingTV: Literal['Yes', 'No', 'No internet service']
    StreamingMovies: Literal['Yes', 'No', 'No internet service']
    Contract: Literal['Month-to-month', 'One year', 'Two year']
    PaperlessBilling: Literal['Yes', 'No']
    PaymentMethod: Literal[
        'Electronic check', 'Mailed check',
        'Bank transfer (automatic)', 'Credit card (automatic)'
    ]

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "tenure": 12, "MonthlyCharges": 70.5, "TotalCharges": 850.0,
                "SeniorCitizen": 0, "gender": "Male", "Partner": "Yes",
                "Dependents": "No", "PhoneService": "Yes", "MultipleLines": "No",
                "InternetService": "Fiber optic", "OnlineSecurity": "No",
                "OnlineBackup": "No", "DeviceProtection": "No",
                "TechSupport": "No", "StreamingTV": "Yes",
                "StreamingMovies": "Yes", "Contract": "Month-to-month",
                "PaperlessBilling": "Yes",
                "PaymentMethod": "Electronic check"
            }]
        }
    }


class ChurnOutput(BaseModel):
    prediction: int
    probability_churn: float
    label: str