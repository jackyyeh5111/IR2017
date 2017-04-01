# -*- coding: utf-8
from __future__ import print_function

import os
import sys
import numpy as np
import time

from query_parser import parseData
from info_retrieval_BM25 import InfoRetrieval
from optparse import OptionParser

# parse commandline arguments
op = OptionParser()
op.add_option("-r",
              dest="relevance_feedback", action="store_true", default=False,
              help="turn on the relevance feedback in program.")
op.add_option("-i",
              dest="QUERY_PATH", default="./queries",
              help="The input query file.")
op.add_option("-o",
              dest="OUTPUT_PATH", type=str,  default="./output/output.csv",
              help="The output ranked list file.")
op.add_option("-m",
              dest="MODEL_PATH", default="model",
              help="The input model directory")
op.add_option("-d", 
			  dest="NTCIR_PATH", type=str, default="./CIRB010",
              help="The directory of NTCIR documents.")

op.add_option("-t", 
			  dest="consider_title", action="store_true", default=False,
              help="Consider query's title.")

op.add_option("-q", 
			  dest="consider_quesion", action="store_true", default=False,
              help="Consider query's quesion.")

op.add_option("-n", 
			  dest="consider_narrative", action="store_true", default=False,
              help="Consider query's narrative.")

op.add_option("-c", 
			  dest="consider_concept", action="store_true", default=False,
              help="Consider query's concept.")

(opts, args) = op.parse_args()


#mode = "TRAIN"
#mode = "TEST"
mode = "DEBUG"

if mode == "TRAIN":
	QUERY_TRAIN_PATH = os.path.join(opts.QUERY_PATH, 'query-train.xml')
	training_num = 10
if mode == "TEST":
	QUERY_TRAIN_PATH = os.path.join(opts.QUERY_PATH, 'query-test.xml')
	training_num = 20

if mode == "DEBUG":
	QUERY_TRAIN_PATH = os.path.join(opts.QUERY_PATH, 'query-jacky.xml')
	training_num = 2

#vector_type = "bigram" # (unigram, bigram)
rank_num = 100 # extract top-n files to rank and output

def main():
	"""Entry Point"""
	tStart = time.time()

	raw_queries = parseData(training_num, QUERY_TRAIN_PATH)
	IR = InfoRetrieval(raw_queries, rank_num, opts.OUTPUT_PATH)
	IR.run()

	tEnd = time.time()
	print ("It cost %f sec" % (tEnd - tStart))
	


if __name__ == '__main__':
	main()