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
FILE_PATH = os.path.join(SCRIPT_PATH, opts.MODEL_PATH, "file-list")
DB_PATH = os.path.join(SCRIPT_PATH, "test.db")
tb_name = "FILE_LIST"


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

# drop and create table

conn.execute('''CREATE TABLE FILE_LIST
       (file_id     INTEGER PRIMARY KEY     AUTOINCREMENT,
        file_name   char(35)  NOT NULL);''')
#print "Table created successfully";


with open(FILE_PATH) as f :
	for line in f.readlines():		
		line = line.replace("\n", "")
		conn.execute("INSERT INTO FILE_LIST (file_name) VALUES (\""+ line + "\")");						

print ("file_list tb  created successfully")


# id minus 1 (start from 0)
conn.execute("UPDATE FILE_LIST set file_id = file_id - 1")
conn.commit()

conn.close()