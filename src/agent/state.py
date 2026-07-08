from typing import TypedDict


class LogAnalysisState(TypedDict, total=False):
    input_path: str
    output_path: str
    raw_log: str
    sanitized_log: str
    validation_errors: list[str]
    detected_errors: list[str]
    detected_warnings: list[str]
    severity: str
    summary: str
    recommendation: str
    report_content: str
    report_path: str
    status: str
