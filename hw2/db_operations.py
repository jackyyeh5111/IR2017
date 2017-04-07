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

def getRelevantDocIDs_And_BigramAppearNums(word_id_pair):

	if len(word_id_pair) == 2:
		conn = sqlite3.connect(DB_NAME)
		cursor = conn.execute("SELECT file_id, appear_num from INVERTED_FILE \
						   where vocab_id1 = "+ str(word_id_pair[0]) +" and vocab_id2 = " + str(word_id_pair[1]))

		file_ids = [] 
		appear_nums = [] # initial
		for row in cursor:
			file_ids.append(int(row[0]))
			appear_nums.append(int(row[1]))

		conn.close()

	elif len(word_id_pair) == 3:
		# split trigram id into 2 bigram id and find the 
		# relevance file_id of which,
		# and then "AND" file_id1, file_id2 is the 
		# relevace file_id of trigram

		bigram_id_pair_1 = (word_id_pair[0], word_id_pair[1])
		bigram_id_pair_2 = (word_id_pair[1], word_id_pair[2])

		conn = sqlite3.connect(DB_NAME)
		cursor = conn.execute("SELECT file_id, appear_num from INVERTED_FILE \
						   where vocab_id1 = "+ str(bigram_id_pair_1[0]) +" and vocab_id2 = " + str(bigram_id_pair_1[1]))

		file_ids_1 = [] 
		appear_nums = [] # initial
		for row in cursor:
			file_ids_1.append(int(row[0]))
			appear_nums.append(int(row[1]))

		cursor = conn.execute("SELECT file_id from INVERTED_FILE \
						   where vocab_id1 = "+ str(bigram_id_pair_2[0]) +" and vocab_id2 = " + str(bigram_id_pair_2[1]))
		file_ids_2 = []
		for row in cursor:
			file_ids_2.append(int(row[0]))
			
		#print "file_ids_1: ", file_ids_1
		#print "appear_nums: ", appear_nums
		#print "file_ids_2: ", file_ids_2


		# AND file_id1, file_id2
		delete_indexs= [idx for idx, file_id in enumerate(file_ids_1) if file_id not in file_ids_2]
		shift = 0
		for idx in delete_indexs:
			del file_ids_1[idx-shift]
			del appear_nums[idx-shift]
			shift += 1

		file_ids = file_ids_1 # final file ids to return
		#print "file_ids: ", file_ids

		conn.close()

	else:
		print ("fuck!!!!!")

	return (file_ids, appear_nums)
