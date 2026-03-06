from typing import List, Optional

from pydantic import BaseModel, Field


class DiagnoseRequest(BaseModel):
    question: str = Field(..., description="Diagnostic question from the user")
    namespace: Optional[str] = Field(default=None, description="Kubernetes namespace")
    resource_name: Optional[str] = Field(default=None, description="Kubernetes pod name to inspect")
    include_logs: bool = Field(default=True, description="Whether to fetch pod logs")


class EvidenceItem(BaseModel):
    source: str
    message: str


class RecommendationItem(BaseModel):
    action: str
    rationale: str


class DiagnoseResponse(BaseModel):
    summary: str
    affected_resource: Optional[str] = None
    root_cause: Optional[str] = None
    confidence: str
    evidence: List[EvidenceItem] = []
    recommendations: List[RecommendationItem] = []
    raw_signals: dict = {}
