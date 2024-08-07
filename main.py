import discord, os
from discord.ext import commands
from dotenv import load_dotenv
from lib.logger import write_log
from lib.function import *

load_dotenv()
TOKEN = os.getenv("DC_TOKEN")
cmd = cmds()
# check log file
while True:
    log_file = input("input log file name[name => log_file | n => no log]:")
    if os.path.exists(log_file):
        print(log_file)
        logger = write_log(log_file)
        logger.write(f"discord bot start at {os.getcwd()}")
        logger.write(f"token = {TOKEN}")
        break
    elif log_file == "n" or log_file == "N" or log_file == "no" or log_file == "No" or log_file == "NO":
        print("no log mode")
        logger = write_log()
        logger.write(f"discord bot start at {os.getcwd()}")
        logger.write(f"token = {TOKEN}")
        break

# check sqlite file
while True:
    db_file = input("input the sqlite file name[you must be used it]:")
    if os.path.exists(db_file):
        sql = data_storage(db_file)
        logger.write(f"discord bot db file = {db_file}")
        print("db file = ", db_file)
        break

# 初始化discord參數
intents = discord.Intents.default()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix=">", intents=intents)


@client.event
async def on_ready() -> None:
    logger.write(f"logged as {client.user}")
    logger.write(f'server list {", ".join([element.name for element in client.guilds])}')
    for guild in client.guilds:
        await sql.create_table_p(tran_table_name(guild.id), {"ID": "INTEGER PRIMARY KEY", "name": "TEXT", "speaktimes": "INTEGER"})


@client.event
async def on_message(message: discord.Message) -> None:
    guild_id = tran_table_name(message.guild.id)
    if not message.author.bot:
        if not message.content.startswith(">"):
            user_sql_info = await sql.select_id(guild_id, message.author.id, "ID", True)
            if user_sql_info is not None:
                await sql.update(guild_id, {"speaktimes": user_sql_info["speaktimes"] + 1}, f"ID == {message.author.id}")
            else:
                await sql.insert_into(guild_id, ["ID", "name", "speaktimes"], [message.author.id, message.author.name, 1])
        else:
            split_text = message.content.split(" ")
            if split_text[1] == "lsuser":
                if not split_text[2] == "man":
                    await message.channel.send(cmd.lsuser(message))
                else:
                    await message.channel.send(cmd.lsuser_man())
            if split_text[1] == "lssql":
                if not split_text[2] == "man":
                    await message.channel.send(cmd.sql_select(message, db_file, split_text[2:]))
                else:
                    await message.channel.sned(cmd.lssql_man)


client.run(TOKEN)
