import redis
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import StreamingResponse
from io import StringIO, BytesIO
import uuid
import json
import dataclasses
from backend.application.use_cases import ProcessCsvUseCase
from backend.application.dtos import ProcessCsvInput, ProcessCsvOutput
from backend.infrastructure.file_processors import CsvDataProcessor
from .schemas import MetricsResponse
from backend.infrastructure.config.redis_config import get_redis_client
from ...infrastructure.file_processors.excel_report_generator import ExcelReportGenerator
from ...infrastructure.file_processors.pdf_report_generator import PdfReportGenerator

router = APIRouter(prefix="/api", tags=["metrics"])

def get_use_case() -> ProcessCsvUseCase:
    """Dependency: create use case with concrete CSV processor."""
    processor = CsvDataProcessor()
    return ProcessCsvUseCase(data_processor=processor)

def get_redis() -> redis.Redis:
    return get_redis_client()

def get_excel_generator() -> ExcelReportGenerator:
    return ExcelReportGenerator()

def get_pdf_generator() -> PdfReportGenerator:
    return PdfReportGenerator()

@router.post("/upload-csv", response_model=MetricsResponse)
async def upload_csv(
    file: UploadFile = File(...),
    use_case: ProcessCsvUseCase = Depends(get_use_case),
    redis_client: redis.Redis = Depends(get_redis)
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

        report_id = str(uuid.uuid4())
        output_dict = dataclasses.asdict(output)
        output_json = json.dumps(output_dict)

        redis_client.setex(report_id, 3600, output_json)
        response_data = output.__dict__.copy()
        response_data['report_id'] = report_id

        return MetricsResponse(**response_data)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"CSV processing error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/export/excel/{report_id}")
async def export_excel(
    report_id: str,
    redis_client: redis.Redis = Depends(get_redis),
    excel_generator: ExcelReportGenerator = Depends(get_excel_generator)
):
    try:
        uuid.UUID(report_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid report ID format")

    cached_data = redis_client.get(report_id)
    if not cached_data:
        raise HTTPException(status_code=404, detail="Report data not found or expired")

    try:
        cached_dict = json.loads(cached_data)
        output_dto = ProcessCsvOutput(**cached_dict)
    except Exception as e:
        print(f"Error deserializing cached data for ID {report_id}: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving report data")

    excel_buffer: BytesIO = excel_generator.generate_report(output_dto)

    return StreamingResponse(
        excel_buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f"attachment; filename=metricflow_report_{report_id}.xlsx"
        }
    )



@router.get("/export/pdf/{report_id}")
async def export_pdf(
    report_id: str,
    redis_client: redis.Redis = Depends(get_redis),
    pdf_generator: PdfReportGenerator = Depends(get_pdf_generator)
):
    try:
        uuid.UUID(report_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid report ID format")

    cached_data = redis_client.get(report_id)
    if not cached_data:
        raise HTTPException(status_code=404, detail="Report data not found or expired")

    try:
        cached_dict = json.loads(cached_data)
        output_dto = ProcessCsvOutput(**cached_dict)
    except Exception as e:
        print(f"Error deserializing cached data for ID {report_id}: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving report data")

    pdf_buffer: BytesIO = pdf_generator.generate_report(output_dto)

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=metricflow_report_{report_id}.pdf"
        }
    )
