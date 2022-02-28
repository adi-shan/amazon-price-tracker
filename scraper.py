import requests
import re
from bs4 import BeautifulSoup

URL = 'https://www.amazon.ca/LG-27GL83A-B-27-Inch-Led-Lit-14700510/dp/B07YGZL8XF/?_encoding=UTF8&pd_rd_w=NjCBf&pf_rd_p=abee655a-f25b-41b9-9f03-635abdfc697d&pf_rd_r=XB9S0PS88K5PVRGB8YJP&pd_rd_r=cce84666-4e32-40b8-b132-fc4fae65cc48&pd_rd_wg=PIHGr&ref_=pd_gw_ci_mcx_mr_hp_atf_m&th=1'
ASIN = re.compile("^https:\/\/www\.amazon\.ca\/(?:.*\/)?dp\/([a-zA-z\d]{10})")
headers = {
    "authority": "www.amazon.com",
    "pragma": "no-cache",
    "cache-control": "no-cache",
    "dnt": "1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "sec-fetch-site": "none",
    "sec-fetch-mode": "navigate",
    "sec-fetch-dest": "document",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
}


page = requests.get(URL, headers=headers)

soup = BeautifulSoup(page.text, 'html.parser')

title = soup.find(id="productTitle")
discount_price = soup.find("div", {"class": "a-price-whole"})
original_price = soup.find("div", {"class": "a-offscreen"})
print(original_price)
print(discount_price)




