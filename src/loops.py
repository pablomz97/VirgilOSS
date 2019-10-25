import discord
from discord.ext.commands import Bot
from discord import Game

import requests
import json
import asyncio
from alerts import *
from cetus import *

data = 0


#Clears latest 100 messages
async def clearFunction(client, channel):
	try:
		mgs = [] #Empty list to put all the messages in the log
		number = int(100) #Converting the amount of messages to delete to an integer
		async for x in client.logs_from(channel, limit = 100):
			mgs.append(x)
		await client.delete_messages(mgs)
	except Exception:
		pass

#Update JSON and call alerts
async def updateJSON(client):
	while not client.is_closed:
		while True:
			try:
				global data
				data = json.loads(requests.get("http://content.warframe.com/dynamic/worldState.php").text)
				#print("JSON updated")
				break
			except requests.exceptions.ConnectionError:
				print("Cannot fetch JSON correctly. Retrying...")
				await asyncio.sleep(5)
		#sleep timer for loop
		await asyncio.sleep(60)

async def loopAlerts(client, channel):
	await client.wait_until_ready()
	await asyncio.sleep(5)
	while not client.is_closed:
		await alerts(data,client,channel)
		await asyncio.sleep(60)

#async def loopCetus(client, channel):
async def loopCetus(client):
	await client.wait_until_ready()
	await asyncio.sleep(5)
	while not client.is_closed:
		try:
			#timeLeft, dayTime = await cetusTime(data,client,channel)
			timeLeft, dayTime = await cetusTime(data,client)
			if dayTime:
				if(timeLeft.hour>0):
					await client.change_presence(game=Game(name="{}h {}m to Night".format(timeLeft.hour,timeLeft.minute),type = 3))
				else:
						await client.change_presence(game=Game(name="{}m to Night".format(timeLeft.minute),type = 3))
			else:
				await client.change_presence(game=Game(name="{}m to Day".format(timeLeft.minute),type = 3))
		except Exception:
			pass
		await asyncio.sleep(60)