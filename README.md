# Introduction [![Python Version](https://img.shields.io/badge/Python-v3.5-green.svg?style=flat-square)](https://www.python.org/downloads/release/python-355/)  [![License](https://img.shields.io/badge/License-MIT-red.svg?style=flat-square)](https://github.com/faisaltheparttimecoder/DataScroller/blob/master/LICENSE)

Basic python script that uses the search API of pivotal tracker and zendesk help center to pull data and store them to excel.

# How to use it

+ Install Python 3.5
+ Install all the requirements using ```pip install -r requirements.txt```
+ To pull data from tracker use the command like below

```
python data_scroller.py tracker -p <project-id> -q <search-string> -t <tracker token>
```

+ To pull data from zendesk use the command like below

```
python data_scroller.py zendesk -u <zd username> -p <zd password> -q <query string> -e <zd-endpoint>
```

# Example

### Tracker

+ To pull all data with label 2.0

```
python data_scroller.py tracker -p <project-id> -q label:2.0 -t <tracker token>
```

+ To pull data for all stories created since 11/16/2017

```
python data_scroller.py tracker -p <project-id> -q created_since:11/16/2017 -t <tracker token>
```

### Zendesk

+ To pull all data with keyword 2.0

```
python data_scroller.py zendesk -u <zd username> -p <zd password> -q 2.0 -e <zd-endpoint>
```

+ To pull all data with keyword 2.0 which is updated after 2014-01-01 and before 2014-02-01

```
python data_scroller.py zendesk -u <zd username> -p <zd password> -q "2.0&updated_after=2014-01-01&updated_before=2014-02-01" -e <zd-endpoint>
```

# More information

+ For more information on Zendesk search keywords, refer to the [link](https://developer.zendesk.com/rest_api/docs/help_center/search)
+ For more information on Tracker search keywords, refer to the [link](https://www.pivotaltracker.com/help/articles/advanced_search/)