class lsuser:
	async def lsuser(ctx):
		user_list = '\n'.join(ctx.guild.members)
		return user_list
	async def man():
		return 'list all of member in this guild\n顯示此伺服器內的所有成員'
class lssql:
	async def botshow(ctx,sql_name,*arg):
		from data import data_storage
		sql = data_storage()
		sql.init(sql_name)
		if arg[0] == 'speaktimes':
			if arg[1] in ['all','-a','a','A']:
				table = sql.select('discord',"speaktimes IS NOT NULL")
				speaktimes_split_text = []
				for row in table:
					speaktimes_split_text.append(row[1],row[2])
				return '\n'.join(speaktimes_split_text)
			else:
				row = sql.select('discord',f"name == '{arg[1]}'")
				return f"{row[1]} {row[2]}"
		elif arg[0] == 'userid':
			if arg[1] in ['all','-a','a','A']:
				table = sql.select_all('discord')
				return '\n'.join([' '.join([row[1],row[2]]) for row in table])
			else:
				row = sql.select('discord',f"name == {arg[1]}")
				return f"{row[1]} {row[2]}"