import argparse, logging
from core.version import version
from core.help import tracker_help_page, zendesk_help_page

# Logger name
log = logging.getLogger("logger")


def parserags(args):
    """
    Parse command line arguments
    """
    # Global Parameter
    parser = argparse.ArgumentParser(prog='data_scroller',
                                     description='This tool aims to help automating backing up '
                                                 'data from Pivotal Tracker & Zendesk Articles to excel, '
                                                 'which is helpful for generating report on known issues '
                                                 'for a particular version',
                                     epilog='Source code available at https://github.com/faisaltheparttimecoder/api-to-excel',
                                     add_help=False)
    parser.add_argument('-?', '--help', action='help', help='Prints this message')
    parser.add_argument('-v', '--version', action='version', version=' %(prog)s version: ' + version())

    # Help Menu
    shared_parser = argparse.ArgumentParser(add_help=False)

    # Add sub parser commands.
    subparsers = parser.add_subparsers(dest='command')

    # Tracker specific options
    tracker_parser = subparsers.add_parser('tracker', parents=[shared_parser],
                                          help='Pull data from pivotal tracker')
    tracker_parser.add_argument('-p', '--projectid', action='store', dest='project_id',
                                      help='Projected the pivotal tracker project id', required=True)
    tracker_parser.add_argument('-q', '--query', action='store', dest='query_string', help=tracker_help_page())
    tracker_parser.add_argument('-s', '--sheetname', action='store', dest='sheet_name', default='tracker', help='Sheet name to be used')
    tracker_parser.add_argument('-t', '--token', action='store', dest='tracker_token',
                                      help='Provide the Pivotal Tracker token', required=True)
    tracker_parser.add_argument('-d', '--debug', action='store_true', help='Enables debug logging')

    # Zendesk specific options
    zendesk_parser = subparsers.add_parser('zendesk', parents=[shared_parser],
                                           help='Pull data from zendesk help center')
    zendesk_parser.add_argument('-u', '--username', action='store', dest='zd_username', required=True,
                                help='Zendesk username')
    zendesk_parser.add_argument('-p', '--password', action='store', dest='zd_password', required=True,
                                help='Zendesk password')
    zendesk_parser.add_argument('-e', '--endpoint', action='store', dest='zd_endpoint', required=True,
                                help='Zendesk API endpoint')
    zendesk_parser.add_argument('-q', '--query', action='store', dest='query_string',
                                help=zendesk_help_page())
    zendesk_parser.add_argument('-s', '--sheetname', action='store', dest='sheet_name', default='zendesk',
                                help='Sheet name to be used')
    zendesk_parser.add_argument('-d', '--debug', action='store_true', help='Enables debug logging')

    # Parse all the command line arguments and send it to the main functions
    options_object = parser.parse_args(args)

    return options_object