
import os
import time
from pprint import pprint
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("API_KEY")
from cruxrequester import CruxRequester


urls = [
    "https://www.thestar.com/",
    "https://www.theglobeandmail.com/",
    "https://www.cbc.ca/",
    "https://nationalpost.com/",
    "https://globalnews.ca/",
    "https://www.ctvnews.ca/",
    "https://www.blogto.com/",
    "https://www.cp24.com/",
    "https://www.sportsnet.ca/",
    "https://www.tsn.ca/"
]



worker = CruxRequester(API_KEY)




