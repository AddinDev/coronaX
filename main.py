import discord
import os
import requests
import json
import random
from keep_alive import keep_alive

client = discord.Client()

sad_words = ["sad", "depressed", "unhappy", "angry"]

starter_encouragements = [
  "Cheer up!",
  "Hang in there.",
  "Just don't die",
  "You are a great person / bot!"
]

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q']
  author = json_data[0]['a']
  text = quote + " -" + author
  return(text)

@client.event
async def on_ready():
  print('We have logged')
  print(self.user.name)
  print(self.user.id)
  print('------')

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if msg.startswith('$hello'):
    await message.channel.send('Hello!')
    
  if msg.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  if msg.startswith('$coronaX'):
    text = "Useless bot made by udin. Fvck u"
    await message.channel.send(text)

  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice(starter_encouragements))

class MyClient(discord.Client):
  async def on_member_join(self, member):
    guild = member.guild
    if guild.system_channel is not None:
      to_send = 'Welcome {0.mention} to {1.name}!'.format(member, guild)
      await guild.system_channel.send(to_send)

intents = discord.Intents.default()
intents.members = True

keep_alive()

token = os.environ['TOKEN']
client.run(token)