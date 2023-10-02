class lsuser:
	async def lsuser(self,message):
		user_list = '\n'.join(message.guild.members)
		return user_list
	async def man(self):
		return 'list all of member in this guild\n顯示此伺服器內的所有成員'
class lssql:
	async def sql_select(self,message,sql_name,arg_list):
		"""
		message => 指令內容
		arg_list => 輸入一個list（通常為使用者輸入的指令，然後切割為list）
		"""
		from data import *
		sql = data_storage()
		sql.init(sql_name)
		guild_id = sql_help().tran_table_name(message.guild.id)
		if arg_list[0] == 'speaktimes':
			if arg_list[1] in ['all','-a','a','A']:
				table = sql.select(guild_id,"speaktimes IS NOT NULL")
				speaktimes_split_text = []
				for row in table:
					speaktimes_split_text.append(row[1],row[2])
				return '\n'.join(speaktimes_split_text)
			else:
				row = sql.select(guild_id,f"name == '{arg_list[1]}'")
				return f"{row[1]} {row[2]}"
		elif arg_list[0] == 'userid':
			if arg_list[1] in ['all','-a','a','A']:
				table = sql.select_all(guild_id)
				return '\n'.join([' '.join([row[1],row[2]]) for row in table])
			else:
				row = sql.select(guild_id,f"name == {arg_list[1]}")
				return f"{row[1]} {row[2]}"
	async def man(self):
		return '''speaktimes: -a all 顯示全部使用者的說話次數（已紀錄）
			user_name 顯示[user_name]的說話次數（已紀錄）
	userid -a all 顯示全部使用著對應的id(discord)（曾經講過話的才會被紀錄）
			user_name 顯示[user_name]的id(discord)（曾經講過話的才會被紀錄）
'''