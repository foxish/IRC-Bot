import sqlite3

class DBHelper(object):
    def __init__(self, db_file, table_name):
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()    
        self.table_name = table_name
        self.db_file = db_file
        self.cur.execute('CREATE TABLE IF NOT EXISTS {0} (Type TEXT, Time INT, Value INT)'.format(table_name))
        
        
    def add_entry(self, typ, time, value):
        self.cur.execute('INSERT INTO ' + self.table_name + ' VALUES(?,?,?)', (typ, time, value))
        self.conn.commit()
        
    def get_categories_count(self, start_time, end_time, limit):
        self.cur.execute("""SELECT Value, count(Type) as ct FROM """ + self.table_name + """
                                                        WHERE Time between ? AND ?
                                                        GROUP BY Value
                                                        ORDER BY ct DESC LIMIT ?""", (start_time, end_time, limit))
        return self.cur.fetchall()

    def get_category_count(self, start_time, end_time, value):
        self.cur.execute("""SELECT count(Type) as ct FROM """ + self.table_name + """
                                                        WHERE Time between ? AND ?
                                                            AND Value LIKE ?
                                                        GROUP BY Value
                                                        ORDER BY ct""", (start_time, end_time, value))
        return self.cur.fetchall()[0][0]
