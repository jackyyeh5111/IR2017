#!/usr/bin/python
import sqlite3
import os
import sys
from optparse import OptionParser

# parse commandline arguments
op = OptionParser()
op.add_option("-m",
              dest="MODEL_PATH", default="model",
              help="The input model directory")
op.add_option("-r",
              dest="relevance_feedback", action="store_true", default=False,
              help="turn on the relevance feedback in program.")
op.add_option("-i",
              dest="QUERY_PATH", default="queries/query-jacky.xml",
              help="The input query file.")
op.add_option("-o",
              dest="OUTPUT_PATH", type=str,  default="./output/output.csv",
              help="The output ranked list file.")
op.add_option("-d", 
			  dest="NTCIR_PATH", type=str, default="./CIRB010",
              help="The directory of NTCIR documents.")
(opts, args) = op.parse_args()

SCRIPT_PATH = os.path.abspath(os.path.dirname(sys.argv[0]))
INVERTED_FILE_PATH = os.path.join(SCRIPT_PATH, opts.MODEL_PATH, "inverted-file")
DB_PATH = os.path.join(SCRIPT_PATH, "test.db")
tb_name = "INVERTED_FILE"


# open database
conn = sqlite3.connect(DB_PATH)
#print "Opened database successfully";


try:
    # drop and create table
	conn.execute("DROP table "+ tb_name +";")
	conn.commit()
	#print ("Table deleted successfully")
except:
    pass


conn.execute('''CREATE TABLE INVERTED_FILE
       (ID INTEGER PRIMARY KEY     AUTOINCREMENT,
        vocab_id1            INT    NOT NULL,
        vocab_id2            INT    NOT NULL,
        file_id              INT     NOT NULL,
        appear_num           INT     NOT NULL);''')
#print "Table created successfully";

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


print ("Inverted file created successfully")

conn.commit()
conn.close()