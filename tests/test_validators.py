
from src.agent.nodes import generate_report_node
from src.security.validators import validate_log_content, validate_log_path
from src.tools.log_tools import (
    build_recommendation,
    classify_severity,
    extract_error_lines,
    extract_warning_lines,
    sanitize_sensitive_data,
)


def test_validate_log_path_accepts_valid_log_file(tmp_path):
    # Arrange
    log_file = tmp_path / 'pipeline.log'
    log_file.write_text('INFO pipeline ok', encoding='utf-8')

    # Act
    errors = validate_log_path(str(log_file))

    # Assert
    assert errors == []


def test_validate_log_path_rejects_missing_file():
    # Arrange
    missing_file = 'arquivo_inexistente.log'

    # Act
    errors = validate_log_path(missing_file)

    # Assert
    assert errors
    assert 'Arquivo não encontrado' in errors[0]


def test_validate_log_path_rejects_invalid_extension(tmp_path):
    # Arrange
    invalid_file = tmp_path / 'pipeline.exe'
    invalid_file.write_text('INFO pipeline ok', encoding='utf-8')

    # Act
    errors = validate_log_path(str(invalid_file))

    # Assert
    assert errors
    assert 'Extensão inválida' in errors[0]


def test_validate_log_content_rejects_empty_content():
    # Arrange
    content = '   '

    # Act
    errors = validate_log_content(content)

    # Assert
    assert errors == ['O arquivo de log está vazio.']


def test_sanitize_sensitive_data_masks_token_values():
    # Arrange
    log_text = 'ERROR token=abc123 password=secret123 api_key=key123'

    # Act
    sanitized = sanitize_sensitive_data(log_text)

    # Assert
    assert 'abc123' not in sanitized
    assert 'secret123' not in sanitized
    assert 'key123' not in sanitized
    assert '[REDACTED]' in sanitized


def test_extract_error_lines_identifies_error_and_failed_lines():
    # Arrange
    log_text = '''
    INFO Starting pipeline
    ERROR Build failed
    INFO Uploading artifacts
    Pipeline failed with exit code 1
    '''

    # Act
    errors = extract_error_lines(log_text)

    # Assert
    assert len(errors) == 2
    assert 'ERROR Build failed' in errors[0]


def test_extract_warning_lines_identifies_warning_lines():
    # Arrange
    log_text = '''
    INFO Starting pipeline
    WARNING Deprecated dependency detected
    INFO Finished
    '''

    # Act
    warnings = extract_warning_lines(log_text)

    # Assert
    assert len(warnings) == 1
    assert 'WARNING Deprecated dependency detected' in warnings[0]


def test_classify_severity_as_high_when_two_or_more_errors():
    # Arrange
    errors = ['ERROR one', 'ERROR two']
    warnings = []

    # Act
    severity = classify_severity(errors, warnings)

    # Assert
    assert severity == 'alta'


def test_classify_severity_as_medium_when_one_error():
    # Arrange
    errors = ['ERROR one']
    warnings = []

    # Act
    severity = classify_severity(errors, warnings)

    # Assert
    assert severity == 'média'


def test_build_recommendation_for_migration_error():
    # Arrange
    errors = ['ERROR Migration failed: relation users already exists']
    warnings = []

    # Act
    recommendation = build_recommendation(errors, warnings)

    # Assert
    assert 'migração' in recommendation
    assert 'idempotência' in recommendation


def test_generate_report_uses_final_status_in_markdown(tmp_path):
    # Arrange
    output_path = tmp_path / 'report.md'
    state = {
        'input_path': 'examples/sample_pipeline_error.log',
        'output_path': str(output_path),
        'status': 'log_analyzed',
        'severity': 'alta',
        'summary': 'Resumo do log.',
        'recommendation': 'Recomendação do log.',
        'detected_errors': [],
        'detected_warnings': [],
    }

    # Act
    result = generate_report_node(state)

    # Assert
    report_content = output_path.read_text(encoding='utf-8')
    assert result['status'] == 'report_generated'
    assert '## Status\n\nfinished' in report_content
    assert '## Status\n\nlog_analyzed' not in report_content
