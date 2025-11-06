from dataclasses import dataclass
from datetime import date
from enum import Enum

class StatusEnum(str, Enum):
    """
    Valid statuses for a business record.
    Inherits from str to allow JSON serialization and easy comparison with strings.
    """
    COMPLETED = "completed"
    PENDING = "pending"
    CANCELLED = "cancelled"

@dataclass(frozen=True)
class BusinessRecord:
    date: date
    amount: float
    category: str  # e.g., "sale", "lead", "expense"
    status: StatusEnum

@dataclass(frozen=True)
class MetricsSummary:
    total_revenue: float
    mom_growth_rate: float
    average_ticket: float
    total_leads: int
    monthly_revenue: dict[str, float]  # ISO year-month: "2025-01"