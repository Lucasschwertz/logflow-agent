from src.agent.state import LogAnalysisState
from src.security.validators import validate_log_content, validate_log_path
from src.tools.file_tools import read_text_file, write_text_file
from src.tools.log_tools import (
    build_recommendation,
    build_summary,
    classify_severity,
    extract_error_lines,
    extract_warning_lines,
    sanitize_sensitive_data,
)


def validate_input_node(state: LogAnalysisState) -> LogAnalysisState:
    errors = validate_log_path(state.get('input_path', ''))

    if errors:
        return {
            'validation_errors': errors,
            'status': 'invalid_input',
        }

    return {
        'validation_errors': [],
        'status': 'input_validated',
    }


def read_log_node(state: LogAnalysisState) -> LogAnalysisState:
    raw_log = read_text_file(state['input_path'])
    errors = validate_log_content(raw_log)

    if errors:
        return {
            'raw_log': raw_log,
            'validation_errors': errors,
            'status': 'invalid_content',
        }

    return {
        'raw_log': raw_log,
        'status': 'log_loaded',
    }


def prepare_context_node(state: LogAnalysisState) -> LogAnalysisState:
    sanitized_log = sanitize_sensitive_data(state['raw_log'])

    return {
        'sanitized_log': sanitized_log,
        'status': 'context_prepared',
    }


def analyze_log_node(state: LogAnalysisState) -> LogAnalysisState:
    sanitized_log = state['sanitized_log']
    errors = extract_error_lines(sanitized_log)
    warnings = extract_warning_lines(sanitized_log)
    severity = classify_severity(errors, warnings)
    summary = build_summary(errors, warnings, severity)
    recommendation = build_recommendation(errors, warnings)

    return {
        'detected_errors': errors,
        'detected_warnings': warnings,
        'severity': severity,
        'summary': summary,
        'recommendation': recommendation,
        'status': 'log_analyzed',
    }


def generate_report_node(state: LogAnalysisState) -> LogAnalysisState:
    report_content = f'''# Relatório LogFlow Agent

## Arquivo analisado

{state['input_path']}

## Status

{state['status']}

## Severidade

{state['severity']}

## Resumo

{state['summary']}

## Erros detectados

{_format_items(state.get('detected_errors', []))}

## Avisos detectados

{_format_items(state.get('detected_warnings', []))}

## Recomendação

{state['recommendation']}

## Observação de segurança

Dados sensíveis identificados por padrões simples foram mascarados quando encontrados.
'''

    output_path = state.get('output_path') or 'outputs/logflow-report.md'
    report_path = write_text_file(output_path, report_content)

    return {
        'report_content': report_content,
        'report_path': report_path,
        'status': 'report_generated',
    }


def final_response_node(state: LogAnalysisState) -> LogAnalysisState:
    return {
        'status': 'finished',
    }


def error_response_node(state: LogAnalysisState) -> LogAnalysisState:
    return {
        'summary': 'A execução foi interrompida por erro de validação.',
        'recommendation': 'Corrija os dados de entrada e execute novamente.',
        'status': 'validation_failed',
    }


def _format_items(items: list[str]) -> str:
    if not items:
        return '- Nenhum item encontrado.'

    return ''.join(f'- {item}\n' for item in items)
