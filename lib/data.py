import os,sqlite3
class data_storage:
	def init(self,database_name):
		sql = sqlite3.connect(database_name)
		self.sql = sql
		self.cursor = sql.cursor()
	async def create_table(self,table_name,key_valuetype): #key_valuetype形式 {key:data_type,key:data_type}
		#check table ready or not
		self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
		result = self.cursor.fetchone()
		if result:
			pass
			# return "create table false, table has exists"
		else:
			split_text = list([f"CREATE TABLE {table_name} ("])
			f_pass = True
			for column, data_type in key_valuetype.items():
				if f_pass:
					split_text.append(f"\n    {column} {data_type}")
					f_pass = False
				else:
					split_text.append(f",\n    {column} {data_type}")
			split_text.append('\n)')
			self.cursor.execute(''.join(split_text))
			self.sql.commit()
			# return f'{table_name} created'
	async def insert_into(self,table_name,column,value): # column value => list
		#位字串形式的值加上單引號
		tran_values = []
		for element in value:
			if type(element) == int or type(element) == float:
				tran_values.append(f"{element}")
			else:
				tran_values.append(f"'{element}'")
		sql_cm = f"INSERT INTO {table_name} ({','.join(column)}) VALUES ({','.join(tran_values)})"
		self.cursor.execute(sql_cm)
		self.sql.commit()
	async def update(self,table_name,colval,where): # colval => dict
		split_text = list([f"UPDATE {table_name}","SET"])
		for column, value in colval.items():
			split_text.append(f"{column} = '{value}'")
		split_text.append(f"WHERE {where}")
		print('\n'.join(split_text))
		self.cursor.execute('\n'.join(split_text))
		self.sql.commit()
	async def select_id(self,table_name,id,pdict=False):
		sqlcmd = (f"SELECT * FROM {table_name} WHERE id = {id}")
		self.cursor.execute(sqlcmd)
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
		self.cursor.execute(sqlcmd)
		result = self.cursor.fetchall()
		description_result = self.cursor.description
		value_list = []
		for row in result:
			value_list.append(row)
		return value_list
	def close(self):
		self.sql.close()