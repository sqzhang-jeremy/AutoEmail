# encoding: utf-8
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import smtplib, ssl
import datetime, time

from bs4 import BeautifulSoup

import requests

def Get_visa_info():
        
    cookies = {
        'LB': '629938860.24615.0000',
        'PD-S-SESSION-ID': '5Vv70Vb67lWRWYSGnk0fKA==:1_2_1_vdnORUSekwjhvLWAtWhE2d4aU+ClGKFsd9oPZtuJPRqOF+AI|',
    }
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
    # 'Cookie': 'LB=629938860.24615.0000; PD-S-SESSION-ID=5Vv70Vb67lWRWYSGnk0fKA==:1_2_1_vdnORUSekwjhvLWAtWhE2d4aU+ClGKFsd9oPZtuJPRqOF+AI|',
    }

    response = requests.get('https://online.immi.gov.au/ola/app', cookies=cookies, headers=headers)

    soup = BeautifulSoup(response.content, 'html.parser')
    print(soup)

    b = soup.find_all(id="MyAppsResultsPanel")
    print(b)

    website = 'https://online.immi.gov.au'

    app_name = []
    app_status = []
    app_type = []
    app_Last_updated = []

    for a in soup.find_all(id="MyAppsResultsPanel"):
        name = a.find(id="nameHeading_0").text
        flag_url = website + a.find(id="MyAppsResultTab_0_0a0")['src']
        status = a.find('div', "wc-text wc-text-type-emphasised").text
        type = a.find_all('div', "wc-input")[1].text
        Last_updated = a.find(id="rightSidePanel_0_0a0b")['datetime']
        Last_submitted = a.find(id="rightSidePanel_0_1a0b")['datetime']

        app_name = name
        app_status = status
        app_type = type
        app_Last_updated = Last_updated

    print('Well done!')

    return app_name, app_status, app_type, app_Last_updated





def Schedule_email():
    #set the timezone
    os.environ['TZ'] = 'Asia/Shanghai'
    time.tzset()

    # calculate time
    submitted_day = datetime.datetime(2022, 7, 29, 13, 30)
    today = datetime.datetime.now()
    time_diff = today - submitted_day
    loading_month = time_diff.seconds//(60*60*24*31)
    loading_day = time_diff.days
    loading_hour = time_diff.seconds//(60*60)
    loading_min = (time_diff.seconds//60) - (loading_hour*60)
    date = time.strftime("%Y.%m.%d", time.localtime()) 


    # mail info
    sender_email = "sqzhang.jeremy@gmail.com"  # Enter your address
    receiver_email = "zhangshiquan97@qq.com"   # Enter receiver address
    password = '{}' # allowed password. if you use gmail, you should go to your google accout and generate secury password

    # text message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg["To"] = receiver_email
    msg['Subject'] = "Visa Application Loading-Day %d"%loading_day

    app_name, app_status, app_type, app_Last_updated = Get_visa_info()

    language = 'en'
    # language mode
    if language == 'en':
        name = 'Bro'
        text = 'Visa application is loading'
        start = 'from'
        start_stop = '.'
        blessing1 = 'Please keep patient! Everything will be fine:)'
        blessing2 = 'Good Luck!'
        alert = 'Please do not reply to this email as it is auto-generated via Google Cloud.'
    elif language == 'cn':
        name = u"老大"
        text = u"签证提交申请已经过去"
        start = u"距离正式提交申请"
        start_stop = u"。"
        blessing1 = u"请继续耐心等待，好事多磨:)"
        blessing2 = u"祝好！"
        alert = u"请不要回复这封由谷歌云自动生成的邮件。"

    htmlEmail = """\
    <p> Hi {name},<br><br>
        Visa name: {app_name}<br>
        Visa status: {app_status}<br>
        Visa type: {app_type}<br>
        Visa last updated: {app_Last_updated}<br><br>
        {text} {mn} months {days} days {hrs} hours {mins} mins {start} 2022.07.29 13:30{start_stop}
    </p><br>
        {blessing1} <br><br>
        {blessing2} <br>
        {date} <br><br>
        <font color="red">{alert} </font>
    """.format(name=name, text=text, mn=loading_month, days=loading_day, hrs=loading_hour, mins=loading_min,\
    start=start, start_stop=start_stop, blessing1=blessing1, blessing2=blessing2, date=date, alert=alert,\
    app_name= app_name, app_status=app_status, app_type=app_type, app_Last_updated=app_Last_updated)

    msg.attach(MIMEText(htmlEmail, 'html'))
    print(msg.as_string())

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port=465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())




Schedule_email()