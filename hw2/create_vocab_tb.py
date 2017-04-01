#!/usr/bin/python
#-*-encoding:utf-8-*-
import sqlite3

db_name = 'test.db'
tb_name = "VOCAB"
VOCAB_FILE_PATH = "model/vocab.all"

# open database
conn = sqlite3.connect(db_name)
print "Opened database successfully";


try:
    # drop and create table
	conn.execute("DROP table "+ tb_name +";")
	conn.commit()
	print "Table deleted successfully";
except:
    pass

# create table
conn.execute('''CREATE TABLE VOCAB
       (vocab_id     INTEGER PRIMARY KEY     AUTOINCREMENT,
        vocab        char(60)  NOT NULL);''')
print "Table created successfully";



line_num = 1
with open(VOCAB_FILE_PATH) as f :
	for line in f.readlines():		
		print line_num
		line = line.replace("\n", "")
		conn.text_factory = str  
		if line_num == 1902:
			conn.execute("INSERT INTO VOCAB (vocab) VALUES (\'"+ line + "\')");						
		else:
			conn.execute("INSERT INTO VOCAB (vocab) VALUES (\""+ line + "\")");						
		
		line_num += 1

print "VOCAB tb  created successfully";

# id minus 1 (start from 0)
conn.execute("UPDATE VOCAB set vocab_id = vocab_id - 1")
conn.commit()


conn.close()