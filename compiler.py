import re
import os
import morph
from morph import rule


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


def process_file(path, rules=morph.rules):
	path = os.path.abspath(path)
	file_name, extension = os.path.splitext(path)
	if extension != ".morph":
		print("ERROR File {} extension is not .morph, please use .morph".format(path))
		exit(-1)
	input_file = open(path, "r")
	output_file = open(file_name, "w")

	input_data = input_file.read()
	for rule in rules:
		match = re.search(rule.input_regex, input_data, re.MULTILINE)
		while match is not None:
			print(match)
			match_output = rule.output
			for token in rule.tokens:
				match_output = match_output.replace("{"+token.name+"}", match.group(token.name))
			print(match_output)
			input_data = input_data[:match.start()] + match_output + input_data[match.end():]
			match = re.search(rule.input_regex, input_data)
	output_file.write(input_data)
	input_file.close()
	output_file.close()


if __name__ == '__main__':
	files = get_morph_files(os.getcwd())
	rule("if\s+(?!\(){{anything:condition}}\s*{", "if ({condition}) {")
	rule("(?<![;\{\}\n])\n", ";\n")
	process_file("test/main.c.morph")
	print(files)
