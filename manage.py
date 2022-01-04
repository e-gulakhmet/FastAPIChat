import argparse
import os


def _init_parser():
    parser = argparse.ArgumentParser(prog='FastAPIChat', description='App management')

    parser.add_argument('command', help='Command to execute')

    parser.add_argument('--port', action='store', type=int, default=80, help='Server post')
    parser.add_argument('--host', action='store', type=str, default='0.0.0.0', help='Server host')

    return parser


def run(args: argparse.Namespace):
    port = args.port
    host = args.host
    os.system('pwd')
    os.system(f'sudo uvicorn main:app --reload --workers 1 --host {host} --port {port}')


def main():
    parser = _init_parser()
    args = parser.parse_args()

    globals()[args.command](args)


if __name__ == "__main__":
    main()
