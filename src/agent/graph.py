from langgraph.graph import END, START, StateGraph

from src.agent.nodes import (
    analyze_log_node,
    error_response_node,
    final_response_node,
    generate_report_node,
    prepare_context_node,
    read_log_node,
    validate_input_node,
)
from src.agent.state import LogAnalysisState


def should_continue_after_validation(state: LogAnalysisState) -> str:
    if state.get('validation_errors'):
        return 'error'

    return 'continue'


def build_graph():
    graph = StateGraph(LogAnalysisState)

    graph.add_node('validate_input', validate_input_node)
    graph.add_node('read_log', read_log_node)
    graph.add_node('prepare_context', prepare_context_node)
    graph.add_node('analyze_log', analyze_log_node)
    graph.add_node('generate_report', generate_report_node)
    graph.add_node('final_response', final_response_node)
    graph.add_node('error_response', error_response_node)

    graph.add_edge(START, 'validate_input')

    graph.add_conditional_edges(
        'validate_input',
        should_continue_after_validation,
        {
            'continue': 'read_log',
            'error': 'error_response',
        },
    )

    graph.add_conditional_edges(
        'read_log',
        should_continue_after_validation,
        {
            'continue': 'prepare_context',
            'error': 'error_response',
        },
    )

    graph.add_edge('prepare_context', 'analyze_log')
    graph.add_edge('analyze_log', 'generate_report')
    graph.add_edge('generate_report', 'final_response')
    graph.add_edge('final_response', END)
    graph.add_edge('error_response', END)

    return graph.compile()
