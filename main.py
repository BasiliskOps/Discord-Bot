import discord
import os
import requests
import json
import random
from replit import db 
from keep_alive import keep_alive


client = discord.Client()

key_sentiments = ["sad", "depressed", "unhappy", "angry", "miserable", "meloncholy", "sadness", "lethargic", "morose", "grief", "death", "pain", "dying", "abyss", "afraid", "die", "suffering", "Death", "Suffering", "Suffer", "suffer"]

enlightenment = ["Overcome thy suffering!", "Become the light and the way.", "Doth not the light of the Sun shine upon thee?", "Abandon doubt, for death is always smiling... fly true.", "Alas, though the Abyss may be Immaterium everlasting... the light of thy soul shines further, still.", "Let thy love be ever eternal...", "Oh what dreams may come!", "We'll meet again...", "Don't give up!", "You've got this!", "Never surrender!", "There was a dream that was Rome...", "Waste no more time arguing what a good man should be. Be One. -Marcus Aurelius", "He who fears death will never do anything worth of a man who is alive. -Seneca", "How long are you going to wait before you demand the best for yourself? -Epictetus", "Don't explain your philosophy, Embody it. -Epictetus", "You have power over your mind—not outside events. Realize this, and you will find strength. —Marcus Aurelius"]

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def update_enlightenments(encouraging_message):
  if "enlightenments" in db.keys():
    enlightenments = db["enlightenments"]
    enlightenments.append(encouraging_message)
    db["enlightenments"] = enlightenments
  else:
    db["enlightenments"] = [encouraging_message]

def delete_enlightenment(index):
  enlightenments = db["enlightenments"]
  if len(enlightenments) > index:
    del enlightenments[index]
    db["enlightenments"] = enlightenments 

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
      return

  msg = message.content

  if message.content.startswith('$motivation'):
    quote = get_quote()
    await message.channel.send(quote)

  options = enlightenment
  if "enlightenments" in db.keys():
    options = options + db["enlightenments"]

  if any(word in msg for word in key_sentiments):
    await message.channel.send(random.choice(options))

  if msg.startswith("$new"):
    encouraging_message = msg.split("$new ",1)[1]
    update_enlightenments(encouraging_message)
    await message.channel.send("We have gained wisdom.")

  if msg.startswith("$del"):
    enlightenments = []
    if "enlightenments" in db.keys():
      index = int(msg.split("$del",1)[1])
      delete_enlightenment(index)
      enlightenments = db["enlightenments"]
    await message.channel.send(enlightenments)

keep_alive()
client.run(os.getenv('TOKEN'))