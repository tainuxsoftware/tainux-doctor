from fastapi import APIRouter, HTTPException

from app.schemas.diagnose import DiagnoseRequest, DiagnoseResponse
from app.services.diagnosis_service import diagnose_question
from app.core.exceptions import DiagnosisError

router = APIRouter()

@router.post("/diagnose", response_model=DiagnoseResponse)
def diagnose(payload: DiagnoseRequest) -> DiagnoseResponse:
    try:
        return diagnose_question(payload)
    except DiagnosisError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
