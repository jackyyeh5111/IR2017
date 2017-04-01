#!/usr/bin/python
import sqlite3

# open database
conn = sqlite3.connect('test.db')
print "Opened database successfully";

# drop and create table
conn.execute("DROP table INVERTED_FILE;")
conn.commit()
print "Table deleted successfully";

conn.execute('''CREATE TABLE INVERTED_FILE
       (ID INTEGER PRIMARY KEY     AUTOINCREMENT,
        vocab_id1            INT    NOT NULL,
        vocab_id2            INT    NOT NULL,
        file_id              INT     NOT NULL,
        appear_num           INT     NOT NULL);''')
print "Table created successfully";


INVERTED_FILE_PATH = "model/inverted-file"
with open(INVERTED_FILE_PATH) as f :

	line = f.readline()
	line_num = 1
	while(line):
	
		line_split = line.split(' ')
		if len(line_split) == 3:
			vocab_id1 = line_split[0]
			vocab_id2 = line_split[1]
			file_num = int(line_split[2])

			for i in range(file_num):
				line = f.readline() # next line
				line_num += 1
				if line_num % 1000000 == 0:
					print ("read line_num:", line_num)


				line_split = line.split(' ')

				file_id = line_split[0]
				appear_num = line_split[1]
				
				# insert data
				
				conn.execute("INSERT INTO INVERTED_FILE (vocab_id1,vocab_id2,file_id,appear_num) \
							  VALUES (" + vocab_id1 + ","+ vocab_id2 +","+ file_id +","+ appear_num +")");				
				
				

		line = f.readline() # next line
		line_num += 1

		if line_num % 1000000 == 0:
			print ("read line_num:", line_num)


print "Inverted file created successfully";

conn.commit()
conn.close()