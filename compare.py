import pandas as pd
import numpy as np

class Compare():
	def __init__(self, n_locus_df, h_locus_df, filename, max_matches, margin):
		self.MAX_MATCHES = max_matches
		self.MARGIN = margin
		self.empty_needles = []
		self.overlap_stats = []

		for i in range(len(n_locus_df)):
			needle = n_locus_df.iloc[i]
			needle_index = n_locus_df.iloc[[i]].index.values[0]
			chr_num = needle['chr']
			n_start = needle['start']
			n_end = needle['end']

			search_space = h_locus_df[h_locus_df.chr == chr_num]
			search_space_indices = search_space.index.values
			
			if search_space.empty:
				self.empty_needles.append(n_locus_df.iloc[[i]].index.values[0])
				continue
			
			h_start_vec = search_space['start']
			h_end_vec = search_space['end']

			overlap_df = self.__calc_overlap(search_space_indices, n_start, n_end, h_start_vec, h_end_vec)
			status_lookup_df = self.__determine_overlap(overlap_df)
			
			if not status_lookup_df.empty:
				self.__calc_overlap_stats(status_lookup_df, needle_index)

		if self.overlap_stats:
			self.overlap_stats_df = pd.DataFrame(self.overlap_stats, columns=self.overlap_stats[0].keys())
			self.overlap_stats_df['haystack_file'] = filename
		else:
			self.overlap_stats_df = filename

		

	def __calc_overlap(self, h_index, n_start, n_end, h_start_vec, h_end_vec):
		n_start -= self.MARGIN if (n_start - self.MARGIN) > 0 else 1
		n_end += self.MARGIN
		n_len = (n_end - n_start) + 1
		h_len = (h_end_vec - h_start_vec) + 1

		nl_hl = n_start - h_start_vec
		nr_hr = n_end - h_end_vec
		nl_hr = n_start - h_end_vec
		nr_hl = n_end - h_start_vec

		return pd.DataFrame({'h_index': h_index,'nl_hl': nl_hl, 'nr_hr': nr_hr, 'nl_hr': nl_hr, 'nr_hl': nr_hl, 'n_len': n_len, 'h_len': h_len})



	def __determine_overlap(self, overlap_df):
		conditions = [
			(overlap_df.nl_hl == 0) & (overlap_df.nr_hr == 0),
			(overlap_df.nl_hl < 0) & (overlap_df.nr_hr < 0) & (overlap_df.nr_hl > 0),
			(overlap_df.nl_hl > 0) & (overlap_df.nr_hr > 0) & (overlap_df.nl_hr < 0),
			(overlap_df.nl_hl <= 0) & (overlap_df.nr_hr >= 0),
			(overlap_df.nl_hl >= 0) & (overlap_df.nr_hr <= 0),
			(overlap_df.nr_hl == 0) | (overlap_df.nl_hr == 0)
		]
		choices = ['complete', 'needle_l', 'needle_r', 'needle_out', 'needle_in', 'end-end']
		overlap_df['overlap'] = np.select(conditions, choices, default='none')
		overlap_df = overlap_df[overlap_df.overlap != "none"]
		return overlap_df



	def __determine_overlap_old(self, overlap_df):
		status_lookup = {}
		num_matches = 0
		print("--------------------------------")
		print("n_index: %s" % overlap_df.n_index.iloc[0])

		for i in range(len(overlap_df)):
			if i % 1000 == 0:
				print("iteration %d" % i)

			if num_matches >= self.MAX_MATCHES and self.MAX_MATCHES != 0:
				break

			row = overlap_df.iloc[i]
			index = overlap_df.iloc[[i]].index.values[0]
			flag = True

			if row.nl_hl == 0 and row.nr_hr == 0:
				status = "complete"
			elif row.nl_hl < 0 and row.nr_hr < 0 and row.nr_hl > 0:
				status = "needle_l"
			elif row.nl_hl > 0 and row.nr_hr > 0 and row.nl_hr < 0:
				status = "needle_r"
			elif row.nl_hl <= 0 and row.nr_hr >= 0:
				status = "needle_out"
			elif row.nl_hl >= 0 and row.nr_hr <= 0:
				status = "needle_in"
			elif row.nr_hl == 0 or row.nl_hr == 0:
				status = "end-end"
			else:
				flag = False
				status = "none"

			if flag:
				num_matches += 1
				status_lookup[index] = status
			
		dict_df = pd.DataFrame.from_dict(status_lookup, orient="index", columns=['overlap'])
		status_lookup_df = overlap_df.join(dict_df)
		status_lookup_df = status_lookup_df[pd.notnull(status_lookup_df.overlap)]
		return status_lookup_df
	


	def __calc_overlap_stats(self, status_lookup_df, n_index):
		for i in range(len(status_lookup_df)):
			overlap_stats = {}
			row = status_lookup_df.iloc[i]
			h_index = status_lookup_df.iloc[[i]].index.values[0]

			if row.overlap == "complete" or row.overlap == "needle_in":
				overlap_bp = row.n_len
			elif row.overlap == "needle_l":
				overlap_bp = row.nr_hl + 1
			elif row.overlap == "needle_r":
				overlap_bp = -row.nl_hr + 1
			elif row.overlap == "needle_out":
				overlap_bp = row.h_len
			elif row.overlap == "end-end":
				overlap_bp = 1
			else:
				return "error"

			needle_overlap = (overlap_bp / row.n_len) * 100
			haystack_overlap = (overlap_bp / row.h_len) * 100
			average = (needle_overlap + haystack_overlap) / 2

			needle_overlap = str(round(needle_overlap, 1)) + "%"
			haystack_overlap = str(round(haystack_overlap, 1)) + "%"
			average = str(round(average, 1)) + "%"

			overlap_stats['n_index'] = n_index
			overlap_stats['h_index'] = row.h_index
			overlap_stats['needle_overlap'] = needle_overlap
			overlap_stats['haystack_overlap'] = haystack_overlap
			overlap_stats['average'] = average
			self.overlap_stats.append(overlap_stats)