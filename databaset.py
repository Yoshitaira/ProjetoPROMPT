import sqlite3

conn = sqlite3.connect("projectdbt.db")
cursor = conn.cursor()
cursor.fetchone

print("Conectado ao banco de dados...")