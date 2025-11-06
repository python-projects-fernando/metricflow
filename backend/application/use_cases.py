from typing import Dict
from ..core.models import StatusEnum
from .dtos import ProcessCsvInput, ProcessCsvOutput
from .interfaces.data_processor import DataProcessor

class ProcessCsvUseCase:
    """
    Use case: process raw CSV data and compute business metrics.
    Depends only on the DataProcessor interface (injected at runtime).
    """

    def __init__(self, data_processor: DataProcessor):
        self._data_processor = data_processor

    def execute(self, input_dto: ProcessCsvInput) -> ProcessCsvOutput:
        # Step 1: Parse raw CSV into domain records
        records = self._data_processor.process(input_dto.csv_content)

        # Step 2: Filter only valid/completed sales for revenue
        completed_sales = [
            r for r in records
            if r.category == "sale" and r.status == StatusEnum.COMPLETED
        ]

        # Step 3: Compute metrics
        total_revenue = sum(r.amount for r in completed_sales)
        average_ticket = total_revenue / len(completed_sales) if completed_sales else 0.0
        total_leads = len([r for r in records if r.category == "lead"])

        # Step 4: Group revenue by month (YYYY-MM)
        monthly_rev: Dict[str, float] = {}
        for sale in completed_sales:
            month_key = sale.date.strftime("%Y-%m")
            monthly_rev[month_key] = monthly_rev.get(month_key, 0.0) + sale.amount

        # Step 5: Calculate MoM growth
        sorted_months = sorted(monthly_rev.keys())
        mom_growth = 0.0
        if len(sorted_months) >= 2:
            last_month = monthly_rev[sorted_months[-1]]
            prev_month = monthly_rev[sorted_months[-2]]
            if prev_month > 0:
                mom_growth = ((last_month - prev_month) / prev_month) * 100

        # Step 6: Return DTO
        return ProcessCsvOutput(
            total_revenue=total_revenue,
            mom_growth_rate=mom_growth,
            average_ticket=average_ticket,
            total_leads=total_leads,
            monthly_revenue=monthly_rev
        )