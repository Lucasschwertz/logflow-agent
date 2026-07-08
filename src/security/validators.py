from pathlib import Path

ALLOWED_EXTENSIONS = {'.log', '.txt'}
MAX_FILE_SIZE_KB = 512


def validate_log_path(file_path: str) -> list[str]:
    errors: list[str] = []

    if not file_path or not file_path.strip():
        return ['O caminho do arquivo não foi informado.']

    path = Path(file_path)

    if not path.exists():
        errors.append(f'Arquivo não encontrado: {file_path}')
        return errors

    if not path.is_file():
        errors.append(f'O caminho informado não é um arquivo: {file_path}')

    if path.suffix.lower() not in ALLOWED_EXTENSIONS:
        errors.append(
            f'Extensão inválida: {path.suffix}. Use apenas .log ou .txt.'
        )

    file_size_kb = path.stat().st_size / 1024
    if file_size_kb > MAX_FILE_SIZE_KB:
        errors.append(
            f'Arquivo maior que o limite de {MAX_FILE_SIZE_KB} KB.'
        )

    return errors


def validate_log_content(content: str) -> list[str]:
    if not content or not content.strip():
        return ['O arquivo de log está vazio.']

    return []
