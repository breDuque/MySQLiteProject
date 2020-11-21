import sqlite3

banco = sqlite3.connect('discografia.db')

cursor = banco.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS album (
        id INTEGER PRIMARY KEY, 
        nome_album TEXT, 
        nome_banda TEXT, 
        data_album TEXT)
    """)

cursor.execute("INSERT INTO album (nome_album, nome_banda, data_album) VALUES ('Queen','Queen','13/07/1973')")

banco.commit()