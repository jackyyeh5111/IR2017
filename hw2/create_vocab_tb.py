#!/usr/bin/python
#-*-encoding:utf-8-*-
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


db_name = 'test.db'
tb_name = "VOCAB"

SCRIPT_PATH = os.path.abspath(os.path.dirname(sys.argv[0]))
VOCAB_FILE_PATH = os.path.join(SCRIPT_PATH, opts.MODEL_PATH, "vocab.all")
DB_PATH = os.path.join(SCRIPT_PATH, "test.db")

# open database
conn = sqlite3.connect(db_name)
#print ("Opened database successfully")


try:
    # drop and create table
	conn.execute("DROP table "+ tb_name +";")
	conn.commit()
	#print ("Table deleted successfully")
except:
    pass

# create table
conn.execute('''CREATE TABLE VOCAB
       (vocab_id     INTEGER PRIMARY KEY     AUTOINCREMENT,
        vocab        char(60)  NOT NULL);''')


line_num = 1
with open(VOCAB_FILE_PATH) as f :
	for line in f.readlines():		
		#print (line_num)
		line = line.replace("\n", "")
		conn.text_factory = str  
		if line_num == 1902:
			conn.execute("INSERT INTO VOCAB (vocab) VALUES (\'"+ line + "\')");						
		else:
			conn.execute("INSERT INTO VOCAB (vocab) VALUES (\""+ line + "\")");						
		
		line_num += 1

print ("Table VOCAB created successfully")

# id minus 1 (start from 0)
conn.execute("UPDATE VOCAB set vocab_id = vocab_id - 1")
conn.commit()


conn.close()