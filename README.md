# CrUX API Checker

A python program to fetch the main Core Web Vitals scores for multiple competitor sites from the Chrome User Experience API. The main 75th percentile scores are fetched, rather than full histogram details. Generate reports in JSON, CSV, or Sqlite (if tracking performance over time).

Requires an API key. Get one (https://developers.google.com/web/tools/chrome-user-experience-report/api/guides/getting-started)[here].

### Install

Place `API_KEY=Your_Key` in `.env` file or see help.
```
python3 -m venv ./crux
source crux/bin/activate
pip install -r requirements.txt
```

### Usage

Example `python main.py --site https://www.google.com`

See `python main.py --help`.

```
usage: main.py [-h] [--site SITE] [--sitelist SITELIST] [--apikey APIKEY] [--csv CSV] [--json JSON]
               [--sqlitedb SQLITEDB]

optional arguments:
  -h, --help           show this help message and exit
  --site SITE          specify a single site to fetch CrUX origin stats
  --sitelist SITELIST  specify a file listing one site per line to check multiple origin stats
  --apikey APIKEY      specify CrUX API key if not included as API_KEY in dot env file
  --csv CSV            specify an output filename for csv report
  --json JSON          specify an output filename for json report
  --sqlitedb SQLITEDB  specify an sqlite filename for rolling reporting (eg. via cron job)
```