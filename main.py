import os
import time
from pprint import pprint
from datetime import datetime
from dotenv import load_dotenv
from crux_requester import CruxRequester
from crux_reporter import CruxReporter
from get_args import get_args

def main():

    sites_to_check = set()
    
    # Get args, API_KEY and site(s) to check
    args = get_args()
    if args.apikey:
        API_KEY = args.apikey
    else:
        load_dotenv()
        API_KEY = os.getenv("API_KEY")
    if args.site:
        sites_to_check.add(args.site)
    if args.sitelist:
        with open(args.sitelist, "r") as f:
            [sites_to_check.add(line.replace("\n", "")) for line in f.readlines()]
    
    # Use CruxRequester to fetch core web vitals data for each site
    worker = CruxRequester(API_KEY)
    results = []
    for site in list(sites_to_check):
        time.sleep(1)
        worker.get_site_data(site)
        mobile = worker.data["mobile"]
        desktop = worker.data["desktop"]
        print(
            f"\nCrUX API Core Web Vitals metrics for origin {site} based on 75th percentile:\n"
            f"Mobile: {mobile}\n"
            f"Desktop: {desktop}\n"
        )
        results.append({
            "origin": site,
            "mobile": mobile,
            "desktop": desktop,
            "timestamp": datetime.isoformat(datetime.now())
        })
    
    # Write reports if requested
    reporter = CruxReporter()
    if args.csv and len(results) > 0:
        reporter.generate_csv(args.csv, results)
    if args.json and len(results) > 0:
        reporter.generate_json(args.json, results)
    if args.sqlitedb and len(results) > 0:
        reporter.add_to_sqlite(args.sqlitedb, results)

main()






