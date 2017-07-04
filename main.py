import re

import requests
from bs4 import BeautifulSoup
search_engine = 'https://www.google.com.tw/search'
keywords = ['requests save html', 'JavaScript', 'photos', "web script", "automation", 'Python', "news", "weather"]
excludes = ['webcache.googleusercontent.com']

google_re_pattern = r"(/url\?q=)?(https?://[^&]*)(&.*)*"
all_url_set = set()

for keyword in keywords:
    query = {'q': keyword}
    r = requests.get(search_engine, params=query)
    bs = BeautifulSoup(r.text, "lxml")

    for c in  bs.find_all("a"):
        url = c.attrs['href']
        if [e for e in excludes if e in url]:
            continue
        match = re.search(google_re_pattern, url)
        if match:
            try:
                all_url_set.add(match.group(2))
            except Exception:
                continue

print all_url_set, len(all_url_set)

"""
/url?q=https://stackoverflow.com/questions/31126596/saving-response-from-requests-to-file&sa=U&ved=0ahUKEwjAlOqAsO_UAhWIKJQKHXyBCzMQFggTMAA&usg=AFQjCNGaUwPNQPOPgkutjrIpE2i2vVp0Rg
/url?q=http://webcache.googleusercontent.com/search%3Fq%3Dcache:puvo7gMxFy8J:https://stackoverflow.com/questions/31126596/saving-response-from-requests-to-file%252Brequests%2Bsave%2Bhtml%26hl%3Dzh-TW%26ct%3Dclnk&sa=U&ved=0ahUKEwjAlOqAsO_UAhWIKJQKHXyBCzMQIAgWMAA&usg=AFQjCNFjzN0zCx_m0zLMOIsQJTIj22IYLw
"""
