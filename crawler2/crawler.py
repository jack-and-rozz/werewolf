# coding: utf-8
import os, sys, re, time, argparse
from collections import OrderedDict
from pprint import pprint

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import requests
import mojimoji


from common import timewatch


root_url = 'https://ruru-jinro.net'
page_url_template = os.path.join(root_url, "searchresult.jsp?st=%d&sort=NUMBER")
imported_urls_filename = 'imported_urls.txt'

