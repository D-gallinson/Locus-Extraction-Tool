import numpy as np
import pandas as pd
import re

################################################################
#-------------------------CLASS VARIABLES-----------------------
# 1) df - contains the input file in a dataframe
# 2) locus_df - contains the parsed loci information as follows:
#  2a) locus_df.chr - the chromosome number of the locus (dtype=object) 
#  2b) locus_df.start - the starting integer of the locus (dtype=int64)
#  2c) locus_df.end - the ending integer of the locus (dtype=int64)
# 3) dropped_rows - dataframe of all rows that contained improperly formatted loci entries
# 4) locus_col_name - name of the locus column for all input files
# 5) file_path - path to the given file
#
#-------------------------CLASS METHODS-------------------------
# 1) __get_file_type(file) - obtains the file extension of a string
# 2) __drop_invalid() - drops rows that have improperly formatted loci
# 3) __parse_loci() - parses a locus into the chr#, start, and end
#
#------------------------CONSTRUCTOR----------------------------
# 1) create the initial dataframe in one of two ways:
#  1a) direct input - create a dataframe with 1 col and the locus input
#  1b) file upload - read the input file and create a dataframe from it
#   1b1) obtain the filetype using __get_filetype(file)
#   1b2) based on the file type, read in the file in one of 3 ways:
#   1b3) read_csv(), read_table(), or read_excel() (pandas functions)
# 2) drop rows with NaN locus entries using dropna (pandas function)
# 3) *drop non-significant differential expression rows (*user specified)
# 4) drop rows with improperly formatted loci using __drop_invalid()
# 5) create locus_df using __parse_loci()
################################################################

class parse_loci():

	def __init__(self, fname, locus_col_name="locus", DIRECT_INPUT_FLAG=False, SIGNIFICANT_FLAG=False):
		self.locus_col_name = locus_col_name
		self.file_path = fname

		if DIRECT_INPUT_FLAG:
			self.df = pd.DataFrame(data={'locus': [fname]})
		else:
			filetype = self.__get_file_type(fname)

			if filetype == "csv":
				self.df = pd.read_csv(fname)
			elif filetype == "tabular":
				self.df = pd.read_table(fname)
			else:
				self.df = pd.read_excel(fname)

			self.df.dropna(subset=[locus_col_name], inplace=True)
			
			#Preprocessing - omit haystack values that were not significantly differentially expressed
			if SIGNIFICANT_FLAG:
				self.df = self.df[self.df.significant == "yes"]

		self.__drop_invalid()
		self.__parse_loci()



	#INPUT: filename with extension
	#OUTPUT: extension (returned)
	def __get_file_type(self, file):
		dot_index = file.rfind(".") + 1 #+1 to skip over dot
		file_len = len(file)
		filetype = file[dot_index : file_len].lower()
		return filetype



	#INPUT: raw df from file (class variable)
	#OUTPUT: same df with invalid locus rows dropped (class variable)
	def __drop_invalid(self):
		self.df ['locus'] = self.df['locus'].str.lower()
		chr_search = self.df["locus"].str.find("chr")
		self.dropped_rows = self.df[(chr_search == -1) & (pd.isna(chr_search) == True)]
		self.df = self.df[(chr_search != -1) & (pd.isna(chr_search) == False)]



	#INPUT: file df containing no invalid loci rows (class variable)
	#OUTPUT: locus df containing each loci's chr#, start, and end (class variable)
	def __parse_loci(self):
		loci = self.df[self.locus_col_name].str.replace(",", "")
		loci = loci.str.lower()
		self.locus_df = pd.DataFrame([re.split(":|-", locus) for locus in loci], columns=['chr', 'start', 'end'])
		self.locus_df['start'] = self.locus_df['start'].astype('int64')
		self.locus_df['end'] = self.locus_df['end'].astype('int64')