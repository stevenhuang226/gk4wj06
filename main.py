import discord,os,datetime
from lib.logger import write_log
TOKEN = ""
# check log file
while True():
	log_file = input('input log file name[name => log_file/n => no log]:')
	if (os.path.exists(log_file)):
		break
	elif (log_file == 'n' or log_file == 'N' or log_file == 'no' or log_file == 'No' or log_file == 'NO'):
		log_file = False
		break
logger = write_log(log_file)
logger.write('discord bot start')
client = discord.Client()
@client.event
async def on_ready():
	logger.write(f'logged as {client.user}')
	logger.write(f'server list {", ".join([element.name for element in client.guilds])}')
@client.event
async def on_message():
	