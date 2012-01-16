import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template

from cleanjs import fileparser
from cleanjs.messagebag import MessageBag
from cleanjs.reviewers import codesize, comments, complexity, formatting, naming, unused, general

import webapp2

class BaseHandler(webapp2.RequestHandler):
	def writeTemplateToResponse(self, tpl, data):
		path = os.path.join(os.path.dirname(__file__), "templates" + os.sep + tpl)
		self.response.headers['Content-Type'] = 'text/html'
		self.response.out.write(template.render(path, data))

class MainPage(BaseHandler):
	def get(self):
		self.writeTemplateToResponse("index.html", {})
		
	def post(self):
		file_data = fileparser.get_file_data_from_content("cleanjs", self.request.get('code'))
		
		message_bag = MessageBag()
		
		general.Reviewer().review(file_data, message_bag)
		codesize.Reviewer().review(file_data, message_bag)
		comments.Reviewer().review(file_data, message_bag)
		complexity.Reviewer().review(file_data, message_bag)
		formatting.Reviewer().review(file_data, message_bag)
		naming.Reviewer().review(file_data, message_bag)
		unused.Reviewer().review(file_data, message_bag)
	
		lines = file_data.lines.all_lines
		lines_data = []
		for line in lines:
			messages = message_bag.get_messages_on_line(line.line_number)
			lines_data.append({"messages": messages, "message_count": len(messages), "line": line})
	
		self.writeTemplateToResponse("report.html", {"bag" : message_bag, "lines" : lines_data})

app = webapp2.WSGIApplication([('/', MainPage)], debug=True)