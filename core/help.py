import logging, datetime, sys, requests

# Logger name
log = logging.getLogger("logger")


def create_filename(command, projectid=None):
    """
    Logic to create filename
    """
    log.info("Generating xlsx filename to store the contents")

    # get the current timestamp
    timestamp_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # if there is a projectid, then add the project id on the file
    if projectid is None:
        filename = "{0}_{1}.xlsx".format(command, timestamp_now)
    else: # else just use the below logic to name the file
        filename = "{0}_{1}_{2}.xlsx".format(command, projectid, timestamp_now)

    return filename


def print_progress(iteration, total, prefix='', suffix='', decimals=1, bar_length=100):
    """
    Call in a loop to create terminal progress bar
    :param iteration: - Required  : current iteration (Int)
    :param total: - Required  : total iterations (Int)
    :param prefix: - Optional  : prefix string (Str)
    :param suffix: - Optional  : suffix string (Str)
    :param decimals: - Optional  : positive number of decimals in percent complete (Int)
    :param bar_length: - Optional  : character length of bar (Int)
    :return:
    """
    format_str = "{0:." + str(decimals) + "f}"
    if total == 0:
        total = 1
    percents = format_str.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '#' * filled_length + '-' * (bar_length - filled_length)
    sys.stdout.write('\r%s (%s/%s) |%s| %s%s %s' % (prefix, iteration, total, bar, percents, '%', suffix)),
    sys.stdout.flush()
    if iteration == total:
        sys.stdout.write('\n')
        sys.stdout.flush()


def call_url(url, **kwargs):
    """
    Logic to read the request and pass on the response from the API URL.
    """
    response = None
    try:
        log.debug('Requesting data from the API: {0}'.format(url))

        if kwargs['command'] == 'zendesk':
            response = requests.get(url, auth=(kwargs['username'], kwargs['password']))
        else:
            response = requests.get(url, headers=kwargs['header'])

        if response.status_code != 200:
            log.error("API request Failure: Status code received ({0}), URL ({1})".format(response.status_code,
                                                                                                 url))
    except requests.ConnectionError():
        log.error('API ({0}) Connection error'.format(url))

    finally:

        if kwargs['command'] == 'zendesk':
            return response.json()
        else:
            return response


def zendesk_help_page():
    """
    Zendesk Help page
    """
    return """ Read more on using ZD search here https://developer.zendesk.com/rest_api/docs/help_center/search """


def tracker_help_page():
    """
    Tracker help page
    """

    return """ Read more on using tracker search here https://www.pivotaltracker.com/help/articles/advanced_search/ """