import discord,os,datetime,asyncio
from discord.ext import commands
from lib.logger import write_log
from lib.cmd import *
from lib.data import data_storage
TOKEN = ""
sql = data_storage()
logger = write_log()
# check log file
while True:
	log_file = input('input log file name[name => log_file | n => no log]:')
	if (os.path.exists(log_file)):
		print(log_file)
		logger.init(log_file)
		logger.write(f'discord bot start at {os.getcwd()}')
		break
	elif (log_file == 'n' or log_file == 'N' or log_file == 'no' or log_file == 'No' or log_file == 'NO'):
		log_file = False
		print('no log mode')
		break
	else:
		continue
#check sqlite file
while True:
	db_file = input('input the sqlite file name[you must be used it]:')
	if (os.path.exists(db_file)):
		sql.init(db_file)
		logger.write(f'discord bot db file = {db_file}')
		print('db file = ',db_file)
		break
	else:
		continue

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
		await sql.create_table_p('discord',{'ID':'INTEGER PRIMARY KEY','name':'TEXT','speaktimes':'INTEGER'})
		user_sql_info = sql.select_id('discord',message.author.id,'ID',True)
		if user_sql_info:
			await sql.update('discord',{'speaktimes':user_sql_info.speaktimes+1})
		else:
			await sql.insert_into('discord',['ID','name','speaktimes'],[message.author.id,message.author.name,1])
@bot.command()
async def lsuser(ctx):
	await ctx.send(await lsuser().lsuser(ctx))
async def lssql(ctx,*arg):
	await ctx.send(await lssql().botshow(ctx,db_file,*arg))
async def man(ctx,arg):
	if arg == 'lsuser':
		await ctx.send(await lsuser().man())