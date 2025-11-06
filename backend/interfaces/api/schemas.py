from pydantic import BaseModel
from typing import Dict

class MetricsResponse(BaseModel):
    total_revenue: float
    mom_growth_rate: float
    average_ticket: float
    total_leads: int
    monthly_revenue: Dict[str, float]