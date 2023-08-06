# Salesforce Reporting - Chunk Style

Get > 2000 rows from your date-sortable Salesforce reports via python using the [Analytics API](https://resources.docs.salesforce.com/sfdc/pdf/salesforce_analytics_rest_api.pdf) (pdf link), by `salesforce-reporting` and some date-trickery.

`salesforce-reporting-chunks` is a wrapper around [cghall](https://pypi.org/user/cghall/)'s `salesforce-reporting` module. The Salesforce API limits output to 2000 rows for a given report. `salesforce-reporting-chunks` works around this by returning a generator that simply pulls a date range from your report a given number of days at a time.

## Install
```pip install force-retrieve-chunked```

## Usage

```python
from salesforce_reporting_chunked import chunk_report_by_date

CONFIG = {
    "security_token": "REPLACE WITH YOUR TOKEN",
    "username": "REPLACE WITH YOUR USERNAME",
    "password": "REPLACE WITH YOUR PASSWORD",
    "api_version": "v38.0"
}

FIELDNAMES = [
    "First Name",
    "Last Name",
    "Date Column", # this is the magic column use for chunking.
    "Corhuscorrated Plethanth",
    "Other Column",
]

REPORT_ID = "YOURREPORTID"

>>> data = chunk_report_by_date(
    CONFIG,
    REPORT_ID,
    FIELDNAMES,
    date_fieldname="Date Column",
    start_date="2018-01-01",
    start_date="2019-01-31",
)
>>> next(data)
OrderedDict([('First Name', 'Fred'),('Last Name', 'Garvin'),('DATE_COLUMN_NAME', '2018-01-01'),('Corhuscorrated Plethanth', True),('Other Column': 'Yep. Another')])
```
