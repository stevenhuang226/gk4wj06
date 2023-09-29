import os,sqlite3
class data_storage:
	async def __init__(self,data_log_name):
		self.sql_data_name = data_log_name
		init_sql()
	async def init_sql(self):
		sql = sqlite3.connect(self.data_log_name)
		sql.autocommit(True)
		self.sql = sql
		self.cursor = sql.cursor()
	async def create_table(self,table_name,valuetype): #key_valuetype形式 {key:data_type,key:data_type}
		#check table ready or not
		self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
		result = self.cursor.fetchone()
		if result:
			pass
			# return "create table false, table has exists"
		else:
			split_text = [f"CREATE TABLE {table_name} ("]
			for column, data_type in key_valuetype.items():
				split_text.append(f"	{column} {data_type},")
			split_text.append(")")
			await self.cursor.execute('\n'.join(split_text))
			await self.sql.commit()
			# return f'{table_name} created'
	async def insert_info(self,table_name,column,value): # column value => list
		split_text = [f"INSERT INFO {table_name} ({','.join(column)})"]
		split_text.append(f"VALUES ({','.join(value)})")
		await self.cursor.execute('\n'.join(split_text))
		await self.sql.commit()
	async def update(self,table_name,colval,where): # colval => dict
		split_text = [f"UPDATE {table_name}","SET"]
		for column, value in colval.items():
			split_text.append(f"	{column} = {value}")
		split_text.append(f"WHERE {where}")
		await self.cursor.execute('\n'.join(split_text))
		await self.sql.commit()
	async def select_id(self,table_name,id,pdict=False):
		sqlcmd = (f"SELECT * FROM {table_name} WHERE id = {id}")
		await self.cursor.execute(sqlcmd)
		result = self.cursor.fetchall()
		description_result = self.cursor.description
		value_list = []
		for row in result:
			for i in range(len(row)):
				value_list.append(row[i])
		if pdict:
			cvdict = {}
			for index,description in enumerate(description_result):
				cvdict[description[0]] = value_list[index]
			return cvdict
		else:
			return value_list
	async def select(self,table_name,where):
		sqlcmd = (f"SELECT * FROM {table_name} WHERE {where}")
		await self.cursor.execute(sqlcmd)
		result = self.cursor.fetchall()
		description_result = self.cursor.description
		value_list = []
		for row in result:
			value_list.append(row)
		return value_list