import discord
import os
import requests
import json
import random

from keep_alive import keep_alive

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

def getNews():
  url = 'https://newsapi.org/v2/top-headlines?country=id&apiKey=' + newsKey
  response = requests.get(url)
  json_data = json.loads(response.text)
  news_data = json_data["articles"]
  news_list = []

  for index in range(5):
  	news_list.append(news_data[index])
  return news_list

@client.event
async def on_ready():
  print('We have logged as {0.user}'.format(client))
  print('------')

@client.event
async def on_message(message):
  if message.author == client.user:
      return

  msg = message.content

  if msg.startswith('/hello'):
    await message.channel.send('Hello!')

  if msg.startswith('/inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  if msg.startswith('coronaX'):
    text = "\nHewwo!\nUseless bot made by udin.  \nMade with Python 🐍 \n"
    await message.channel.send(text)

  if msg.startswith('/quran'):
    quran_index = int(msg.split("/quran ", 1)[1]) - 1
    if quran_index < 114:
      surah = get_quran(quran_index)
      await message.channel.send(surah)
    else:
      await message.channel.send("error lah blok, surah cuma ada 114")

  if msg.startswith('/news'):
    news_list = getNews()
    for news in news_list:
        text = news["source"]["name"] + " - " + news["description"]
        await message.channel.send(text + "\n===========")

  if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(starter_encouragements))


# Live the server
keep_alive()

client.run(token)
