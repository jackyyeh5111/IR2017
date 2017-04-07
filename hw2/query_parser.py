# -*- coding: utf-8
import xml.etree.ElementTree as ET

def parseData(num, FILE_PATH):

	tree = ET.parse(FILE_PATH)

	data_num = num
	query = [''] * data_num
	title_list = []
	question_list = []
	narrative_list = []
	concepts_list = []
	complete_contents = [''] * data_num
	
	for title in tree.iter(tag='title'):
	   	title_list.append(title.text)
	
	for question in tree.iter(tag='question'):
	   	question_list.append(question.text)

	for narrative in tree.iter(tag='narrative'):
	   	narrative_list.append(narrative.text)
	
	for concepts in tree.iter(tag='concepts'):
	   	concepts_list.append(concepts.text)
	

	

	for i in range(num):
		# u'、' for split words
		complete_contents[i] = title_list[i] + u'、' + question_list[i] + u'、' + \
				   narrative_list[i] + u'、' + concepts_list[i]
		#complete_contents[i] = title_list[i] + u'、' + question_list[i] + u'、' + \
		#		               narrative_list[i] 

		#query[i] = concepts_list[i]
		query[i] = question_list[i] + u'、' + concepts_list[i]
		#query[i] = title_list[i] + u'、' + question_list[i] + u'、' + \
		#		   narrative_list[i] + u'、' + concepts_list[i]

	return query, complete_contents

def getDocLength(FILE_PATH):
	# for BM25
	tree = ET.parse(FILE_PATH)
	content_list = []

	for content in tree.iter(tag='p'):
	   	content_list.append(content.text)

	return sum([len(content) for content in content_list])

def getDocTitle(FILE_PATH):
	# for BM25
	tree = ET.parse(FILE_PATH)

	for title in tree.iter(tag='title'):
	   	return title.text

	



