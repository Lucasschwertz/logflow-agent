import re

TOKEN_PATTERNS = [
    r'(?i)(api[_-]?key\s*=\s*)[^\s]+',
    r'(?i)(token\s*=\s*)[^\s]+',
    r'(?i)(password\s*=\s*)[^\s]+',
    r'(?i)(secret\s*=\s*)[^\s]+',
]


def sanitize_sensitive_data(log_text: str) -> str:
    sanitized = log_text

    for pattern in TOKEN_PATTERNS:
        sanitized = re.sub(pattern, r'\1[REDACTED]', sanitized)

    return sanitized


def extract_error_lines(log_text: str) -> list[str]:
    return [
        line.strip()
        for line in log_text.splitlines()
        if 'ERROR' in line.upper() or 'FAILED' in line.upper()
    ]


def extract_warning_lines(log_text: str) -> list[str]:
    return [
        line.strip()
        for line in log_text.splitlines()
        if 'WARNING' in line.upper() or 'WARN' in line.upper()
    ]


def classify_severity(errors: list[str], warnings: list[str]) -> str:
    if len(errors) >= 2:
        return 'alta'

    if len(errors) == 1:
        return 'média'

    if warnings:
        return 'baixa'

    return 'informativa'


def build_summary(errors: list[str], warnings: list[str], severity: str) -> str:
    if errors:
        return (
            f'Foram encontrados {len(errors)} erro(s) e '
            f'{len(warnings)} aviso(s). Severidade classificada como {severity}.'
        )

    if warnings:
        return (
            f'Nenhum erro crítico foi encontrado, mas há '
            f'{len(warnings)} aviso(s). Severidade classificada como {severity}.'
        )

    return 'Nenhum erro ou aviso relevante foi encontrado no log.'


def build_recommendation(errors: list[str], warnings: list[str]) -> str:
    joined_errors = ' '.join(errors).lower()

    if 'migration' in joined_errors or 'relation' in joined_errors:
        return (
            'Verificar o estado da migração, revisar scripts já aplicados '
            'e garantir idempotência antes de executar novamente.'
        )

    if 'dependency' in ' '.join(warnings).lower():
        return (
            'Atualizar dependências depreciadas e validar compatibilidade '
            'antes do próximo deploy.'
        )

    if errors:
        return (
            'Analisar as linhas de erro, reproduzir o problema localmente '
            'e corrigir a causa antes de reexecutar o pipeline.'
        )

    if warnings:
        return 'Revisar os avisos antes da próxima execução.'

    return 'Nenhuma ação corretiva é necessária no momento.'
