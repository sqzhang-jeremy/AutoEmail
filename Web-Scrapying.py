from bs4 import BeautifulSoup
import requests

# Start the session
session = requests.session()

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'https://online.immi.gov.au/lusc/login',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6',
    # Requests sorts cookies= alphabetically
    'Cookie': 'LB=629938860.24615.0000; PD-S-SESSION-ID=5Vv70Vb67lWRWYSGnk0fKA==:1_2_1_viexp6-CKoyW7BzSeL9uDusTgmRJ++8ebcPnGVoJRTADGhDP|',
}


# Create the payload
payload = {
    'username':'sqzhang.jeremy@gmail.com', 
    'password':'{}',
    'wc_t': '4f1dfcdc-4298-4109-b081-3ba24ff9d0b7',
    'wc_s': '2',
    'continue': 'x',
    'next': 'lusc/login'
    }

s = session.get("https://online.immi.gov.au/lusc/login")
# Post the payload to the site to log in
s = session.post("https://online.immi.gov.au/lusc/login", data=payload)

# Navigate to the next page and scrape the data
s = session.get('https://online.immi.gov.au/ola/app', headers=headers)

soup = BeautifulSoup(s.content, 'html.parser')
print(soup)

b = soup.find_all(id="MyAppsResultsPanel")
print(b)

website = 'https://online.immi.gov.au'

for a in soup.find_all(id="MyAppsResultsPanel"):
    name = a.find(id="nameHeading_0").text
    flag_url = website + a.find(id="MyAppsResultTab_0_0a0")['src']
    status = a.find('div', "wc-text wc-text-type-emphasised").text
    type = a.find_all('div', "wc-input")[1].text
    Last_updated = a.find(id="rightSidePanel_0_0a0b")['datetime']
    Last_submitted = a.find(id="rightSidePanel_0_1a0b")['datetime']

    print(name)
    print("Flag URL:", flag_url)
    print(status)
    print(type)
    print(Last_updated)
    print(Last_submitted)

print('Well done!')
