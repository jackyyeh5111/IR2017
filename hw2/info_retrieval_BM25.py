# -*- coding: utf-8
import numpy as np
import db_operations as dbOp
from math import log, sqrt
from query_parser import getDocLength, getDocTitle


class Query:
	def __init__(self, bigram_words, q_tf_vector, idf_vector, relevant_docs):
		#self.bigram_pairs = bigram_pairs
		self.bigram_words = bigram_words
		self.q_tf_vector = q_tf_vector
		self.idf_vector = idf_vector
		self.relevant_docs = relevant_docs  
		#self.ranked_doc_names = ranked_doc_names
		#self.q_doc_ids = q_doc_ids
		#self.q_appear_nums = q_appear_nums # for idf
		#self.idf = idf
		#self.ranked_docname = ranked_docname
	def setRankedDocumentIDs(self, ranked_document_ids):
		self.ranked_document_ids = ranked_document_ids

class Document:
	def __init__(self, id, d_tf_vector):
		self.id = id
		self.d_tf_vector = d_tf_vector


class InfoRetrieval:

	def __init__(self, raw_queries, rank_num, OUTPUT_PATH):
		
		self.rank_num = rank_num
		self.raw_queries = raw_queries
		self.OUTPUT_PATH = OUTPUT_PATH

	def getBigramWordsID(self, bigram_words):

		bigram_pairs = [(dbOp.getVocabID(w1), dbOp.getVocabID(w2))
						 for w1, w2 in bigram_words]
		return bigram_pairs

	def getBigramWordsOfQuery(self, raw_query):

		words = raw_query.split(u'、')

		# process strange tokens
		words = [word.replace("\n", "").replace(" ", "").strip(u"。") \
				 for word in words]

		bigram_words = []
		for word in words:
			if len(word) < 2 : pass

			# word turn to bigram
			for i in range(len(word)-1):
				bigram_words.append((word[i], word[i+1]))

		#for word in bigram_words:
		#	print word[0], word[1]
		return bigram_words

	def getRelevantDocs(self, bigramID_pairs):
		# Besides get relevant docs, 
		# tf_vector of doc is also modified at the same time
		# because it is efficient to get (docIDs, bigramAppearNums)
		# in one operation from DB 

		relevant_docs = []
		appeared_docIDs = []
		for i, b_id_pair in enumerate(bigramID_pairs):
			docIDs, appear_nums = dbOp.getRelevantDocIDs_And_BigramAppearNums(b_id_pair)
			
			#print docIDs
			#print appear_nums
			#raw_input()
			
			for j, docID in enumerate(docIDs):
				# docID have not appeared
				if docID not in appeared_docIDs:
					doc = Document(docID, [0]*len(bigramID_pairs))
					appeared_docIDs.append(docID)
					relevant_docs.append(doc)

				toModifyIndex =  appeared_docIDs.index(docID)
				relevant_docs[toModifyIndex].d_tf_vector[i] = appear_nums[j]

				#print relevant_docs[toModifyIndex].d_tf_vector
				#raw_input()


		return relevant_docs

	
	# calculate idf weight
	def get_IDF_Vector(self, relevant_docs):
		doc_total_num = 46972  # look up file-list
		
		temp = np.array([doc.d_tf_vector for doc in relevant_docs])
		query_word_appear_nums = np.sum(temp, axis=0)

		#print query_word_appear_nums
		#print query_word_appear_nums.shape
		#raw_input() 

		idf_vector = np.log(np.divide(doc_total_num, query_word_appear_nums))

		return idf_vector
	
	def get_TF_Vector(self, bigram_words, unique_bigram_words):

		return [bigram_words.count(word) for word in unique_bigram_words]

	def printBigramWord(self, bigram_word):
		print "".join(bigram_word),

	def displayWordWithTopn_TFIDF_Weight(self, query, topn):
		
		top_tfidf_weight_words = []
		q_tfidf_vector = [a*b for a, b in zip(query.q_tf_vector, query.idf_vector)]
		for _ in range(topn):
			max_idx = q_tfidf_vector.index(max(q_tfidf_vector))
			q_tfidf_vector[max_idx] = -1
			top_tfidf_weight_words.append(query.bigram_words[max_idx])
			
		print "words with top tfidf weight: "
		for bigram_word in top_tfidf_weight_words:
			self.printBigramWord(bigram_word)

		print ("")



	def rankBySimilarity(self, query, rank_num):

		N = len(query.relevant_docs) # total number of docs in the collection

		r = np.zeros(len(query.q_tf_vector)).astype(float) # number of docs that contain the term
		for doc in query.relevant_docs:
			q_contains = np.array([1 if appear_num != 0 else 0 for appear_num in doc.d_tf_vector])
			r = r + q_contains

		dl_list = []
		for doc in query.relevant_docs: 
			doc_name = dbOp.getDocName(doc.id) 
			dl = getDocLength(doc_name) # document's length
			dl_list.append(dl)

		avdl = float(sum(dl_list)) / len(dl_list) # average doc length


		doc_similarity_scores = []
		ranked_document_ids = []
		for i, doc in enumerate(query.relevant_docs): 
			tf = np.array(doc.d_tf_vector).astype(float) # term's frequency in document
			qtf = np.array(query.q_tf_vector).astype(float) # term's frequency in query
			dl = dl_list[i]
			
			#print tf
			#print qtf
			#print dl
			#raw_input()
			similarity_score = self.score_BM25(tf, qtf, r, N, dl, avdl)
			doc_similarity_scores.append(similarity_score)

		# rank similarity
		for i in range(rank_num):
			max_idx = doc_similarity_scores.index(max(doc_similarity_scores))
			ranked_document_ids.append(query.relevant_docs[max_idx].id)
			doc_similarity_scores[max_idx] = -10000 # assign a small value
			
		return ranked_document_ids

	def score_BM25(self, tf, qtf, r, N, dl, avdl):
		# initial parameter 
		k1 = 1.5
		k2 = 500
		b = 0.75
		R = 0.0

		K = k1 * ((1-b) + b * (float(dl)/float(avdl)) )
		
		first = np.log((N - r + 0.5) / (r + 0.5))
		#first = np.log( ( (r + 0.5) / (R - r + 0.5) ) / ( (n - r + 0.5) / (N - n - R + r + 0.5)) )
		second = ((k1 + 1) * tf) / (K + tf)
		third = ((k2+1) * qtf) / (k2 + qtf)
		
		return np.sum(first * second * third)

	def run(self):

		self.Queries = []

		for i, raw_query in enumerate(self.raw_queries):

			bigram_words = self.getBigramWordsOfQuery(raw_query)
			unique_bigram_words = list(set(bigram_words)) # make bigram_words unique
			bigramID_pairs = self.getBigramWordsID(unique_bigram_words)

			relevant_docs = self.getRelevantDocs(bigramID_pairs)

			# q for query to differ from d_tf_vector
			q_tf_vector = self.get_TF_Vector(bigram_words, unique_bigram_words)
			
			# idf is shared by docs and query, don't have to differ 
			idf_vector = self.get_IDF_Vector(relevant_docs)

			query = Query(unique_bigram_words, q_tf_vector, idf_vector, relevant_docs)

			ranked_document_ids = self.rankBySimilarity(query, self.rank_num)
			

			query.setRankedDocumentIDs(ranked_document_ids)

			self.Queries.append(query)

			print ("-" * 10)
			print ("query %d completed!" % (i+1))

			# print words with top tfidf weight 
			topn = 10
			self.displayWordWithTopn_TFIDF_Weight(query, topn)
			self.displayTopnDocsTitle(query, topn)


		self.output(self.Queries)
	
	def output(self, queries):
	
		output = "query_id,retrieved_docs\n"
		for i, query in enumerate(queries):
		
			relevant_doc_names = [dbOp.getDocName(doc_id).split("/")[-1].lower() for doc_id in query.ranked_document_ids]

			output += "0" + str(i+11) + ','
			output += ' '.join(relevant_doc_names) 
			output += '\n'

		with open(self.OUTPUT_PATH, 'w') as f:
			f.write(output)
		

	def displayTopnDocsTitle(self, query, topn):
		FILE_PATH_LIST = [dbOp.getDocName(doc_id) for doc_id in query.ranked_document_ids]
		print "topn titles: "
		for i in range(topn):
			print getDocTitle(FILE_PATH_LIST[i])
		