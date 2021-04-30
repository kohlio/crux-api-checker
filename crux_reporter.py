import csv
import json
import sqlite3
from datetime import datetime
import mysql.connector as mysql

class CruxReporter():
    
    def __init__(self):
        self.timestamp = datetime.isoformat(datetime.now())

    def generate_csv(self, filename, results):
        with open(filename, "w", newline="") as csvfile:
            fieldnames = [
                "Page",
                "Device",
                "LCP",
                "FID",
                "CLS",
                "Result Type",
                "Timestamp"
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({
                "LCP": "Target less than 2500ms",
                "FID": "Target less than 100ms",
                "CLS": "Target less than 0.1"
            })
            for result in results:
                writer.writerow({
                    "Page": result["page"],
                    "Device": result["device"],
                    "LCP": result["lcp"],
                    "FID": result["fid"],
                    "CLS": result["cls"],
                    "Result Type": result["result_type"],
                    "Timestamp": self.timestamp
                })
        print(f"\nResults written to {filename}.\n")

    def generate_json(self, filename, results):
        for result in results:
            result["Timestamp"] = self.timestamp
        with open(filename, "w") as f:
            json.dump(results, f, indent=4)
        print(f"\nResults written to {filename}.\n")
    
    def add_to_sqlite(self, dbname, results):
        conn = sqlite3.connect(dbname)
        cursor = conn.cursor()
        sql = """CREATE TABLE IF NOT EXISTS core_web_vitals
                (site VARCHAR(250), device VARCHAR(10), cls VARCHAR(10), fid INT, lcp INT, timestamp VARCHAR(50), result_type VARCHAR(25))"""
        cursor.execute(sql)
        for result in results:
            site = result["page"]
            device = result["device"]
            cls = result["cls"]
            fid = result["fid"]
            lcp = result["lcp"]
            result_type = result["result_type"]
            timestamp = self.timestamp
            sql = (
                f"INSERT INTO core_web_vitals (site, device, cls, fid, lcp, timestamp, result_type) "
                f"VALUES ('{site}','{device}',{cls},{fid},{lcp},'{timestamp}', '{result_type}');"
            )
            cursor.execute(sql)
        conn.commit()
        conn.close()
        print(f"\nResults written to {dbname}.\n")
    
    def add_to_remote_mysql(self, endpoint, dbase, user, password, results):
        db_connection = mysql.connect(host=endpoint, database=dbase, user=user, password=password)
        cursor = db_connection.cursor()
        for result in results:
            site = result["page"]
            device = result["device"]
            cls = result["cls"]
            fid = result["fid"]
            lcp = result["lcp"]
            result_type = result["result_type"]
            timestamp = self.timestamp
            sql = (
                f"INSERT INTO core_web_vitals (site, device, cls, fid, lcp, timestamp, result_type) "
                f"VALUES ('{site}','{device}',{cls},{fid},{lcp},'{timestamp}', '{result_type}');"
            )
            cursor.execute(sql)
        db_connection.commit()
        db_connection.close()
        print(f"\nResults sent to remote mysql database.\n")

