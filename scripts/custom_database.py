
import sqlite3
class database():
    def __init__(self,database_name):
        try:
            self.sqliteConnection = sqlite3.connect(database_name) #database name <something>.db
            self.sqliteConnection.cursor().execute("PRAGMA foreign_keys = ON;")
            self.sqliteConnection.cursor().execute("PRAGMA DTHREADSAFE = 2;")
            self.sqliteConnection.cursor().close()
        except:
            pass
 
    
    def run(self,query):
        self.cursor = self.sqliteConnection.cursor()
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        self.sqliteConnection.commit()
        self.cursor.close()
        return result