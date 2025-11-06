from typing import Protocol, List
from ...core.models import BusinessRecord

class DataProcessor(Protocol):
    """
    Abstract interface to process raw data (e.g., CSV) into domain records.
    This is a 'port' — implemented by adapters in infrastructure/.
    """
    def process(self, raw_data: str) -> List[BusinessRecord]:
        ...