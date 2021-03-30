import discord
from discord.ext import commands, tasks
import urllib
import json


TOKEN = ''

PREFIX = '!BTC'

SERVER_MSG = '[BTC] '

#GETTING THE BOT TOKEN
with open('./token.txt', 'r') as f:
    TOKEN = f.read()


# web scrape
async def retrieve_btc():
    URL = 'https://data.messari.io/api/v1/assets/btc/metrics'
    old_price = 0   #btc old price
    up_arrow = '↗️'
    down_arrow = '↘️'
    data = urllib.request.urlopen(URL).read()
    data = data.decode('utf-8')
    data = json.loads(data)
    btc_data = data["data"]
    market_data = btc_data["market_data"]
    price = str(market_data["price_usd"])     #btc current price
    print(SERVER_MSG + 'BTC $' + price[:8])
    percent_change = str(market_data["percent_change_usd_last_24_hours"])
    print(SERVER_MSG +'24h: ' +  percent_change[:10] + '%')
    if float(price) > float(old_price):
        old_price = price
        return str(price[:8]), str(percent_change[:10]), up_arrow

    elif float(price) < float(old_price):
        old_price = price
        return str(price[:8]), str(percent_change[:10]), down_arrow

    else:
        old_price = price
        return str(price[:8]), str(percent_change[:10]), '='


client = commands.Bot(command_prefix=PREFIX)


@tasks.loop(seconds=60)
async def update_crypto():
    btc_price, percent_change, arrow = await retrieve_btc()
    act = discord.Activity(name=f'$ 24h: {percent_change}%', type=discord.ActivityType.watching)
    await client.change_presence(status=discord.Status.online, activity=act) #24hr return
    print(SERVER_MSG + "Bot Activity Updated")

    # changing the bot nickname
    guilds = client.guilds
    for guild in guilds:
        members = guild.members
        for member in members:
            if member.name == client.user.name:
                await member.edit(nick=f'BTC ${btc_price} ({arrow})')   #change the BTC price to the price
                print(SERVER_MSG + 'BTC Data Updated!')

@client.event
async def on_ready():
    print(SERVER_MSG + 'The Bot is Online!')
    update_crypto.start()


print(SERVER_MSG + 'Starting....')
client.run(TOKEN, reconnect=True)
print(SERVER_MSG + 'Bot Ended')
