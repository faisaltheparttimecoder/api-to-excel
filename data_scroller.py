import logging, sys, os
from core.init_log import init_logging
from core.argparser import parserags
from core.help import create_filename
from zendesk.zd import ZendeskHC
from tracker.tracker import Tracker

# Logger name
log = logging.getLogger("logger")

if __name__ == "__main__":

    # Parse the command line arguments
    cmdline_args = parserags(sys.argv[1:])

    # First Initialize the logging module
    if cmdline_args.debug:
        init_logging(logging.DEBUG)
    else:
        init_logging(logging.INFO)

    # Get filename
    sheetname = cmdline_args.sheet_name

    log.info("Starting the program to pull all data from {0}".format(cmdline_args.command))

    # Call program based on the program command called.
    filename = None
    if cmdline_args.command == 'tracker':  # If tracker
        filename = create_filename(cmdline_args.command, cmdline_args.project_id)
        tracker = Tracker(filename, sheetname, cmdline_args.project_id, cmdline_args.query_string, cmdline_args.tracker_token)
        tracker.TrackerWorkflow()
    elif cmdline_args.command == 'zendesk':  # If zendesk
        filename = create_filename(cmdline_args.command)
        zendesk = ZendeskHC(filename, sheetname, cmdline_args.zd_username, cmdline_args.zd_password, cmdline_args.zd_endpoint, cmdline_args.query_string)
        zendesk.ZendeskWorkflow()
    else:  # It will never reach here since argparse will not anyways allow.
        log.error("Invalid option specified on the command line arguments")

    # Success message
    current_loc_filename = os.getcwd() + "/" + filename
    log.info("The program has successfully completed, the data is stored on location: {0}".format(current_loc_filename))