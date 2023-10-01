import discord,os,datetime,asyncio
from discord.ext import commands
from dotenv import load_dotenv
from lib.logger import write_log
from lib.cmd import *
from lib.data import *
load_dotenv()
TOKEN = os.getenv('DC_TOKEN')
sql = data_storage()
sql_h = sql_help() #用於統一轉換某些變數，避免與SQLite語法衝突
logger = write_log()
# check log file
while True:
	log_file = input('input log file name[name => log_file | n => no log]:')
	if (os.path.exists(log_file)):
		print(log_file)
		logger.init(log_file)
		logger.write(f'discord bot start at {os.getcwd()}')
		logger.write(f"token = {TOKEN}")
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
		await sql.create_table_p(sql_h.tran_table_name(guild.id),{'ID':'INTEGER PRIMARY KEY','name':'TEXT','speaktimes':'INTEGER'})
@client.event
async def on_message(message):
	guild_id = str(message.guild.id)
	if not message.author.bot:
		user_sql_info = await sql.select_id(sql_h.tran_table_name(guild_id),message.author.id,'ID',True)
		print(user_sql_info) #test
		if user_sql_info:
			await sql.update(sql_h.tran_table_name(guild_id),{'speaktimes':user_sql_info['speaktimes']+1},f"ID == {message.author.id}")
		else:
			await sql.insert_into(sql_h.tran_table_name(guild_id),['ID','name','speaktimes'],[message.author.id,message.author.name,1])
@bot.command()
async def lsuser(ctx):
	await ctx.send(await lsuser().lsuser(ctx))
@bot.command()
async def lssql(ctx,*arg):
	await ctx.send(await lssql().botshow(ctx,db_file,sql_h.tran_table_name(ctx.guild.id),list(arg)))
client.run(TOKEN)
