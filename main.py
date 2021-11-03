import discord
import os
import requests
import json
import random
from replit import db

from keep_alive import keep_alive

# Prefix
news_limit  = 5

# Tokens \ Keys
token = os.environ['TOKEN']
newsKey = os.environ['newsKey']


client = discord.Client()

sad_words = ["sad", "depressed", "unhappy", "angry"]

starter_encouragements = [
    "Cheer up!", "Hang in there.", "Just don't die",
    "You are a great person / bot!"
]

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q']
    author = json_data[0]['a']
    text = quote + " -" + author
    return (text)

def get_quran(index):
  response = requests.get("http://api.alquran.cloud/v1/surah")
  json_data = json.loads(response.text)
  surah = json_data['data'][index]
  text = surah['name'] + " - " + surah['englishName'] + " - " + surah['englishNameTranslation'] + " - " + str(surah['numberOfAyahs']) + " ayahs"
  return(text)

def get_news():
  url = 'https://newsapi.org/v2/top-headlines?country=id&apiKey=' + newsKey
  response = requests.get(url)
  json_data = json.loads(response.text)
  news_data = json_data["articles"]
  news_list = []
  for index in range(news_limit):
  	news_list.append(news_data[index])
  return news_list

def search_news(word):
  url = 'https://newsapi.org/v2/everything?q=' + word + '&sortBy=popularity&apiKey=' + newsKey
  response = requests.get(url)
  json_data = json.loads(response.text)
  news_data = json_data["articles"]
  news_list = []
  for index in range(news_limit):
  	news_list.append(news_data[index])
  return news_list

@client.event
async def on_ready():
  print('We have logged as {0.user}'.format(client))
  print('------')

@client.event
async def on_message(message):
  global news_limit

  if message.author == client.user:
      return

  msg = message.content

  if msg.startswith('/hello'):
    await message.channel.send('Hello!')

  if msg.startswith('/inspire'):
    print("Inspire")
    quote = get_quote()
    await message.channel.send(quote)

  if msg.startswith('coronaX'):
    text = "\nHewwo!\nUseless bot made by udin.  \nMade with Python 🐍 \n"
    await message.channel.send(text)

# Spam
  if msg.startswith('/spam'):
    print("Spam")
    splitted = msg.split()
    name = splitted[1]
    time = int(splitted[2])
    for _ in range(time):
      await message.channel.send(name)

# Quran
  if msg.startswith('/quran'):
    print("Quran")
    quran_index = int(msg.split("/quran ", 1)[1]) - 1
    if quran_index < 114:
      surah = get_quran(quran_index)
      await message.channel.send(surah)
    else:
      await message.channel.send("error lah blok, surah cuma ada 114")

# News
  if msg.startswith('/news'):
    print("News")
    news_list = get_news()
    for news in news_list:
        text = news["source"]["name"] + " - " + news["description"]
        await message.channel.send(text + "\n===========")

  if msg.startswith('/search'):
    print("Search")
    word = msg.split("/search ", 1)[1]
    news_list = search_news(word)
    await message.channel.send("SEARCHING FOR: " + word) 
    for news in news_list:
        text = news["source"]["name"] + " - " + news["description"]
        await message.channel.send(text + "\n===========") 

  if msg.startswith('/nl'):
    await message.channel.send("News Limit: " + str(news_limit))

  if msg.startswith('/sl'):
    new_limit = int(msg.split("/sl ", 1)[1])
    if (new_limit <= 0):
      await message.channel.send("Use your brain")
    elif (new_limit > 10):
      await message.channel.send("Kebanyakan. memory bocor")
    else:
      news_limit = new_limit
      await message.channel.send("Done. Current limit: " + str(new_limit))

  if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(starter_encouragements))


# Live the server
keep_alive()

client.run(token)
