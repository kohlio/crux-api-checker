import csv
import json
import sqlite3

class CruxReporter():
    
    def __init__(self):
        pass

    def generate_csv(self, filename, results):
        with open(filename, "w", newline="") as csvfile:
            fieldnames = [
                "Site",
                "Device",
                "CLS",
                "FID",
                "LCP",
                "FCP",
                "Timestamp"
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for device in ["mobile", "desktop"]:
                for result in results:
                    writer.writerow({
                        "Site": result["origin"],
                        "Device": device,
                        "CLS": result[device]["cls"],
                        "FID": result[device]["fid"],
                        "LCP": result[device]["lcp"],
                        "FCP": result[device]["fcp"],
                        "Timestamp": result["timestamp"]
                    })
        print(f"Results written to {filename}.\n")

    def generate_json(self, filename, results):
        with open(filename, "w") as f:
            json.dump(results, f, indent=4)
        print(f"Results written to {filename}.\n")
    
    def add_to_sqlite(self, dbname, results):
        conn = sqlite3.connect(dbname)
        cursor = conn.cursor()
        sql = (
            f"CREATE TABLE IF NOT EXISTS core_web_vitals ("
            f"timestamp VARCHAR(50),"
            f"site VARCHAR(250),"
            f"device VARCHAR(10),"
            f"cls VARCHAR(10),"
            f"fid INT,"
            f"lcp INT,"
            f"fcp INT"
            f")"
        )
        cursor.execute(sql)
        for device_type in ["mobile", "desktop"]:
            for result in results:
                site = result["origin"]
                cls = result[device_type]["cls"]
                fid = result[device_type]["fid"]
                lcp = result[device_type]["lcp"]
                fcp = result[device_type]["fcp"]
                timestamp = result["timestamp"]
                sql = (
                    f"INSERT INTO core_web_vitals (site, device, cls, fid, lcp, fcp, timestamp) "
                    f"VALUES ('{site}','{device_type}',{cls},{fid},{lcp},{fcp},'{timestamp}');"
                )
                cursor.execute(sql)
        conn.commit()
        conn.close()

    


   