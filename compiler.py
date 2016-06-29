import re
import os


def get_morph_files(directory, found_files=None):
	if found_files is None:
		found_files = []
	files = os.listdir(directory)
	for file in files:
		if file.endswith(".morph"):
			found_files.append(os.path.abspath(file))
	parent_dir = os.path.dirname(directory)
	if parent_dir == directory:
		return found_files
	return get_morph_files(parent_dir, found_files)


if __name__ == '__main__':
	files = get_morph_files(os.getcwd())
	print(files)
