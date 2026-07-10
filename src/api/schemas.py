from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    service: str


class AnalyzeResponse(BaseModel):
    status: str | None = None
    severity: str | None = None
    summary: str | None = None
    recommendation: str | None = None
    validation_errors: list[str] = Field(default_factory=list)
    report_path: str | None = None
