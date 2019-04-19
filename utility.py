def get_filename(name, extension=False):
	last_slash = name.rfind("/") + 1
	last_dot = name.rfind(".")
	
	if extension:
		name = name[last_slash : len(name)]
	else:
		name = name[last_slash : last_dot]

	return name


def get_filenames(paths, extension=False):
	names = []

	for path in paths:
		name = get_filename(path, extension)
		names.append(name)

	return names



def append_dfs(df_list):
	merged_df = df_list[0]
	df_list = df_list[1:]

	for df in df_list:
		merged_df = merged_df.append(df)

	return merged_df