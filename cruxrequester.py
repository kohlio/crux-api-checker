import requests
import json

class CruxRequester():
    
    def __init__(self, API_KEY):
        self.key = API_KEY
        self.data = {
            "desktop": {},
            "mobile": {}
        }

    def request_origin_crux(self, site, form_factor):
        endpoint = f"https://chromeuxreport.googleapis.com/v1/records:queryRecord?key={self.key}"
        headers = {"Content-Type": "application/json"}
        req_body = {"origin": site, "formFactor": form_factor}
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
    
    def get_site_data(self, site):
        self.data["desktop"] = self.extract_percentiles(
            self.request_origin_crux(site, "DESKTOP")
        )
        self.data["mobile"] = self.extract_percentiles(
            self.request_origin_crux(site, "PHONE")
        )