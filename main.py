import discord,os,datetime
from discrod.ext import commands
from lib.logger import write_log
from lib.command_man import *
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

# 初始化discord參數
intents = discord.Intents.default()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='$',intents=intents)


@client.event
async def on_ready():
	logger.write(f'logged as {client.user}')
	logger.write(f'server list {", ".join([element.name for element in client.guilds])}')
@client.event
async def on_message():
	if message.bot == False:
		#TODO 紀錄發言者的ID到SQL

@bot.command()
async def lsuser(ctx):
	user_list = '\n'.join(ctx.guild.members)
	await (ctx.send(f""))
async def man(ctx,*arg):
	await (ctx.send(f"{lsuser_man().man()}"))