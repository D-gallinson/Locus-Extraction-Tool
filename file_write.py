import numpy as np

def write_to_file(filename, needle_name, haystack_name, haystack_header, needle_list, haystack_list):
	needle_len = len(needle_list)
	file = open(filename, 'w')
	file.write("-----Basic run info-----\n")
	file.write("Needle: %s\n" % needle_name)
	file.write("Haystack: %s\n" % haystack_name)
	file.write("Order of overlap stats: needle overlap | haystack overlap | average\n\n")

	for m in range(needle_len):
		needle_matches = haystack_list[m]
		match_len = len(needle_matches)

		file.write(needle_list[m])
		file.write("\nMATCHES:\n")
		file.write(haystack_header + "\n")

		for i in range(match_len):
			file.write(needle_matches[i])
			file.write("\n")

		file.write("--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
	file.close()

"""
def format_needle_matches(needle_df, needle_indices):
	index_len = len(needle_indices)
	match_list = []

	for i in range(index_len):
		index = needle_indices[i]
		match = needle_df.loc[index].values
		match = escape_commas(match)
		match = ",".join(map(str, match))

		match_list.append(match)

	return match_list


def format_haystack_matches(haystack_df, haystack_indices, stats_list):
	index_len = len(haystack_indices)
	match_list = []

	for outer in range(index_len):
		matches = haystack_indices[outer]
		stats_multiple = stats_list[outer]
		matches_len = len(matches)
		matches_list = []

		for inner in range(matches_len):
			match_index = matches[inner]
			match = haystack_df.loc[match_index].values
			stats = stats_multiple[inner]
			match = np.concatenate((match, stats))
			match = escape_commas(match)
			match = ",".join(map(str, match))

			matches_list.append(match)

		match_list.append(matches_list)

	return match_list


def get_filename(path):
    last_slash = path.rfind("/") + 1
    last_dot = path.rfind(".")
    return path[last_slash : last_dot]


def escape_commas(str_list):
	for i, string in enumerate(str_list):
		if not isinstance(string, str):
			continue
		if "," in string:
			if not string.startswith("\"") or not string.endswith("\""):
				str_list[i] = "\"" + string + "\""

	return str_list


def create_results_folder():
	pass
"""