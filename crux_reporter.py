import csv
import json

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

    


   