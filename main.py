import os
import time
from pprint import pprint
from datetime import datetime
from dotenv import load_dotenv
from crux_requester import CruxRequester
from crux_reporter import CruxReporter
from get_args import get_args

def main():

    pages_to_check = []
    
    # Get args, API_KEY and site(s) to check
    args = get_args()
    if args.apikey:
        API_KEY = args.apikey
    else:
        load_dotenv()
        API_KEY = os.getenv("API_KEY")
    if args.site:
        pages_to_check.append({
            "request_type": "origin",
            "page": args.site
        })
    if args.siteslist:
        with open(args.siteslist, "r") as f:
            pages = [line.replace("\n", "") for line in f.readlines()]
            for url in pages:
                pages_to_check.append({
                    "request_type": "origin",
                    "page": url
                })
    if args.url:
        pages_to_check.append({
            "request_type": "url",
            "page": args.url
        })
    if args.urlslist:
        with open(args.urlslist, "r") as f:
            pages = [line.replace("\n", "") for line in f.readlines()]
            for url in pages:
                pages_to_check.append({
                    "request_type": "url",
                    "page": url
                })

    # Use CruxRequester to fetch core web vitals data for each site
    worker = CruxRequester(API_KEY)
    results = []
    worker.get_results(pages_to_check)
    pprint(worker.data)
    # results.append(data)
    # mobile = worker.data["mobile"]
    # desktop = worker.data["desktop"]
    # print(
    #     f"\nCrUX API Core Web Vitals metrics for {page} based on 75th percentile:\n"
    #     f"Data: {data}\n"
    # )
    # results.append({
    #     "page": page,
    #     "mobile": mobile,
    #     "desktop": desktop,
    #     "timestamp": datetime.isoformat(datetime.now())
    # })

    # Write reports if requested
    reporter = CruxReporter()
    if args.csv and len(results) > 0:
        reporter.generate_csv(args.csv, worker.data)
    if args.json and len(results) > 0:
        print('saving json')
        reporter.generate_json(args.json, worker.data)
    if args.sqlitedb and len(results) > 0:
        reporter.add_to_sqlite(args.sqlitedb, worker.data)

main()






