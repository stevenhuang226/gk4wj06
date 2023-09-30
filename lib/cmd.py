class lsuser:
	async def lsuser(ctx):
		user_list = '\n'.join(ctx.guild.members)
		return user_list
	async def man():
		return 'list all of member in this guild\n顯示此伺服器內的所有成員'
class lssql:
	async def botshow(ctx,sql_name,guild_name,arg_list):
		"""
		ctx => 指令內容（class）
		arg_list => 輸入一個list（通常為使用者輸入的指令，然後切割為list）
		"""
		from data import data_storage
		sql = data_storage()
		sql.init(sql_name)
		if arg_list[0] == 'speaktimes':
			if arg_list[1] in ['all','-a','a','A']:
				table = sql.select(guild_name,"speaktimes IS NOT NULL")
				speaktimes_split_text = []
				for row in table:
					speaktimes_split_text.append(row[1],row[2])
				return '\n'.join(speaktimes_split_text)
			else:
				row = sql.select(guild_name,f"name == '{arg_list[1]}'")
				return f"{row[1]} {row[2]}"
		elif arg_list[0] == 'userid':
			if arg_list[1] in ['all','-a','a','A']:
				table = sql.select_all(guild_name)
				return '\n'.join([' '.join([row[1],row[2]]) for row in table])
			else:
				row = sql.select(guild_name,f"name == {arg_list[1]}")
				return f"{row[1]} {row[2]}"
