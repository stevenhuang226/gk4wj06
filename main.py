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
bot = commands.Bot(command_prefix='$',case_insensitive=True,intents=intents)


@client.event
async def on_ready():
	logger.write(f'logged as {client.user}')
	logger.write(f'server list {", ".join([element.name for element in client.guilds])}')
	for guild in client.guilds:
		await sql.create_table_p(str(guild.id),{'ID':'INTEGER PRIMARY KEY','name':'TEXT','speaktimes':'INTEGER'})
@client.event
async def on_message(message):
	guild_id = str(message.guild.id)
	if message.bot == False:
		user_sql_info = sql.select_id(guild_id,message.author.id,'ID',True)
		if user_sql_info:
			await sql.update(guild_id,{'speaktimes':user_sql_info.speaktimes+1})
		else:
			await sql.insert_into(guild_id,['ID','name','speaktimes'],[message.author.id,message.author.name,1])
@bot.command()
async def lsuser(ctx):
	await ctx.send(await lsuser().lsuser(ctx))
@bot.command()
async def lssql(ctx,*arg):
	await ctx.send(await lssql().botshow(ctx,db_file,ctx.guild.id,list(arg)))
###
#@bot.command()
#async def lsuser(ctx):
#	await ctx.send(await lsuser().lsuser(ctx))
#async def lssql(ctx,*arg):
#	arg_list = list(arg)
#	await ctx.send(await lssql().botshow(ctx,db_file,arg_list))
#async def man(ctx,arg):
#	"""
#	ctx => 指令內容
#	arg => 顯示「指令」的說明文檔
#	"""
#	if arg == 'lsuser':
#		await ctx.send(await lsuser().man())
###