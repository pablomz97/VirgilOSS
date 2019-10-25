import time
import datetime
import json
import asyncio
import discord
from alertClass import *

#role to mention
#Clan role
#roleID = "<@&469279521044955156>"
roleID = "<@&469267150935162890>"

#Function to obtain current date in milliseconds
current_milli_time = lambda: int(round(time.time() * 1000))

#Function to convert milliseconds to minutes
millis_to_mins = lambda x: int((x/(1000*60))%60)

#Item dictionary
items = json.load(open('res/json/items.json'))
#Mission Type dictionary
missions = json.load(open('res/json/missiontype.json'))
#Solar Nodes Dictionary
locations = json.load(open('res/json/solarNodes.json'))
#Interesting rewards
rewards = json.load(open('res/json/usefulItems.json'))['Items']
#Item per Role
itemRoles = json.load(open('res/json/roles.json'))['Roles']


ongoing = list()

async def check(item : str):
    msg = ""
    found = False
    for i in itemRoles:
        if found:
            msg += i['id'] + " "
        else:
            if item in i['items']:
                found = True
                msg = i['id'] + " "
    if not found:
        msg = itemRoles[4]['id']
    return msg

#Alert info output
async def alerts(data, bot, channel):
	alertList = data['Alerts']
	for i in range(0,len(alertList)):
		alert = alertList[i]
		case = 0
		contained = False
		end = False

		#Rewards
		try:
			reward = alert['MissionInfo']['missionReward']['countedItems'][0]
			case = 1
		except KeyError:
			pass

		try:
			reward = alert['MissionInfo']['missionReward']['items'][0]
			case = 2
		except KeyError:
			pass

		if(case != 0):
			#Mission Type String
			missionType = missions[alert['MissionInfo']['missionType']]['value']
			#Location String
			location = locations[alert['MissionInfo']['location']]['value']
			#Rewardss String
			if(case == 1):
				try:
					item = items[reward['ItemType']]
					reward = "{}x {}".format(reward['ItemCount'],items[reward['ItemType']])
				except KeyError:
					pass
			else:
				try:
					item = items[reward]
					reward = items[reward]
				except KeyError:
					pass

			now = datetime.datetime.now()

			#Time start String
			activation = int(alert['Activation']['$date']['$numberLong'])
			#timeStart = datetime.datetime.fromtimestamp(start/1000.0)

			#Time left String
			expiry = int(alert['Expiry']['$date']['$numberLong'])
			#timeLeft = datetime.datetime.fromtimestamp(expiry/1000.0)

			#if (timeLeft>now):
			#	diffEnd = (datetime.datetime.min + (timeLeft-now)).time() 
			#else:
			#	diffEnd = datetime.datetime.fromtimestamp(0)
			#	end=True

			#diffStart = (datetime.datetime.min + (timeStart-now)).time() if timeStart>now else datetime.datetime.fromtimestamp(0)

			actualAlert = Alert(missionType,location,reward,activation,expiry)
            
			if(actualAlert not in ongoing):
				ok, embed = actualAlert.toEmbed()
				if(ok):
					try:
						msg = await bot.send_message(channel, embed=embed)
						try:
							mensaje = await check(item)
							mention = await bot.send_message(channel, mensaje)
							actualAlert.addMention(mention)
							actualAlert.changeMessage(msg)
							ongoing.append(actualAlert)
							print("Added ", actualAlert.reward, " to ongoing")
						except Exception:
							pass
					except Exception:
						pass

					#if(item in rewards):
					#	try:
					#		mention = await bot.send_message(channel, roleID)
					#	except Exception:
					#		pass
					#	actualAlert.addMention(mention)
					#actualAlert.changeMessage(msg)
					#ongoing.append(actualAlert)
					#print("Added ", actualAlert.reward, " to ongoing")

	for x in ongoing:
		if(not x.end()):
			#x.update(actualAlert)
			ok, embed = x.toEmbed()
			try:
				await bot.edit_message(x.msg, embed=embed)
			except Exception:
				pass
			print("Updated ", x.reward)
		else:
			try:
				await bot.delete_message(x.msg)
			except Exception:
				pass
			if(x.hasMention):
				try:
					await bot.delete_message(x.mention)
				except Exception:
					pass
				
			print("Deleted ", x.reward)
			ongoing.remove(x)