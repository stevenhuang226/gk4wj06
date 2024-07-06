import sqlite3, discord
from typing import Literal

TH = int | float | str
T = Literal["int", "float", "str"]


class data_storage:
    def __init__(self, database_name: str) -> None:
        self.sql = sqlite3.connect(database_name)
        self.cursor = self.sql.cursor()
        self.lssql_man = """speaktimes: -a all 顯示全部使用者的說話次數（已紀錄）
			user_name 顯示[user_name]的說話次數（已紀錄）
userid -a all 顯示全部使用者對應的id(discord)（曾經講過話的才會被紀錄）
	   user_name 顯示[user_name]的id(discord)（曾經講過話的才會被紀錄）
"""

    async def create_table_p(self, table_name: str, key_valuetype: dict[str:TH]) -> None:
        """
        輸入 table_name key_valuetype
        table_name => 要新增的表格名稱
        key_valuetype => 一個字典{鍵(col)：變數類型}
        如果table已經存在，則不作為
        """
        # check table ready or not
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
            split_text.append("\n)")
            self.cursor.execute("".join(split_text))
            self.sql.commit()
            # return f'{table_name} created'

    async def insert_into(self, table_name: str, column: list[TH], value: list[TH]) -> None:
        """
        (table_name,column,value)
        table_name => 表格名稱
        colum => 一個list [鍵(col)1,鍵(col)2]
        value => 一個list [值1,值2]
        #新增的東西均在同一個row內
        """
        tran_values = []
        for element in value:
            if type(element) == int or type(element) == float:
                tran_values.append(f"{element}")
            else:
                tran_values.append(f"'{element}'")
        sql_cm = f"INSERT INTO {table_name} ({','.join(column)}) VALUES ({','.join(tran_values)})"
        self.cursor.execute(sql_cm)
        self.sql.commit()

    async def update(self, table_name: str, colval: dict[str:TH], where: str) -> None:
        """
        (table_name,colval,where)
        table_name => table名稱
        colval => 一個字典 {要修改的鍵(col):新賦予的值}
        where => SQLite 語法，塞選條件（建議在使用時使用雙引號）
        """
        split_text = list([f"UPDATE {table_name} SET"])
        f_pass = True
        for column, value in colval.items():
            if type(value) == str:
                value = str(f"'{value}'")
            if f_pass:
                split_text.append(f"\n    {column} = {value}")
                f_pass = False
            else:
                split_text.append(f",\n    {column} = {value}")
        split_text.append(f"\nWHERE {where}")
        self.cursor.execute("".join(split_text))
        self.sql.commit()

    async def get_col(self, table_name: str) -> TH:
        """
        輸入table_name獲取col內容
        """
        sqlcmd = f"PRAGMA table_info ({table_name})"
        self.cursor.execute(sqlcmd)
        result = self.cursor.fetchall()
        col_value = [info[1] for info in result]
        return col_value

    async def append_col(self, table_name: str, new_col: str, new_col_datatype: T) -> None:
        """
        新增一個鍵(col)
        new_col => 鍵 的名稱
        new_col_datatype => 鍵 的值 的資料類型
        """
        sqlcmd = f"ALTER TABLE {table_name}\nADD {new_col} {new_col_datatype}"
        self.cursor.execute(sqlcmd)

    async def append_col_p(self, table_name: str, new_col: str, new_col_datatype: T) -> None:
        """
        新增一個鍵(col)
        new_col => 鍵 的名稱
        new_col_datatype => 鍵 的值 的資料類型
        #如果鍵已經存在，將不作為
        """
        if new_col not in await self.get_col(table_name):
            sqlcmd = f"ALTER TABLE {table_name}\nADD {new_col} {new_col_datatype}"
            self.cursor.execute(sqlcmd)

    async def select_id(self, table_name: str, id: str | int, id_name: str = "ID", pdict: bool = False) -> list[TH] | dict[str:TH]:
        """
        (table_name,id)
        table_name => table名稱
        id => 篩選的id值
        id_name => 指定id（預設為"ID"）
        pdict => True 用dict輸出（預設為False（list輸出））
        #只輸出一行，因為一個唯一id只應該出現一次
        .
        """
        sqlcmd = f"SELECT * FROM {table_name} WHERE {id_name} = {id}"
        self.cursor.execute(sqlcmd)
        result = self.cursor.fetchone()
        if result:
            description_result = self.cursor.description
            value_list = list(result)
            if pdict:
                cvdict = {}
                for index, description in enumerate(description_result):
                    cvdict[description[0]] = value_list[index]
                return cvdict
            else:
                return value_list
        else:
            return None

    async def select(self, table_name: str, where: str = None) -> list[list[TH]]:
        """
        (table_name,where)
        table_name => table名稱
        where => SQLite語法（建議用雙引號）（預設為None）
        如果where為None會獲取整個table的內容（list輸出）
        #本函式輸出一個list（依照鍵(col)的順序）
        """
        if where is None:
            self.cursor.execute(f"SELECT * FROM {table_name}")
        else:
            self.cursor.execute(f"SELECT * FROM {table_name} WHERE {where}")
        return [list(row) for row in self.cursor.fetchall()]

    def close(self) -> None:
        self.sql.close()


def tran_table_name(table_name: str):
    return f"_{table_name}"


# commands
class cmds:
    # 顯示使用者相關資料
    async def lsuser(self, message: discord.Message) -> str:
        return "\n".join(message.guild.members)

    async def lsuser_man(self) -> str:
        return "list all of member in this guild\n顯示此伺服器內的所有成員"

    # 與sql相關
    async def sql_select(self, message: discord.Message, sql_name: str, arg_list: list[str]) -> str:
        """
        message => 指令內容
        arg_list => 輸入一個list（通常為使用者輸入的指令，然後切割為list）
        回傳指令執行結果
        """
        sql = data_storage(sql_name)
        guild_id = tran_table_name(message.guild.id)
        if arg_list[0] == "speaktimes":
            if arg_list[1] in ["all", "-a", "a", "A"]:
                table = sql.select(guild_id, "speaktimes IS NOT NULL")
                speaktimes_split_text = []
                for row in table:
                    speaktimes_split_text.append(row[1], row[2])
                return "\n".join(speaktimes_split_text)
            else:
                row = sql.select(guild_id, f"name == '{arg_list[1]}'")
                return f"{row[1]} {row[2]}"
        elif arg_list[0] == "userid":
            if arg_list[1] in ["all", "-a", "a", "A"]:
                table = sql.select_all(guild_id)
                return "\n".join([" ".join([row[1], row[2]]) for row in table])
            else:
                row = sql.select(guild_id, f"name == {arg_list[1]}")
                return f"{row[1]} {row[2]}"
