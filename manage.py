import argparse
import os


class Commands:
    @staticmethod
    def run(args: argparse.Namespace):
        port = args.port
        host = args.host
        os.system(f'sudo uvicorn main:app --reload --workers 1 --host {host} --port {port}')

    @staticmethod
    def make_migrations(args: argparse.Namespace):
        message = args.message
        assert message, 'Set migration message arg(check help)'
        os.system(f'alembic revision --autogenerate -m "{message}"')

    @staticmethod
    def migrate():
        os.system('alembic upgrade head')


def _init_parser():
    parser = argparse.ArgumentParser(prog='FastAPIChat', description='App management')

    parser.add_argument('command', help='Commands to execute: run, migrate, make_migrations')

    # run command args
    parser.add_argument('--port', action='store', type=int, default=80, help='Server post')
    parser.add_argument('--host', action='store', type=str, default='0.0.0.0', help='Server host')
    # make_migrations command args
    parser.add_argument('--message', action='store', type=str, help='Migration message')

    return parser


def main():
    parser = _init_parser()
    args = parser.parse_args()

    getattr(Commands, args.command)(args)


if __name__ == "__main__":
    main()
