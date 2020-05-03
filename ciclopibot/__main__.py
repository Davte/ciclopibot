"""Run a local copy of CicloPiBot."""

# Standard library modules
import argparse

# Project modules
from . import bot


def main():
    # Parse command-line arguments
    cli_parser = argparse.ArgumentParser(description=__doc__,
                                         allow_abbrev=False)
    cli_parser.add_argument('--bot_token', '--token', '--t', type=str,
                            default=None,
                            required=False,
                            help='telegram bot token')
    cli_parser.add_argument('--path', type=str,
                            default=None,
                            required=False,
                            help='path where data should be stored')
    cli_parser.add_argument('--log_file_name', '--log', type=str,
                            default=None,
                            required=False,
                            help='file to store full log')
    cli_parser.add_argument('--errors_file_name', '--err', type=str,
                            default=None,
                            required=False,
                            help='file to store error log')
    cli_parser.add_argument('--local_host', '--host', type=str,
                            default=None,
                            required=False,
                            help='local host address for linked web-app')
    cli_parser.add_argument('--port', type=int,
                            default=None,
                            required=False,
                            help='local host port for linked web-app')
    cli_parser.add_argument('--hostname', type=str,
                            default=None,
                            required=False,
                            help='host name for webhooks')
    cli_parser.add_argument('--certificate', type=str,
                            default=None,
                            required=False,
                            help='certificate for webhooks')
    cli_arguments = vars(cli_parser.parse_args())
    bot.main(
        **cli_arguments
    )


if __name__ == '__main__':
    main()
