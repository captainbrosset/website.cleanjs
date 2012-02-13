import unicodedata

import base
from cleanjs.parsers import fileparser
from cleanjs.reviewers import reviewer
from libs import pb64
from model import report as reportdb

class ReportByIdHandler(base.BaseHandler):
	def get(self, id):
		self.redirect("/" + pb64.encodeB64Padless(id))

class ReportHandler(base.BaseHandler):
	def get(self, b64=None):
		index = pb64.decodeB64Padless(b64)
		if index:
			src_file = self.retrieve_file(index)
			if src_file:
				self.display_report(src_file, index)
			else:
				self.redirect("/")
		else:
			self.redirect("/")
	
	def store_file(self, src_file):
		return reportdb.add_file(src_file)
	
	def retrieve_file(self, index):
		return reportdb.get_file(index)
	
	def display_report(self, src_code, index):
		try:
			file_data = fileparser.get_file_data_from_content("cleanjs", src_code)

			result = reviewer.review(file_data)

			message_bag = result.message_bag
			rating = result.rate

			lines = file_data.lines.all_lines
			file_lines = []
			for line in lines:
				messages = message_bag.get_messages_on_line(line.line_number)
				file_lines.append({"messages": messages, "message_count": len(messages), "line": line})
		
			reportdb.add_file_to_global_stats(src_code, file_data, rating, message_bag)

			self.writeTemplateToResponse("report.html", {
				"bag" : message_bag,
				"lines" : file_lines,
				"rating": rating,
				"pb64": pb64.encodeB64Padless(index),
				"nb_total_lines": len(lines),
				"nb_code_lines": len(file_data.lines.get_code_lines()),
				"nb_comments_lines": len(file_data.lines.get_comments_lines())
			})
		except Exception as error:
			self.writeTemplateToResponse("error.html", {"error": error})

	def post(self):
		src_code = self.request.get('code')
		src_code = unicodedata.normalize('NFKD', src_code).encode('ascii','ignore')
		
		if src_code == "":
			self.redirect("/")
		else:
			index = self.store_file(src_code)
			self.redirect("/" + pb64.encodeB64Padless(index))