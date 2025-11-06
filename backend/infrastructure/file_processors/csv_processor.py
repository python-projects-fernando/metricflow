import csv
from io import StringIO
from datetime import datetime
from typing import List
from ...core.models import BusinessRecord, StatusEnum
from ...application.interfaces.data_processor import DataProcessor

class CsvDataProcessor(DataProcessor):
    """
    Concrete adapter that parses CSV content into domain BusinessRecord entities.
    Implements the DataProcessor port defined in the application layer.
    """

    def process(self, raw_data: str) -> List[BusinessRecord]:
        if not raw_data.strip():
            return []

        records: List[BusinessRecord] = []
        reader = csv.DictReader(StringIO(raw_data))

        # Validate required columns
        required_columns = {"date", "amount", "category"}
        if not required_columns.issubset(reader.fieldnames or []):
            missing = required_columns - set(reader.fieldnames or [])
            raise ValueError(f"Missing required CSV columns: {missing}")

        for row_num, row in enumerate(reader, start=1):
            try:
                # Parse date (expecting YYYY-MM-DD)
                record_date = datetime.strptime(row["date"], "%Y-%m-%d").date()

                # Parse amount (allow negative for expenses)
                amount = float(row["amount"])

                # Category is free text (str)
                category = row["category"].strip()

                # Status: use enum or default to 'completed' if not provided
                status_str = row.get("status", "completed").strip().lower()
                try:
                    status = StatusEnum(status_str)
                except ValueError:
                    raise ValueError(
                        f"Row {row_num}: invalid status '{status_str}'. "
                        f"Allowed: {[s.value for s in StatusEnum]}"
                    )

                records.append(
                    BusinessRecord(
                        date=record_date,
                        amount=amount,
                        category=category,
                        status=status
                    )
                )

            except ValueError as e:
                raise ValueError(f"Row {row_num}: invalid data — {e}") from e
            except Exception as e:
                raise ValueError(f"Row {row_num}: unexpected error — {e}") from e

        return records