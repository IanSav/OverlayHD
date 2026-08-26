from sys import argv
from os import listdir
from os.path import basename, isdir, join
from re import compile
from xml.sax import make_parser
from xml.sax.handler import ContentHandler, LexicalHandler, property_lexical_handler


class parse_xml(ContentHandler, LexicalHandler):
	def __init__(self, attributes):
		self.attributes = attributes
		self.lastComment = None
		self.isHex = compile(r'#[0-9a-fA-F]+\Z')
		self.locator = None

	def setDocumentLocator(self, locator):
		self.locator = locator

	def comment(self, comment):
		if "TRANSLATORS:" in comment:
			self.lastComment = comment

	def startElement(self, tag, attribs):
		for attribute in ["text", "title", "value", "caption", "description", "red", "green", "yellow", "blue"]:  # Attributes that need to be translated.
			try:
				value = attribs[attribute]
				if value.strip() != "" and not self.isHex.match(value):
					line = self.locator.getLineNumber() if self.locator else 0
					context = "%s attribute '%s'" % (tag, attribute)
					self.attributes.add((value, self.lastComment, context, line))
					self.lastComment = None
			except KeyError:
				pass


def po_escape(value):
	return value.replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", "\\n")


excludeFiles = ["dnsservers.xml"]


def parse_file(file):
	attributes = set()
	parser = make_parser()
	content_handler = parse_xml(attributes)
	parser.setContentHandler(content_handler)
	parser.setProperty(property_lexical_handler, content_handler)
	parser.parse(file)
	return attributes


for arg in argv[1:]:
	if isdir(arg):
		files = [join(arg, f) for f in listdir(arg) if f.endswith(".xml")]
	else:
		files = [arg]
	attributes = set()
	for file in files:
		if basename(file) not in excludeFiles:
			attributes.update(parse_file(file))
	attributes = list(attributes)
	attributes.sort(key=lambda x: x[0])
	for (key, translator_comment, context, line) in attributes:
		print()
		if line:
			print(f"#: {arg}:{line}")
		else:
			print(f"#: {arg}")
		print(f"#. XML context: {context}")
		if translator_comment:
			for comment_line in translator_comment.split("\n"):
				print(f"#. {comment_line.strip()}")
		print(f"msgid \"{po_escape(key)}\"")
		print("msgstr \"\"")
	attributes = set()
