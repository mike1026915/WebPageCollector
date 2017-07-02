import requests
from bs4 import BeautifulSoup
search_engine = 'https://www.google.com.tw/search'
keyword = ['requests save html']

query = {'q': 'requests save html'}

r = requests.get(search_engine, params=query)
bs = BeautifulSoup(r.text)
