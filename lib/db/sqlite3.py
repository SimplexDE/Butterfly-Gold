import sqlite3

class SQLite3:
	def __init__(self, db_name):
		self.db_name = db_name
		self.conn = None
		self.cursor = None

	def __enter__(self):
		self.conn = sqlite3.connect(self.db_name)
		self.cursor = self.conn.cursor()
		return self.cursor

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.conn.commit()
		self.conn.close()

	@staticmethod
	def create_table(db_name, table_name, columns):
		with SQLite3(db_name) as cursor:
			cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({','.join(columns)});")

	@staticmethod
	def insert_into_table(db_name, table_name, columns, values):
		with SQLite3(db_name) as cursor:
			cursor.execute(f"INSERT INTO {table_name} ({','.join(columns)}) VALUES ({','.join(['?']*len(values))});", values)

	@staticmethod
	def delete_from_table(db_name, table_name, columns, values):
		with SQLite3(db_name) as cursor:
			cursor.execute(f"DELETE FROM {table_name} WHERE {columns} = {values};")

	@staticmethod
	def select_from_table(db_name, table_name, columns, values):
		with SQLite3(db_name) as cursor:
			cursor.execute(f"SELECT {','.join(columns)} FROM {table_name} WHERE {columns} = {values};")
			return cursor.fetchall()

	@staticmethod
	def update_from_table(db_name, table_name, columns, values, where):
		with SQLite3(db_name) as cursor:
			cursor.execute(f"UPDATE {table_name} SET {columns} = {values} WHERE {columns} = {where};")

	@staticmethod
	def count_rows_in_table(db_name, table_name):
		with SQLite3(db_name) as cursor:
			cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
			return cursor.fetchone()[0]

	@staticmethod
	def drop_table(db_name, table_name):
		with SQLite3(db_name) as cursor:
			cursor.execute(f"DROP TABLE IF EXISTS {table_name};")

	@staticmethod
	def drop_all_tables(db_name):
		with SQLite3(db_name) as cursor:
			cursor.execute(f"DROP TABLE IF EXISTS {table_name};")

	@staticmethod
	def create_index(db_name, table_name, columns, index_name):
		with SQLite3(db_name) as cursor:
			cursor.execute(f"CREATE INDEX IF NOT EXISTS {index_name} ON {table_name} ({','.join(columns)});")

	@staticmethod
	def drop_index(db_name, table_name, columns, index_name):
		with SQLite3(db_name) as cursor:
			cursor.execute(f"DROP INDEX IF EXISTS {index_name} ON {table_name} ({','.join(columns)});")