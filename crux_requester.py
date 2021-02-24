import requests
import json
import time

class CruxRequester():
    
    def __init__(self, API_KEY):
        self.key = API_KEY
        self.data = []

    def request_page_crux(self, page, form_factor):
        endpoint = f"https://chromeuxreport.googleapis.com/v1/records:queryRecord?key={self.key}"
        headers = {"Content-Type": "application/json"}
        req_body = {}
        if page["request_type"] == "origin":
            req_body = {"origin": page["page"], "formFactor": form_factor}
        if page["request_type"] == "url":
            req_body = {"url": page["page"], "formFactor": form_factor}
        req = requests.post(endpoint, headers=headers, data=json.dumps(req_body))
        if req.status_code == 200:
            return req.json()
        else:
            return None
    
    def extract_percentiles(self, data):
        '''
        Extracts the 75% percentiles for the main metrics.
        '''
        return {
            "fcp": data["record"]["metrics"]["first_contentful_paint"]["percentiles"]["p75"],
            "fid": data["record"]["metrics"]["first_input_delay"]["percentiles"]["p75"],
            "lcp": data["record"]["metrics"]["largest_contentful_paint"]["percentiles"]["p75"],
            "cls": data["record"]["metrics"]["cumulative_layout_shift"]["percentiles"]["p75"]
        }
    
    def get_results(self, pages_to_check):
        for page in pages_to_check:
            for device in ["DESKTOP", "PHONE"]:
                time.sleep(1)
                data = self.request_page_crux(page, device)
                web_vitals = self.extract_percentiles(data)
                result = {
                    "page": page["page"],
                    "result_type": page["request_type"],
                    "device": device.lower().replace("phone", "mobile"),
                    "fid": web_vitals["fid"],
                    "lcp": web_vitals["lcp"],
                    "cls": web_vitals["cls"] 
                }
                self.data.append(result)
