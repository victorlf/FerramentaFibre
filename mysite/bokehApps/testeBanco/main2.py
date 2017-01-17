import sqlite3

#conn = sqlite3.connect('/home/victor/db.sqlite3')
#print "Opened database successfully";
#conn2 = conn.cursor()
#conn2.execute('''CREATE TABLE COMPANY3
#       (ID INT PRIMARY KEY     NOT NULL,
#       NAME           TEXT    NOT NULL,
#       AGE            INT     NOT NULL,
#       ADDRESS        CHAR(50),
#       SALARY         REAL);''')
#print "Table created successfully";
#conn.commit()
#conn.close()
#onn.close()
con = sqlite3.connect('db.sqlite3')
cursor = con.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())