from typing import Protocol
from io import BytesIO
from backend.application.dtos import ProcessCsvOutput

class ReportGenerator(Protocol):

    def generate_report(self, output_dto: ProcessCsvOutput) -> BytesIO:
        ...
