import re
import os
import hashlib
import requests
from bs4 import BeautifulSoup
search_engine = 'https://www.google.com.tw/search'
keywords = ['requests save html',] #['requests save html', 'JavaScript', 'photos', "web script", "automation", 'Python', "news", "weather"]
excludes = ['webcache.googleusercontent.com']

google_re_pattern = r"(/url\?q=)?(https?://[^&]*)(&.*)*"
all_url_set = set()

for keyword in keywords:
    query = {'q': keyword}
    #head = requests.head(search_engine, params=query)
    get = requests.get(search_engine, params=query)
    bs = BeautifulSoup(get.text, "lxml")

    for a in  bs.find_all("a"):
        url = a.attrs['href']
        if [e for e in excludes if e in url]:
            continue
        match = re.search(google_re_pattern, url)
        if match:
            try:
                all_url_set.add(match.group(2))
            except Exception:
                continue

if not os.path.isdir("result"):
    os.makedirs("result")

sha_1 = hashlib.sha1()

for url in all_url_set:
    get = requests.get(url, params=query)
    if "html" not in get.headers['Content-Type']:
        continue
    get.encoding = "utf8"
    print url
    sha_1.update(repr(get.text))
    file_name = sha_1.hexdigest() #url.split("/")[-1] if not url.endswith('/') else url.split("/")[-2]
    file_path = os.path.join("result", file_name+".html")
    with open(file_path, "w") as f:
        f.write(get.text.encode("utf8"))


"""
/url?q=https://stackoverflow.com/questions/31126596/saving-response-from-requests-to-file&sa=U&ved=0ahUKEwjAlOqAsO_UAhWIKJQKHXyBCzMQFggTMAA&usg=AFQjCNGaUwPNQPOPgkutjrIpE2i2vVp0Rg
/url?q=http://webcache.googleusercontent.com/search%3Fq%3Dcache:puvo7gMxFy8J:https://stackoverflow.com/questions/31126596/saving-response-from-requests-to-file%252Brequests%2Bsave%2Bhtml%26hl%3Dzh-TW%26ct%3Dclnk&sa=U&ved=0ahUKEwjAlOqAsO_UAhWIKJQKHXyBCzMQIAgWMAA&usg=AFQjCNFjzN0zCx_m0zLMOIsQJTIj22IYLw
"""
