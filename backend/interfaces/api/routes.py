from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from io import StringIO
from ...application.use_cases import ProcessCsvUseCase
from ...application.dtos import ProcessCsvInput
from ...infrastructure.file_processors import CsvDataProcessor
from .schemas import MetricsResponse

router = APIRouter(prefix="/api", tags=["metrics"])

def get_use_case() -> ProcessCsvUseCase:
    """Dependency: create use case with concrete CSV processor."""
    processor = CsvDataProcessor()
    return ProcessCsvUseCase(data_processor=processor)

@router.post("/upload-csv", response_model=MetricsResponse)
async def upload_csv(
    file: UploadFile = File(...),
    use_case: ProcessCsvUseCase = Depends(get_use_case)
):
    """
    Upload a CSV file and get business metrics instantly.
    Expected columns: date (YYYY-MM-DD), amount, category, [status]
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")

    try:
        content = await file.read()
        csv_text = content.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="Invalid file encoding. Use UTF-8.")

    # Trim BOM if present
    if csv_text.startswith("\ufeff"):
        csv_text = csv_text[1:]

    if not csv_text.strip():
        raise HTTPException(status_code=400, detail="CSV file is empty")

    try:
        input_dto = ProcessCsvInput(csv_content=csv_text)
        output = use_case.execute(input_dto)
        return MetricsResponse(**output.__dict__)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"CSV processing error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")