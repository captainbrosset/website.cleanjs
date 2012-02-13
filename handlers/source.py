import base
from model import report as reportdb

class GetSource(base.BaseHandler):
	def get(self, id):
		source = html_escape(reportdb.get_file(id))
		self.response.out.write("<pre>"+source+"</pre>")

html_escape_table = {
	"&": "&amp;",
	'"': "&quot;",
	"'": "&apos;",
	">": "&gt;",
	"<": "&lt;",
}

def html_escape(text):
	"""Produce entities within text."""
	return "".join(html_escape_table.get(c,c) for c in text)