import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--site",
        type=str,
        help="specify a single site to fetch CrUX origin stats"
    )
    parser.add_argument(
        "--siteslist",
        type=str,
        help="specify a file listing one site per line to check multiple origin stats"
    )
    parser.add_argument(
        "--url",
        type=str,
        help="specify a single site to fetch CrUX url stats"
    )
    parser.add_argument(
        "--urlslist",
        type=str,
        help="specify a file listing one url per line to check multiple url stats"
    )
    parser.add_argument(
        "--apikey",
        type=str,
        help="specify CrUX API key if not included as API_KEY in dot env file"
    )
    parser.add_argument(
        "--csv",
        type=str,
        help="specify an output filename for csv report"
    )
    parser.add_argument(
        "--json",
        type=str,
        help="specify an output filename for json report"
    )
    parser.add_argument(
        "--sqlitedb",
        type=str,
        help="specify an sqlite filename for rolling reporting (eg. via cron job)"
    )
    parser.add_argument(
        "--mysql",
        action='store_true',
        help="insert results to remote mysql with credentials from dot env file"
    )
    args = parser.parse_args()
    return args