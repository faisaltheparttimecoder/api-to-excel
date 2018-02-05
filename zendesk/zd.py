import logging
from datetime import datetime
from core.excel import Excel
from core.help import print_progress, call_url

# Logger name
log = logging.getLogger("logger")


class ZendeskAPI:

    # Initialize all the Zendesk API request
    def __init__(self, url, username, password):
        self.zd_hc_search_api = url
        self.username = username
        self.password = password
        self.kwargs = {
            'command': 'zendesk',
            'username': self.username,
            'password': self.password
        }

    def zd_sections(self, sections_url):
        """
        Loop through the sections URL to get all the KB sections
        """
        log.info("Reading zendesk help center API for all KB sections")

        # Initializing the search runners & page number.
        runner = 1
        page = 1

        # Store house for the responses
        collector = {}

        # Loop till we hit at the end of the page
        while runner != 0:
            url = sections_url.format(page)
            responses = call_url(url, **self.kwargs)
            total_request = responses['page_count']

            # Disable progress bar if the debug level is turned on.
            if log.level != 10:
                print_progress(
                        page,
                        total_request,
                        prefix='Loading sections page (current/total):',
                        suffix='Done',
                        bar_length=50
                )

            # Just collect the information that we are interested in
            for response in responses['sections']:
                collector[str(response['id'])] = response['name']

            # Until the page looper doesn't return none, we will try collect all information
            if responses['next_page'] is None:
                runner = 0
            else:
                page += 1

        return collector

    def zd_search(self, search_string, sections):
        """
        Loop through the Zendesk Help Center API to extract the KB's with the search word
        """
        log.info("Reading zendesk help center API for all KB's with search word: {0}".format(search_string))

        # Initializing the search runners & page number.
        runner = 1
        page = 1

        # Store house for the responses
        collector = []

        # Loop until we hit at the end of the page.
        while runner != 0:
            url = self.zd_hc_search_api.format(search_string, page)
            responses = call_url(url, **self.kwargs)
            results = responses['results']
            total_request = responses['page_count']

            # Disable progress bar if the debug level is turned on.
            if log.level != 10:
                print_progress(
                        page,
                        total_request,
                        prefix='Loading search page (current/total):',
                        suffix='Done',
                        bar_length=50
                )

            for result in results:

                # Get the section name
                if str(result['section_id']) in sections:
                    section_name = sections[str(result['section_id'])]
                else:
                    section_name = str(result['section_id'])

                # Store the data in this format to write to the excel
                data = [
                    result['id'],
                    result['name'], section_name, result['draft'],
                    str(datetime.strptime(result['created_at'], "%Y-%m-%dT%H:%M:%SZ")),
                    str(datetime.strptime(result['updated_at'], "%Y-%m-%dT%H:%M:%SZ")),
                    ",".join(result['label_names']), result['html_url']
                ]
                collector.append(data)

            # Until the page looper doesn't return none, we will try collect all information
            if responses['next_page'] is None:
                runner = 0
            else:
                page += 1

        return collector


class ZendeskHC:

    def __init__(self, filename, sheetname, username, password, endpoint, query):
        self.excel = Excel(filename, sheetname)
        self.zd_endpoint = endpoint
        self.zd_hc_search_api = self.zd_endpoint + "/api/v2/help_center/articles/search.json?query={0}&page={1}"
        self.zd_sections_api = self.zd_endpoint + "/api/v2/help_center/en-us/sections.json?page={0}"
        self.username = username
        self.api = ZendeskAPI(self.zd_hc_search_api, self.username, password)
        self.search_string = query

    def get_api_response(self, sections):
        """
        Obtain all the responses from the Zendesk API
        """
        log.info("Reading all the zendesk sections")
        return self.api.zd_search(self.search_string, sections)

    def ZendeskWorkflow(self):
        """
        The workflow to store the data to excel
        """
        log.info("Starting the zendesk workflow to insert into worksheet")

        # Get all the KB sections
        sections = self.api.zd_sections(self.zd_sections_api)

        # Get all the data
        data = self.get_api_response(sections)

        # Create a excel workbook and worksheet
        workbook, worksheet = self.excel.create_excel()

        # Add data to the excel sheet
        kwargs = {
            'endpoint': self.zd_endpoint,
            'url': self.zd_hc_search_api,
            'username': self.username,
            'search_string': self.search_string
        }
        self.excel.add_zendesk_content_data(worksheet, data, **kwargs)

        # Close the sheet
        self.excel.close_excel(workbook)
