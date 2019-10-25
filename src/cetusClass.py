import discord
class Cetus:

	def __init__(self,dayTime,timeLeft):
		self.actualTime, self.picture, self.color = setCycle(dayTime)
		self.timeLeft = setTimeLeft(timeLeft)

	def toEmbed(self):
		embed=discord.Embed(title="Cetus", description=self.actualTime, color=self.color)
		embed.set_thumbnail(url=self.picture)
		embed.add_field(name="Time Remaining", value=self.timeLeft, inline=False)
		return embed

def setCycle(dayTime):
	if(dayTime==True):
		actualTime = "Day"
		#self.picture ="https://assets.pokemon.com/assets/cms2/img/pokedex/full/338.png"
		picture = "https://vignette.wikia.nocookie.net/warframe/images/6/66/EquinoxDay.png/revision/latest/scale-to-width-down/291?cb=20150731174046"
		color = 0xffffff
	else:
		actualTime = "Night"
		#self.picture ="https://assets.pokemon.com/assets/cms2/img/pokedex/full/337.png"
		picture = "https://vignette.wikia.nocookie.net/warframe/images/4/46/EquinoxNight.png/revision/latest/scale-to-width-down/291?cb=20150731174104"
		color = 0x000001
	return actualTime, picture, color


def setTimeLeft(timeLeft):
	if(timeLeft.hour==0):
		return "{} minutes {} seconds".format(timeLeft.minute, timeLeft.second)
	else:
		return "{} hours {} minutes {} seconds".format(timeLeft.hour, timeLeft.minute, timeLeft.second)