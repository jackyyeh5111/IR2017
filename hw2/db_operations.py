# -*- coding: utf-8
import sqlite3

DB_NAME = "test.db"

def getDocName(doc_id):
		
		conn = sqlite3.connect('test.db')
		cursor = conn.execute("SELECT file_name from FILE_LIST where file_id = " + str(doc_id))	
		file_name = ""
		for row in cursor:
			file_name = row[0]
		 
		conn.close()

		return file_name

def getVocabID(vocab):

	#print vocab
	conn = sqlite3.connect(DB_NAME)
	cursor = conn.execute("SELECT vocab_id from VOCAB where vocab = \""+ vocab+ "\"")	
	vocab_id = -1
	for row in cursor:
		vocab_id = row[0] # vocab_id
	 
	conn.close()
	#print vocab_id

	return vocab_id

def getRelevantDocIDs_And_BigramAppearNums(b_id_pair):

	conn = sqlite3.connect(DB_NAME)
	cursor = conn.execute("SELECT file_id, appear_num from INVERTED_FILE \
					   where vocab_id1 = "+ str(b_id_pair[0]) +" and vocab_id2 = " + str(b_id_pair[1]))

	file_ids = [] 
	appear_nums = [] # initial
	for row in cursor:
		file_ids.append(int(row[0]))
		appear_nums.append(int(row[1]))

	conn.close()

	return (file_ids, appear_nums)
