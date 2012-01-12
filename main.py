import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

from cleanjs import fileparser
from cleanjs.messagebag import MessageBag
from cleanjs.reviewers import codesize, comments, complexity, formatting, naming, unused, general
from cleanjs.reporters import htmlwithcode

import webapp2

class MainPage(webapp2.RequestHandler):
	def get(self):
		content = """
		<!DOCTYPE html>
		<html lang="en">
			<head>
				<meta charset="utf-8">
			    <title>cleanjs report for file testscripts/goodfile.js</title>
				<style type="text/css">
					body {
						margin: 0;
						padding: 1em;
						font-size: 14px;
						font-family: 'Palatino Linotype', 'Book Antiqua', Palatino, FreeSerif, serif;
						overflow-x: hidden;
						width: 100%;
					}
					h1 {
						margin: 0;
						padding: 1em 1em 1em 25px;
					}
					p {
						margin: 0;
						padding: 1em 1em 1em 25px;
					}
					textarea {
						width: 500px;
						height: 500px;
					}
					button {
						font-size: 20px;
						font-weight: bold;
					}
				</style>
			</head>
			<body>
				<h1>cleanjs</h1>
				<p>Copy your javascript source code below and hit 'review'</p>
				<form method="post" action="/">
					<p>
						<textarea name="code"></textarea>
					</p>
					<p>
						<button type="submit">review</button>
					</p>
				</form>
			</body>
		</html>"""
		self.response.headers['Content-Type'] = 'text/html'
		self.response.out.write(content)
		
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
		
		content = htmlwithcode.output_messages(message_bag, file_data)
		
		self.response.headers['Content-Type'] = 'text/html'
		self.response.out.write(content)

app = webapp2.WSGIApplication([('/', MainPage)], debug=True)