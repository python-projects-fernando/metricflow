from dataclasses import dataclass

@dataclass(frozen=True)
class ProcessCsvInput:
    """Input for the CSV processing use case. Raw CSV content as string"""
    csv_content: str

@dataclass(frozen=True)
class ProcessCsvOutput:
    """Output of the CSV processing use case."""
    total_revenue: float
    mom_growth_rate: float
    average_ticket: float
    total_leads: int
    monthly_revenue: dict[str, float]  # ISO year-month: "2025-01"