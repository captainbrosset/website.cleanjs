import base
from cleanjs.parsers import fileparser
from cleanjs.reviewers import reviewer
from libs import pb64
from model import report as reportdb

class ReportHandler(base.BaseHandler):
	def get(self, b64=None):
		index = pb64.decodeB64Padless(b64)
		if index:
			src_file = self.retrieve_file(index)
			self.display_report(src_file, index)
		else:
			self.redirect("/")
	
	def store_file(self, src_file):
		return reportdb.add_file(src_file)
	
	def retrieve_file(self, index):
		return reportdb.get_file(index)
	
	def display_report(self, src_code, index):
		file_data = fileparser.get_file_data_from_content("cleanjs", src_code)
		result = reviewer.review(file_data)
		
		message_bag = result["message_bag"]
		rating = result["rating"]

		lines = file_data.lines.all_lines
		lines_data = []
		for line in lines:
			messages = message_bag.get_messages_on_line(line.line_number)
			lines_data.append({"messages": messages, "message_count": len(messages), "line": line})
	
		self.writeTemplateToResponse("report.html", {
			"bag" : message_bag,
			"lines" : lines_data,
			"rating": rating,
			"pb64": pb64.encodeB64Padless(index),
			"nb_total_lines": len(lines),
			"nb_code_lines": len(file_data.lines.get_code_lines()),
			"nb_comments_lines": len(file_data.lines.get_comments_lines())
		})

	def post(self):
		src_code = self.request.get('code')
		if src_code == "":
			self.redirect("/")
		else:
			index = self.store_file(src_code)
			self.redirect("/" + pb64.encodeB64Padless(index))