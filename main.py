import gspread
from twitter import *
import schedule
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import math
import pandas as pd
import os
import time
import plotly.graph_objects as go
import config
from plotly.colors import n_colors
from plotly.subplots import make_subplots
import asyncio
from pyppeteer import launch
from PIL import Image

# Import keys
consumer_key = config.consumer_key
consumer_secret = config.consumer_secret
token = config.token
token_secret = config.token_secret

# Initialize with keys
gc = gspread.service_account('credentials.json')
t = Twitter(
    auth=OAuth(token, token_secret, consumer_key, consumer_secret))
t.statuses.home_timeline()

# Open the worksheets on Gspread
wks = gc.open("Valuations").worksheet("Worksheet")
wksStore = gc.open("Valuations").worksheet("Stats")
wksAlgo = gc.open("Valuations").worksheet("Algorithm")

######################## Daily sector buyscore alert ###############################

# Convert the html from plotly to an image file
async def converter():
    browser = await launch()
    page = await browser.newPage()
    await page.goto(config.fig_path)
    await page.screenshot({'path': 'fig1.png', 'fullPage': 'true'})
    await browser.close()

# Use plotly to make a gauge table representing buyscores
def buyscores():
    fig = make_subplots(rows=2, cols=5, start_cell="bottom-left", specs=[[{"type": "domain"}, {"type": "domain"}, {"type": "domain"}, {
                        "type": "domain"}, {"type": "domain"}], [{"type": "domain"}, {"type": "domain"}, {"type": "domain"}, {"type": "domain"}, {"type": "domain"}]])
    sector_list = wks.get('B1:K1')
    buy_score = wks.get('B5:K5')
    obuy_score = wksStore.get('B13:K13')
    x = list(range(0, 10))
    yY = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5]
    xX = [1, 2, 1, 2, 1, 2, 1, 2, 1, 2]
    for i in x:
        value = float(buy_score[0][i])
        NumX = xX[i]
        NumY = yY[i]

        fig.append_trace(go.Indicator(
            mode="gauge+number+delta",
            value=value,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': f"{sector_list[0][i]}", 'font': {'size': 24}},
            delta={'reference': float(obuy_score[0][i]), 'increasing': {
                'color': "green"}},
            gauge={
                'axis': {'range': [None, 20], 'tickwidth': 1, 'tickcolor': "black"},
                'bar': {'color': "black"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 5], 'color': 'red'},
                    {'range': [5, 15], 'color': 'orange'},
                    {'range': [15, 20], 'color': 'green'}],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 20}}), row=NumX, col=NumY)
    fig.update_layout(paper_bgcolor="white", font={
                      'color': "black", 'family': "Arial"}, height=700, width=2000, title_text="Buyscores (Higher = better)")
    fig.write_html("fig.html")
    # Convert the html to an image and upload to twitter
    asyncio.get_event_loop().run_until_complete(converter())
    wksStore.update('B13:K13', buy_score)
    with open("fig1.png", "rb") as imagefile:
        imagedata = imagefile.read()
    t_upload = Twitter(domain='upload.twitter.com',
                       auth=OAuth(token, token_secret, consumer_key, consumer_secret))
    id_img1 = t_upload.media.upload(media=imagedata)["media_id_string"]
    t.statuses.update(status="Today's Buyscores",
                      media_ids=",".join([id_img1]))
    os.remove('fig1.png')
    print("Image Posted")

######################## Sector change alerts ###############################

# Post a graph about the sectors that have changed in valuation
def valuealert():
    current_vals = wksStore.get('B8:L8')
    current_vals = current_vals[0]
    current_pes = wksAlgo.get('A2:AE2')
    current_pes = current_pes[0]
    current_pes = current_pes[3::3]
    stored_pes = wksStore.get('B9:L9')
    stored_pes = stored_pes[0]

    x = list(range(0, 9))
    changed = []
    changedold = []
    changednew = []
    storeToChange = {"Industrials": 'B9', "Basic Materials": 'C9', "Consumer Cyclical": 'D9', "Financial Services": 'E9',
                     'Consumer Defensive': 'F9', "Healthcare": 'G9', "Technology": 'H9', "Utilities": 'I9', "Energy": 'J9', "Communication Services": 'K9'}
    print(x)
    for nums in x:
        if current_pes[nums] != stored_pes[nums]:
            changed.append(current_vals[nums])
            changedold.append(stored_pes[nums])
            changednew.append(current_pes[nums])
            for secs in storeToChange:
                if current_vals[nums] == secs:
                    wksStore.update(
                        str(storeToChange[secs]), str(current_pes[nums]))

    if changed == []:
        return

    gets = {"Industrials": 'B2:B', "Basic Materials": 'E2:E', "Consumer Cyclical": 'H2:H', "Financial Services": 'K2:K', 'Consumer Defensive': 'N2:N',
            "Healthcare": 'Q2:Q', "Technology": 'T2:T', "Utilities": 'W2:W', "Energy": 'Z2:Z', "Communication Services": 'AC2:AC'}
    linksNum = 0
    for sectors in changed:
        sigma = 6
        n = wksAlgo.get(str(gets[sectors]))
        time.sleep(10)
        x = []
        for lists in n:
            for nlists in lists:
                x.append(nlists)

        x = pd.to_numeric(x)
        mean = (sum(x)/len(x))
        y = stats.norm.pdf(x, mean, sigma)
        plt.scatter(x, y, label='Historic CAPE')
        plt.scatter(x[0], y[0], marker='o', color='red', label='Current CAPE')
        plt.xlabel('CAPE')
        plt.ylabel('Distribution')
        plt.title(f'{sectors} Sector')
        print(
            f"The {sectors} sector has changed from {changedold[linksNum]} to {changednew[linksNum]}!")
        plt.savefig(fname='plot')
        with open("plot.png", "rb") as imagefile:
            imagedata = imagefile.read()
        t_upload = Twitter(domain='upload.twitter.com',
                           auth=OAuth(token, token_secret, consumer_key, consumer_secret))
        id_img1 = t_upload.media.upload(media=imagedata)["media_id_string"]
        t.statuses.update(
            status=f"The {sectors} sector has changed from {changedold[linksNum]} to {changednew[linksNum]}!", media_ids=",".join([id_img1]))
        os.remove('plot.png')
        plt.clf()
        linksNum = + 1

######################## Weekly Score Movement Tracker ###############################

# Track the changes in PE over the last week
def scoretracker():
    plt.style.use('fivethirtyeight')

    x = list(range(0, 8))
    print(x)
    listofgets = ['B9:B16', 'C9:C16', 'D9:D16', 'E9:E16', 'F9:F16',
                  'G9:G16', 'H9:H16', 'I9:I16', 'J9:J16', 'K9:K16', 'L9:L16']
    labels = ['Materials', 'Cons. Cycl.', 'Financials', 'Cons. Def.', 'Healthcare',
              'Technology', 'Utilities', 'Energy', 'Comm. Services', 'Industrials', 'S&P 500']
    colors = ['blue', 'red', 'green', 'orange', 'purple',
              'mediumpurple', 'wheat', 'lightcoral', 'silver', 'gold', 'aqua']
    fig, ax = plt.subplots()
    labn = 0
    for gets in listofgets:
        BM = wks.get(gets)
        BM = sum(BM, [])  # changes from list of list to one flat list
        BM.reverse()
        BM = np.array(BM, dtype=float)
        BMB = (np.diff(BM) / np.abs(BM[:-1]) * 100)
        Changed = [100]
        i = 1
        for changes in BMB:
            Changed.append(changes+Changed[i-1])
            i = i + 1
        print(Changed)
        ax.plot(x, Changed, label=labels[labn], color=colors[labn])
        labn = labn + 1

    ax.legend(frameon=False, loc='best', labelspacing=0.05, prop={'size': 10})
    ax.set_title("PE 10 Changes (scaled)")
    plt.savefig(fname='plot')
    with open("plot.png", "rb") as imagefile:
        imagedata = imagefile.read()
    t_upload = Twitter(domain='upload.twitter.com',
                       auth=OAuth(token, token_secret, consumer_key, consumer_secret))
    id_img1 = t_upload.media.upload(media=imagedata)["media_id_string"]
    t.statuses.update(status=f"Changes in PE 10 for the week:",
                      media_ids=",".join([id_img1]))
    os.remove('plot.png')
    plt.clf()

######################## Weekly Sector Status Update Table ###############################

# Make a status table representing the valuations of the sectors
def statustable():
    current_pes = wksAlgo.get('A2:AE2')
    current_pes = current_pes[0]
    current_pes = current_pes[3::3]
    current_vals = wksStore.get('B8:L8')
    current_vals = current_vals[0]
    print(current_pes)
    print(current_vals)
    df = pd.DataFrame({"Sector": current_vals,
                       "Status": current_pes,
                       })

    map_color = {"MIGHTLY OVERVALUED": "darkred", "EXTREMELY OVERVALUED": "red", "OVERVALUED": "lightcoral", "ABOVE AVERAGE": "orange",
                 "AVERAGE": "yellow", "BELOW AVERAGE": "lightgreen", "UNDERVALUED": "green", "EXTREMELY UNDERVALUED": "darkgreen", "CRASH": "darkblue"}

    df["color"] = df["Status"].map(map_color)

    cols_to_show = ["Sector", "Status"]
    fill_color = []
    n = len(df)
    for col in cols_to_show:
        if col != 'Status':
            fill_color.append('white')
        else:
            fill_color.append(df["color"].to_list())
    data = [go.Table(
        header=dict(values=[f"<b>{col}</b>" for col in cols_to_show],
                    fill_color='white',
                    line_color='white',
                    align='center',
                    font=dict(color='black', size=20),
                    height=30
                    ),
        cells=dict(values=df[cols_to_show].values.T,
                   fill_color=fill_color,
                   line_color='white',
                   align='left',
                   font=dict(color='black', size=20),
                   height=30
                   ))
            ]
    fig = go.Figure(data=data)
    fig.write_html("fig.html")
    asyncio.get_event_loop().run_until_complete(converter())
    im = Image.open(config.fig_path1)
    left = 75
    right = 725
    top = 100
    bottom = 475
    im1 = im.crop((left, top, right, bottom))
    im1.save('fig2.png')
    with open("fig2.png", "rb") as imagefile:
        imagedata = imagefile.read()
    t_upload = Twitter(domain='upload.twitter.com',
                       auth=OAuth(token, token_secret, consumer_key, consumer_secret))
    id_img1 = t_upload.media.upload(media=imagedata)["media_id_string"]
    t.statuses.update(status="Sector statuses", media_ids=",".join([id_img1]))
    os.remove('fig1.png')
    os.remove('fig2.png')
    print("Image Posted")


# BUYSCORES SCHEDULING
schedule.every().monday.at("21:00").do(buyscores)

# WEEKLY STATUS TABLE SCHEDULING
schedule.every().thursday.at("22:14").do(statustable)

# VALUE CHANGE ALERT SCHEDULING
schedule.every().monday.at("21:10").do(valuealert)
schedule.every().tuesday.at("21:10").do(valuealert)
schedule.every().wednesday.at("21:10").do(valuealert)
schedule.every().thursday.at("21:10").do(valuealert)
schedule.every().friday.at("21:10").do(valuealert)

# SCORE TRACKER SCHEDULING
schedule.every().friday.at("21:15").do(scoretracker)

while True:
  # run_pending
    schedule.run_pending()
    time.sleep(1)
