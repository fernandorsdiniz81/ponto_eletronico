import mysql.connector


class DataBase: #CRUD
	def __init__(self):
		self.connection = mysql.connector.connect(
		host = "localhost",
		user = "root",
		password = "seu password",
		database = "ponto_eletronico",
  		connection_timeout=60)
		self.cursor = self.connection.cursor()
   	
	def close_connection(self):
		self.cursor.close()
		self.connection.close()  

	def create(self, query):
		self.cursor.execute(query)
		self.connection.commit()
	
	def read(self, query):
		self.cursor.execute(query)
		projetos = self.cursor.fetchall()
		return  projetos
			
	def update(self, query):
		self.cursor.execute(query)
		self.connection.commit()
		
	def delete(self, query):
		self.cursor.execute(query)
		self.connection.commit()