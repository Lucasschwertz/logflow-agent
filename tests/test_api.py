from pathlib import Path

from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


def test_health_returns_ok():
    # Act
    response = client.get('/health')

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        'status': 'ok',
        'service': 'logflow-agent',
    }


def test_analyze_sample_pipeline_error_log_returns_finished_high_severity():
    # Arrange
    sample_path = Path('examples/sample_pipeline_error.log')

    # Act
    with sample_path.open('rb') as log_file:
        response = client.post(
            '/analyze',
            files={'file': ('sample_pipeline_error.log', log_file, 'text/plain')},
        )

    # Assert
    payload = response.json()
    assert response.status_code == 200
    assert payload['status'] == 'finished'
    assert payload['severity'] == 'alta'
    assert payload['validation_errors'] == []
    assert Path(payload['report_path']) == Path('outputs/logflow-report.md')


def test_analyze_rejects_invalid_extension():
    # Act
    response = client.post(
        '/analyze',
        files={'file': ('pipeline.exe', b'ERROR failed', 'application/octet-stream')},
    )

    # Assert
    payload = response.json()
    assert response.status_code == 400
    assert payload['status'] == 'validation_failed'
    assert payload['severity'] is None
    assert payload['validation_errors']
    assert 'Extensão inválida' in payload['validation_errors'][0]
