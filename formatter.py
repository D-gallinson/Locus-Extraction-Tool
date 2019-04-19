import numpy as np

class Format():
	def __init__(self, h_df, n_df, overlap_stats_df, rename_flag):
		h_match_indices = overlap_stats_df.h_index
		n_match_indices	= overlap_stats_df.n_index
		h_df = self.__rename_cols(h_df, False)
		if rename_flag:
			n_df = self.__rename_cols(n_df, True)
		merged_df = self.__merge_dfs(h_match_indices, n_match_indices, h_df, n_df)
		self.output_df = self.__add_stats(merged_df, overlap_stats_df)


	def __rename_cols(self, df, needle):
		cols = df.columns.values
		
		if needle:
			prepend = "n_"
		else:
			prepend = "h_"
		
		new_cols = [prepend + col for col in cols]
		df.columns = new_cols
		return df

	
	def __merge_dfs(self, h_indices, n_indices, h_df, n_df):
		h_df_matches = h_df.iloc[h_indices].reset_index(drop=True)
		n_df_matches = n_df.iloc[n_indices].reset_index(drop=True)
		
		return n_df_matches.join(h_df_matches)
		

	def __add_stats(self, merged_df, overlap_stats_df):
		haystack_file_name = overlap_stats_df.haystack_file
		stats = overlap_stats_df[['needle_overlap', 'haystack_overlap', 'average']]
		merged_df.insert(0, 'haystack_file', haystack_file_name)
		
		return merged_df.join(stats)