import time
import json
import datetime
import asyncio
import discord
from cetusClass import *

#Function to obtain current date in milliseconds
current_milli_time = lambda: int(round(time.time() * 1000))

nightTime = 3000000 #time in miliseconds
delay = 22000 # time in miliseconds

msg = 0

#async def cetusTime(data, bot, channel):
async def cetusTime(data, bot):
	try:
		expiry = int(data['SyndicateMissions'][9]['Expiry']['$date']['$numberLong'])
		now = current_milli_time()
		millisLeft = expiry-now
		dayTime = millisLeft > nightTime

		millisLeft = millisLeft - nightTime if dayTime else millisLeft
		timeLeft = datetime.datetime.utcfromtimestamp(millisLeft/1000.0)

		cetus = Cetus(dayTime,timeLeft)

		now = datetime.datetime.now()
		expiry = datetime.datetime.fromtimestamp(expiry/1000.0)

		#try:
		#	global msg
		#	if (msg == 0):
		#		try:
		#			msg = await bot.send_message(channel, embed=cetus.toEmbed())
		#		except Exception:
		#			pass
		#	elif(expiry>now):
		#		try:
		#			await bot.edit_message(msg, embed=cetus.toEmbed())
		#		except Exception:
		#			pass
		#	else:
				#await bot.edit_message(msg, embed=cetus.toEmbed())
				#if millisLeft<0 and not dayTime:
				#	await bot.delete_message(msg)
				#	msg=0
		#		try:
		#			await bot.delete_message(msg)
		#		except Exception:
		#			pass
		#		msg = 0
		#except IndexError:
		#	pass

		return timeLeft, dayTime
	except IndexError:
		pass

