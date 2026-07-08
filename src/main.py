import argparse
import json

from src.agent.graph import build_graph


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='LogFlow Agent: agente LangGraph para análise de logs de pipeline.'
    )
    parser.add_argument(
        'input_path',
        help='Caminho do arquivo .log ou .txt que será analisado.',
    )
    parser.add_argument(
        '--output',
        default='outputs/logflow-report.md',
        help='Caminho do relatório gerado.',
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    app = build_graph()

    result = app.invoke(
        {
            'input_path': args.input_path,
            'output_path': args.output,
        }
    )

    response = {
        'status': result.get('status'),
        'severity': result.get('severity'),
        'summary': result.get('summary'),
        'recommendation': result.get('recommendation'),
        'report_path': result.get('report_path'),
        'validation_errors': result.get('validation_errors', []),
    }

    print(json.dumps(response, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
