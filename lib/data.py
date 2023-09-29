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
	async def create_table(self,table_name,dict(key_valuetype)): #key_valuetype形式 {key:data_type,key:data_type}
		#check table ready or not
		self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
		result = self.cursor.fetchone()
		if result:
			pass
			# return "create table false, table has exists"
		else:
			split_text = [f'CREATE TABLE {table_name} (']
			for column, data_type in key_valuetype.items():
				split_text.append(f"	{column} {data_type},")
			split_text.append(')')
			self.cursor.execute('\n'.join(split_text))
			self.sql.commit()
			# return f'{table_name} created'
	async def insert_info(self,table_name,list(column),list(value)):
		pass
	async def update(self,table_name,list(column),list(value),str(where)):
		pass
	async def sync(self,table_name,list(column),list(value),str(where)='new'):
		pass
	async def select_fr_id(self.table_name,data_id):
		pass
	async def select_sc(self,tale_name,column_name):
		pass
	