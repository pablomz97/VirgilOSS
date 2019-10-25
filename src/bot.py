import discord
import discord.utils
from discord.ext.commands import Bot
from discord import Game

import requests
import json
import time
import datetime
import asyncio
from loops import *

ids = json.load(open('res/json/ids.json'))

TOKEN = ids['token']
#Clan server
alertChannel = discord.Object(id = ids['alertChannel'])
botChannel = discord.Object(id = ids['botChannel'])
cetusChannel = discord.Object(id = ids['cetusChannel'])

#prefijos a usar por el bot
BOT_PREFIX = ("/")

#inicializacion de la clase
client = Bot(command_prefix=BOT_PREFIX)    
client.remove_command('help')

availableRoles = list()

def startRoles():
	#global roles
	lista = json.load(open('res/json/roles.json'))['Roles']
	for x in lista:
		availableRoles.append(x['name'])
	print(availableRoles)

async def removeOtherRoles(user):
	for i in availableRoles:
		for j in user.roles:
			if(j.name == i):
				await client.remove_roles(user, j)

@client.command(name = 'add', pass_context = True)
async def add(ctx, role : str):
	try:
		#tries to get role from server
		newRole = discord.utils.get(ctx.message.server.roles, name=role)
		#check if role is in alerts
		if newRole.name in availableRoles:
			#user doenst have the role
			if(newRole not in ctx.message.author.roles):
				#removes other alert roles the user has
				await removeOtherRoles(ctx.message.author)
				await client.add_roles(ctx.message.author, newRole)
				await client.say("Role Assigned")
			#user is already in the role
			else:
				output = "You are already in <" + role + ">"
				await client.say(output)
		#role exists but not in alerts
		else:
			await client.say("Role not available")			

	#role doesnt exist
	except AttributeError as e:
		try:
			output = 'Role doesnt exist. Available roles: \n' + ''.join(str(e)+'\n' for e in availableRoles)
			await client.say(output)
		except Exception:
			pass

@client.command(name = 'rm', pass_context = True)
async def rm(ctx, role : str):
	try:
		newRole = discord.utils.get(ctx.message.server.roles, name=role)
		if(newRole in ctx.message.author.roles):
			await client.remove_roles(ctx.message.author, newRole)
			await client.say("Role Removed")
		else:
			authorRoles = ctx.message.author.roles
			del authorRoles[0]
			output = 'You arent in <'+ role +'>. Your roles: \n' + ''.join(str(e)+'\n' for e in authorRoles)
			await client.say(output)

	except Exception as e:
		try:
			await client.say('Role doesnt exist')
		except Exception:
			pass	

@client.command(name = 'info')
async def info():
    embed = discord.Embed(title="VirgilOSS", description="Manages Warframe Alerts", color=0x266ee2)
    embed.add_field(name="Author", value="BassNuke")
    embed.add_field(name="Server count", value=len(client.servers))
    embed.add_field(name="Invite", value="[Invite link](<insert your OAuth invitation link here>)")
    await client.say(embed=embed)

@client.command(name = 'roles')
async def roles():
    embed=discord.Embed(title="Available Roles", description="Each role is mentioned when any of the corresponding items in it or in the roles above appears.\
                                                                If you dont agree with an item positioning please PM BassNuke", color=0x01ff16)
    embed.add_field(name="T5", value="Potatoes and Riven Mods", inline=False)
    embed.add_field(name="T4", value="Nitain Extract, Vauban Parts, Aura Mods and Kavat Codes", inline=False)
    embed.add_field(name="T3", value="Forma and Nightmare Mods", inline=False)
    embed.add_field(name="T2", value="Helmet Blueprints and Kubrow Egg", inline=False)
    embed.add_field(name="T1", value="Materials and everything else not mentioned above", inline=False)
    await client.say(embed=embed)

@client.command(name = 'help')
async def help():
    embed=discord.Embed(title="Boterino Helperino", description="Informs of ongoing alerts and pings roles depending on the reward\n\
    																If theres nothing on the channel there is nothing worthwhile", color=0x01ff16)
    embed.add_field(name="/add <Role>", value="Adds the role and removes other previous AlertRoles", inline=False)
    embed.add_field(name="/help", value="Shows info about all the bot commands", inline=False)
    embed.add_field(name="/info", value="Shows info about the bot", inline=False)
    embed.add_field(name="/roles", value="Shows info of rewards mentioned for each role", inline=False)    
    embed.add_field(name="/rm <Role>", value="Removes the corresponding AlertRole", inline=False)
    await client.say(embed=embed)

@client.event
async def on_message(message):
	if message.author.bot:
			return
	if message.channel.id == botChannel.id:
		await client.process_commands(message)

		if client.user.mentioned_in(message) and message.mention_everyone is False:
			await client.send_message(message.channel, "Type /help for info on the bot commands")
	else:
		if client.user.mentioned_in(message) and message.mention_everyone is False or message.content.startswith('/'):
			for ch in message.server.channels:
				if ch.id == botChannel.id:
					mention = ch.mention
			msg = "Please write commands to me in " + mention + ". Type /help there for the list of commands."
			await client.send_message(message.author, msg)
			await client.delete_message(message)

@client.event
async def on_ready():
	await clearFunction(client, alertChannel)
	print('Logged in as')
	print(client.user.name)
	#print(client.user.id)
	print('------')

startRoles()
client.loop.create_task(updateJSON(client))
client.loop.create_task(loopAlerts(client,alertChannel))
#client.loop.create_task(loopCetus(client,cetusChannel))
client.loop.create_task(loopCetus(client))
client.run(TOKEN)