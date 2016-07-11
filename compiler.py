import click
import re
import os
import sys
import rules


def get_rule_files(directory, found_files=None):
	if found_files is None:
		found_files = []
	files = os.listdir(directory)
	for file in files:
		if file.endswith(".morph.py"):
			found_files.append(directory + "/" + file)
	parent_dir = os.path.dirname(directory)
	if parent_dir == directory:
		return found_files
	return get_rule_files(parent_dir, found_files)


def get_morph_files(directory):
	f = []
	for (dirpath, dirnames, filenames) in os.walk(directory):
		fnames = filter(lambda fname: fname.endswith(".morph"), filenames)
		f.extend([dirpath + "/" + fname for fname in fnames])
	return f


def process_file(path, file_rules):
	file_name, extension = os.path.splitext(path)
	if extension != ".morph":
		print("ERROR File {} extension is not .morph, please use .morph".format(path))
		exit(-1)
	input_file = open(path, "r")
	output_file = open(file_name, "w")

	input_data = input_file.read()
	for file_rule in file_rules:
		match = re.search(file_rule.input_regex, input_data, re.MULTILINE)
		while match is not None:
			match_output = file_rule.output
			for token in file_rule.tokens:
				match_output = match_output.replace("{"+token.name+"}", match.group(token.name))
			print("{}: {} matched {} -> {}".format(input_data.count('\n', 0, match.start()) + 1, file_rule, rules.escape(match.group(0)), rules.escape(match_output)))
			input_data = input_data[:match.start()] + match_output + input_data[match.end():]
			match = re.search(file_rule.input_regex, input_data)
	output_file.write(input_data)
	input_file.close()
	output_file.close()


def load_rule_file(path):
	version = sys.version_info
	if version[0] == 3:
		if version[1] <= 4:
			from importlib.machinery import SourceFileLoader
			SourceFileLoader("module.name", path).load_module()
		elif version[1] >= 5:
			import importlib.util
			spec = importlib.util.spec_from_file_location("module.name", path)
			module = importlib.util.module_from_spec(spec)
			spec.loader.exec_module(module)
	else:
		raise Exception("Python version != 3.X not supported")


@click.group()
def morph():
	print("Welcome to Morph!")


@click.command()
@click.argument("directory", default=".")
def clean(directory):
	directory = os.path.abspath(directory)
	files = get_morph_files(directory)
	for file in files:
		file_name, _ = os.path.splitext(file)
		if os.path.exists(file_name):
			print("Cleaned: {}".format(file_name))
			os.remove(file_name)


@click.command()
@click.argument("directory", default=".")
@click.pass_context
def compile(ctx, directory):
	ctx.invoke(clean, directory=directory)
	directory = os.path.abspath(directory)
	files = get_morph_files(directory)
	for file in files:
		rule_files = get_rule_files(os.path.dirname(file))
		rules.rules = []
		for rule_file in rule_files:
			load_rule_file(rule_file)
		print("Processing {} using {}:".format(file, rules.rules))
		process_file(file, rules.rules)


morph.add_command(compile)
morph.add_command(clean, name='clean')

if __name__ == '__main__':
	morph()
