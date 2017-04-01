#!/usr/bin/python
import sqlite3

# open database
conn = sqlite3.connect('test.db')
print "Opened database successfully";

# drop and create table
conn.execute("DROP table FILE_LIST;")
conn.commit()
print "Table deleted successfully";

conn.execute('''CREATE TABLE FILE_LIST
       (file_id     INTEGER PRIMARY KEY     AUTOINCREMENT,
        file_name   char(35)  NOT NULL);''')
print "Table created successfully";


INVERTED_FILE_PATH = "model/file-list"

with open(INVERTED_FILE_PATH) as f :
	for line in f.readlines():		
		line = line.replace("\n", "")
		conn.execute("INSERT INTO FILE_LIST (file_name) VALUES (\""+ line + "\")");						

print "file_list tb  created successfully";


# id minus 1 (start from 0)
conn.execute("UPDATE FILE_LIST set file_id = file_id - 1")
conn.commit()

conn.close()