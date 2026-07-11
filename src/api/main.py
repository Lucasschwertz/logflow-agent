from pathlib import Path
from tempfile import TemporaryDirectory

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.agent.graph import build_graph
from src.api.schemas import AnalyzeResponse, HealthResponse

ALLOWED_UPLOAD_EXTENSIONS = {'.log', '.txt'}
DEFAULT_REPORT_PATH = 'outputs/logflow-report.md'
LOCAL_DEVELOPMENT_ORIGINS = [
    'http://localhost:8080',
    'http://127.0.0.1:8080',
    'http://localhost:5173',
    'http://127.0.0.1:5173',
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]

app = FastAPI(
    title='LogFlow Agent API',
    description='API HTTP opcional para análise de logs pelo LogFlow Agent.',
    version='1.0.0',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=LOCAL_DEVELOPMENT_ORIGINS,
    allow_methods=['GET', 'POST', 'OPTIONS'],
    allow_headers=['*'],
)


@app.get('/health', response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status='ok', service='logflow-agent')


@app.post('/analyze', response_model=AnalyzeResponse)
async def analyze(file: UploadFile = File(...)) -> AnalyzeResponse | JSONResponse:
    suffix = Path(file.filename or '').suffix.lower()

    if suffix not in ALLOWED_UPLOAD_EXTENSIONS:
        return JSONResponse(
            status_code=400,
            content=AnalyzeResponse(
                status='validation_failed',
                validation_errors=[
                    f'Extensão inválida: {suffix or "sem extensão"}. '
                    'Use apenas .log ou .txt.'
                ],
            ).model_dump(),
        )

    with TemporaryDirectory(prefix='logflow-api-') as temp_dir:
        input_path = Path(temp_dir) / f'uploaded{suffix}'
        content = await file.read()
        input_path.write_bytes(content)

        result = build_graph().invoke(
            {
                'input_path': str(input_path),
                'output_path': DEFAULT_REPORT_PATH,
            }
        )

    return AnalyzeResponse(
        status=result.get('status'),
        severity=result.get('severity'),
        summary=result.get('summary'),
        recommendation=result.get('recommendation'),
        validation_errors=result.get('validation_errors', []),
        report_path=result.get('report_path'),
    )
