import requests, logging
from datetime import datetime
from core.excel import Excel
from core.help import call_url

# Logger name
log = logging.getLogger("logger")


class TrackerAPI:

    def __init__(self, url, token):
        self.tracker_url = url
        self.token = token

    def create_response_dict(self, project_id, search_string):
        """
        Store house for all the API response from the tracker API
        """

        log.info("Reading Tracker API and recording its responses")

        # Collector & runner
        runner = 1
        offset = 0
        collector = []

        # Loop until we hit the end of the page.
        while runner != "0":

            # Format the URL to place in all the search keywords
            url = self.tracker_url.format(project_id, search_string, offset)
            kwargs = {
                "command": "tracker",
                "header": {'X-TrackerToken': '{0}'.format(self.token)}
            }

            # Call the URL and get the response.
            responses = call_url(url, **kwargs)

            # Loop through the response and collect the
            # information that we are interested in
            for response in responses.json():

                # All the labels store house
                labels = []
                for label_key in response['labels']:
                    labels.append(label_key['name'])

                # If the description is blank, leave them blank
                # so that we dont crap out ..
                if 'description' not in response:
                    response['description'] = ""

                # Store the data in the below format
                data = [
                    response['id'], str(datetime.strptime(response['created_at'], "%Y-%m-%dT%H:%M:%SZ")), response['current_state'],
                    response['name'], response['description'], response['story_type'],
                    str(datetime.strptime(response['updated_at'], "%Y-%m-%dT%H:%M:%SZ")), ",".join(labels), response['url']
                ]

                collector.append(data)

            # CHnage the offset and start to loop again
            offset += 500
            runner = responses.headers['X-Tracker-Pagination-Returned']

        return collector


class Tracker:

    def __init__(self, filename, sheetname, project_id, query, token):
        self.excel = Excel(filename, sheetname)
        self.project_id = project_id
        self.label = query
        self.tracker_url = "https://www.pivotaltracker.com/services/v5/projects/{0}/stories?filter={1}&offset={2}&limit=500"
        self.api = TrackerAPI(self.tracker_url, token)

    def get_api_response(self):
        """
        Pull data from the tracker API
        """
        log.info("Requesting data for the tracker project: {0}, label {1}".format(self.project_id, self.label))
        return self.api.create_response_dict(self.project_id, self.label)

    def TrackerWorkflow(self):
        """
        Tracker Workflow.
        """
        log.info("Starting the tracker workflow to insert into worksheet")

        # Obtain data
        data = self.get_api_response()

        # Create workbook
        workbook, worksheet = self.excel.create_excel()

        # Add excel data
        kwargs = {
            'projectid': self.project_id,
            'url': self.tracker_url,
            'search_string': self.label
        }
        self.excel.add_tracker_excel_contents(worksheet, data, **kwargs)

        # Close the excel workbook
        self.excel.close_excel(workbook)
