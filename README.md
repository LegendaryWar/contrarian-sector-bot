# Contrarian Sector Bot
A bot that uses shiller PE values to gain inferences about current valuations different stock market sectors. The bot categorizes each sector into 9 different categories ranging from CRASH to MIGHTLY OVERVALUED.
 
# Datascraping
The shiller PE values are scraped from a website by using regexes on it's HTML source code. The datascraping takes place on google cloud using google scripts, which directly interact with the spreadsheet at regulay 24 hour periods. The google scripts are also responsible for logging the new data by creating new lines in the database and also sending any changes in valuations to emails or phones.

# Twitter bot
This bot publishes the inferences gained from the spreadsheet database by visualizing the data on a regular basis and uploading it to twitter. The bot constructs three different types of visualizations that each cover different aspects of the data.

## Buyscores
Buyscores are metrics calculated by the spreadsheet that analyze the shiller PE values over the last 10 years. These can give a quick overview on curreny valuation relative to past valuations. These are presented in a gauge chart format.

![image](https://pbs.twimg.com/media/FNS62jOXIAM27j6?format=jpg&name=large)

## Sector Normal Distribution Charts
Whenever a sector changes its valuation from one category to another, a normal distribution chart will be created by the bot. This chart shows the current valuation of the sector compared to its past.

#### The energy sector in Feb 2021
![image](https://pbs.twimg.com/media/EvCrAQbWQAA8Teb?format=png&name=small)

#### The energy sector in April 2022
![image](https://pbs.twimg.com/media/FN2yiHHXMAYL95c?format=png&name=small)

## Sector Valuation Tables
The bot releases the current valuations of the stock market sectors in a table format to provide a summary of the categorizations of each sector. 
![image](https://pbs.twimg.com/media/FQRTV-UXwAAOEDY?format=png&name=small)