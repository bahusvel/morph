import re

rules = []


class Rule:

	class TokenType:
		default_tokens = []

		@staticmethod
		def get_token(name, tokens=default_tokens):
			for token in tokens:
				if token.name == name:
					return token
			raise Exception("Token not found " + name)

		def __init__(self, name, regex):
			super().__init__()
			self.name = name
			self.regex = regex

	class TokenInstance:

		def generate_output_token(self):
			return "{{}}".format(self.name)

		def generate_input_token(self):
			return "{{{}:{}}}".format(self.tokentype.name, self.name)

		def generate_regex(self):
			return "(?P<{}>{})".format(self.name, self.tokentype.regex)

		def __init__(self, name, tokentype):
			super().__init__()
			self.name = name
			self.tokentype = tokentype

	def init_tokens(self):
		from_input = re.findall("\{.+\}", self.input)
		for input_token in from_input:
			token_name = input_token.strip("{}")
			splits = token_name.split(":")
			if len(splits) != 2:
				raise Exception("wrong syntax: " + self.input)
			typename = splits[0]
			instancename = splits[1]
			self.tokens.append(Rule.TokenInstance(instancename, Rule.TokenType.get_token(typename)))

	def generate_input_regex(self):
		for token_instance in self.tokens:
			regex = token_instance.generate_regex()
			input_token = token_instance.generate_input_token()
			self.input_regex = self.input_regex.replace(input_token, regex)
			print(self.input_regex)

	def run_rule(self, file):
		pass

	def __init__(self, input, output, tokens=None):
		super().__init__()
		self.input = input
		self.output = output
		self.tokens = []
		self.init_tokens()
		self.input_regex = self.input
		self.generate_input_regex()


def rule(input, output):
	rules.append(Rule(input, output))

Rule.TokenType.default_tokens.append(Rule.TokenType("anything", ".*"))

if __name__ == '__main__':
	rule("if\s{anything:condition}$", "if\s({condition}) {")
