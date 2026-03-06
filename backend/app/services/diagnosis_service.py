from app.schemas.diagnose import DiagnoseRequest, DiagnoseResponse
from app.diagnostics.engine import run_diagnosis


def diagnose_question(payload: DiagnoseRequest) -> DiagnoseResponse:
    result = run_diagnosis(
        question=payload.question,
        namespace=payload.namespace,
        resource_name=payload.resource_name,
        include_logs=payload.include_logs,
    )
    return DiagnoseResponse(**result)
