import xlsxwriter, logging
from datetime import datetime

# Logger name
log = logging.getLogger("logger")


class Excel:

    def __init__(self, filename, sheetname):
        self.filename = filename
        self.sheetname = sheetname
        self.bold = None

    def create_excel(self):
        """
        Create a excel workbook and a worksheet
        """
        log.info("Initializing Excel Workbook & Work Sheet")

        # Create an new Excel file and add a worksheet.
        workbook = xlsxwriter.Workbook(self.filename, {'strings_to_urls': False})
        worksheet = workbook.add_worksheet(self.sheetname)

        # Text formatting
        self.bold = workbook.add_format({'bold': True})

        return workbook, worksheet

    def add_tracker_excel_contents(self, worksheet, data, **kwargs):
        """
        Below functions take care of how the content in the excel
        would be written for tracker API pull
        """
        log.info("Adding Tracker Worksheet contents")

        # Widen the first column to make the text clearer.
        worksheet.set_column('B:D', 20)
        worksheet.set_column('E:F', 40)
        worksheet.set_column('C:I', 20)

        # Total results obtained.
        total_data = len(data)

        # Sheet Metadata Heading
        worksheet.write('B2', 'ProjectID:', self.bold)
        worksheet.write('B3', 'API URL:', self.bold)
        worksheet.write('B4', 'Search String:', self.bold)
        worksheet.write('B5', 'Report date:', self.bold)

        # Sheet Metadata
        worksheet.write('C2', kwargs['projectid'])
        worksheet.write('C3', kwargs['url'])
        worksheet.write('C4', kwargs['search_string'])
        worksheet.write('C5', str(datetime.now()))

        # Add table column heading
        worksheet.add_table('B7:I' + str(total_data), {
            'style': 'Table Style Light 11',
            'columns': [
                {'header': 'Tracker ID'},
                {'header': 'Created at'},
                {'header': 'Current State'},
                {'header': 'Name'},
                {'header': 'Description'},
                {'header': 'Story Type'},
                {'header': 'Updated at'},
                {'header': 'Labels'},

            ]
        })

        # Start to add table data
        position = 8
        for i in data:
            worksheet.write_row('B' + str(position), i)
            worksheet.write_url('B' + str(position), str(i[-1]), string=str(i[0]))
            worksheet.set_column('J:J', None, None, {'hidden': True})
            position += 1

    def add_zendesk_content_data(self, worksheet, data, **kwargs):
        """
        Below functions take care of how the content in the excel
        would be written for Zendesk API pull
        """
        log.info("Adding zendesk Worksheet contents")

        # Widen the first column to make the text clearer.
        worksheet.set_column('B:B', 20)
        worksheet.set_column('C:C', 40)
        worksheet.set_column('D:H', 20)

        # Total results obtained.
        total_data = len(data)

        # Sheet Metadata Heading
        worksheet.write('B2', 'Endpoint:', self.bold)
        worksheet.write('B3', 'API URL:', self.bold)
        worksheet.write('B4', 'Username:', self.bold)
        worksheet.write('B5', 'Query String:', self.bold)
        worksheet.write('B6', 'Report date:', self.bold)

        # Sheet Metadata
        worksheet.write('C2', kwargs['endpoint'])
        worksheet.write('C3', kwargs['url'])
        worksheet.write('C4', kwargs['username'])
        worksheet.write('C5', kwargs['search_string'])
        worksheet.write('C6', str(datetime.now()))

        # Add table contents
        worksheet.add_table('B8:I' + str(total_data), {
            'style': 'Table Style Light 11',
            'columns': [
                {'header': 'Article ID'},
                {'header': 'Description'},
                {'header': 'Section'},
                {'header': 'Draft'},
                {'header': 'Created at'},
                {'header': 'Updated at'},
                {'header': 'Label'},
            ]
        })

        position = 9
        for i in data:
            worksheet.write_row('B' + str(position), i)
            worksheet.write_url('B' + str(position), str(i[-1]), string=str(i[0]))
            worksheet.set_column('I:I', None, None, {'hidden': True})
            position += 1

    def close_excel(self, workbook):
        """
        Once everything is done, close the workbook
        """

        log.info("Data insertion complete, closing the workbook")

        # Insert an image.
        workbook.close()