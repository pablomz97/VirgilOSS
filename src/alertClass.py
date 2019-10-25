import discord
import datetime
class Alert:

	def __init__(self,missionType,location,reward, activation, expiry):
		self.missionType=missionType
		self.location=location
		self.reward=reward
		self.activation=activation
		self.expiry=expiry
		self.hasMention=False

	def update(self, other):
		self.timeLeft=other.timeLeft
		self.timeStart=other.timeStart
		self.booleano=other.booleano
		self.stringStart=other.stringStart
		self.color=other.color

	def end(self):
		now = datetime.datetime.now()
		expiry = datetime.datetime.fromtimestamp(self.expiry/1000.0)
		if(expiry<now):
			return True
		else:
			return False

	def changeMessage(self,msg):
		self.msg=msg

	def addMention(self,msg):
		self.mention=msg
		self.hasMention=True

	def toEmbed(self):
		activationTime = getTimetoTimestamp(self.activation)
		expiryTime = getTimetoTimestamp(self.expiry)
		
		if(expiryTime!=False):
			booleano, stringInfo = setStringStart(activationTime)
			if(activationTime!=False):
				stringStart = setTimeLeft(activationTime)
			stringLeft = setTimeLeft(expiryTime)
			color = setColor(expiryTime)

			embed=discord.Embed(title=self.reward, color=color)
			embed.add_field(name=self.missionType, value=self.location, inline=True)
			embed.add_field(name=stringInfo, value=stringLeft if booleano else stringStart, inline=True)
			return True, embed	
		else:
			return False, -1

	def __hash__(self):
		return hash((self.missionType,self.location,self.reward,\
			self.timeStart,self.timeLeft,self.color))

	def __eq__(self,other):
		if not isinstance(other,type(self)): return NotImplemented
		return self.location==other.location and \
			self.missionType==other.missionType

def getTimetoTimestamp(timestamp):
	now = datetime.datetime.now()
	timestampDate = datetime.datetime.fromtimestamp(timestamp/1000.0)
	return (datetime.datetime.min + (timestampDate-now)).time() if timestampDate>now else False

def setColor(timeLeft):
	if(timeLeft.hour<1):
		if(timeLeft.minute<15):
			return 0xff0000
		elif(timeLeft.minute<30):
			return 0xf7e10c
		else:
			return 0x01ff16
	else:
		return 0x01ff16

def setTimeLeft(timeLeft):
	if(timeLeft.hour==0):
		return "{} minutes".format(timeLeft.minute)
	else:
		return "{} hours {} minutes".format(timeLeft.hour, timeLeft.minute)

def setStringStart(timeStart):
	#if(timeStart.minute>=0 and timeStart.second>0):
	if(timeStart==-1):
		return False,"Starts In"
	else:
		return True,"Time Remaining"
