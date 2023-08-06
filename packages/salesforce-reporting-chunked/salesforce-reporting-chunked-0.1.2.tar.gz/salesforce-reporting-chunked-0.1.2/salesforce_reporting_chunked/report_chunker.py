from collections import OrderedDict
from salesforce_reporting_chunked import Chunky, ReportParser

def chunk_report_by_date(config, report_id, fieldnames, date_fieldname, start_date, end_date, day_increment=1):
    """
    Expects:
        config (dict) Dictonary containing username, password, security_token and api_version.
        report_id (str) Salesforce report id.
        fieldnames (list)   Columns from Salesforce report.
        date_fieldname (str)    Name of sortable date fieldname used to get incremental chunks of report.
        start_date (str)    iso-formatted date string
        end_date (str)    iso-formatted date string
        day_increment (int) Number of days in an incremental chunk.
    Yields: (OrdereDict)    Report row value as a python OrderdDict object.
    """

    sf = Chunky(**config)

    chunks = sf.get_daterange_chunked_report(
            report_id,
            date_fieldname=date_fieldname,
            start_date=start_date,
            end_date=end_date,
            day_increment=day_increment,
        )

    while True:
        try:
            parser = ReportParser(next(chunks))
            for line in parser.records():
                yield OrderedDict([(k, v) for k, v in zip(fieldnames, line)])
        except StopIteration:
            break
