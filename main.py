import pandas as pd
import numpy as np
import compare as cp
import compare as new_cp
import parse_locus as pl
import file_write as fw
import formatter as fmt
import utility as ut
import time

####################### TODO ##########################
# 1) Include overlap stats in output [COMPLETE]
#  1a) Format output based on overlap stats
#  1b) If MAX_MATCHES is exceded, keep searching and replace old matches if a new match has higher stats*
# 2) Preprocessing functions to clean CSV's with weird formatting (ie commas in locus)
# 3) Write functions (or another little tool) to clean haystack of redundant entries
# 4) Verify overlap_stats with examples that have known answers
# 5) Test tool on different files
# 6) Comment out code further, write workflow and basic documentation for the tool
# *This may be unnecessary and would technically slow down the tool (slow down would be irrelevant if the tool is very fast)
#######################################################

def main(haystack_files, needle_path, needle_direct, needle_flag, sig_flag, max_matches, margin):
	total_start = time.time()

	DIRECT_NEEDLE_FLAG = needle_flag #setting variable
	DROP_NON_SIGNIFICANT_FLAG = sig_flag #Setting variable
	MAX_MATCHES = max_matches #setting variable
	MARGIN = margin #setting variable
	NEEDLE_DIRECT = needle_direct


	#--------------------------------------------Parse Needle and Haystack Loci--------------------------------
	start = time.time()
	print("Parsing haystack and needle loci...")

	haystack_objs = []

	for file in haystack_files:
		haystack = pl.parse_loci(file)
		haystack_objs.append(haystack)

	if DIRECT_NEEDLE_FLAG:
		needle_name = NEEDLE_DIRECT #used for file_write to output the needle name in the results file
		needle = pl.parse_loci(NEEDLE_DIRECT, DIRECT_INPUT_FLAG=True)
	else:
		needle_name = needle_path #used for file_write to output the needle name in the results file
		needle = pl.parse_loci(needle_path, DIRECT_INPUT_FLAG=False)

	delta = time.time() - start
	print("Parsing execution time: %fs" % delta)
	print("--------------------------------")
	#----------------------------------------------------------------------------------------------------------

	#--------------------------------------------Compare Needles to Haystack-----------------------------------
	#--Input in this block--
	#A vector of needle chromosome numbers, a vector of needle loci start coords, and a vector of needle loci end coords
	#A vector of haystack chromosome numbers, a vector of haystack loci start coords, and a vector of haystack loci end coords

	#--Result of this block is two lists--
	#List of needle match indices (1d vector): needle_match_indices
	#List of haystack match indices (list of lists - asymetric 2d matrix): haystack_match_indices

	#--How this block works--
	#Iterate over all genes in the needle vector
	#For each iteration, pull a single needle chr#, locus start, and locus end (add margins to each end of the locus)
	#create a comparison object for each needle gene. This object takes care of searching through the haystack to find matches
	#If a match is found, append the haystack index (or indices), the needle index, and the match statistics to their corresponding lists
	start = time.time()
	print("Comparing needle(s) to haystack(s)...")

	overlap_stats = []

	for i in range(len(haystack_objs)):
		filename = ut.get_filename(haystack_objs[i].file_path, True)
		h_locus_df = haystack_objs[i].locus_df
		compare_obj = new_cp.Compare(needle.locus_df, h_locus_df, filename, max_matches, margin)
		overlap_stats.append(compare_obj.overlap_stats_df)
	
	delta = time.time() - start
	print("Done!")
	print("Comparison execution time: %fs" % delta)
	print("--------------------------------")

	#----------------------------------------------------------------------------------------------------------

	#--------------------------------------Format Match Indices------------------------------------------------
	#Result of this block is two lists:
	#A list of needle matches containing a string of the gene info (1d vector)
	#A list of haystack matches containing a string of gene info (2d list of lists - each match list contains all matches to a given needle)
	start = time.time()
	print("Formatting matches...")

	output_dfs = []
	rename_flag = True

	for i in range(len(overlap_stats)):
		overlap_stats_df = overlap_stats[i]

		if not isinstance(overlap_stats_df, pd.DataFrame):
			print("this one is empty")
			print(ut.get_filename(overlap_stats_df))
			continue

		h_df = haystack_objs[i].df
		n_df = needle.df
		output_df = fmt.Format(h_df, n_df, overlap_stats_df, rename_flag)
		output_df = output_df.output_df
		output_dfs.append(output_df)
		rename_flag = False

	output_df = ut.append_dfs(output_dfs)

	delta = time.time() - start
	print("Done!")
	print("Formatting execution time: %fs" % delta)
	print("--------------------------------")
	#----------------------------------------------------------------------------------------------------------

	#---------------------------------------------Write Matches to File----------------------------------------
	#This block writes all formatted matches to a CSV file. Nothing is returned.

	output_df.to_csv("../results/results.csv", index=False)

	#-----------------------------------------------------------------------------------------------------------

	total_delta = time.time() - total_start
	print("Total execution time: %fs" % total_delta)