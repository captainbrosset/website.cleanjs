import webapp2
import os

from google.appengine.ext.webapp import template

class BaseHandler(webapp2.RequestHandler):
	def writeTemplateToResponse(self, tpl, data):
		path = os.path.join(os.path.dirname(__file__), ".." + os.sep + "templates" + os.sep + tpl)
		self.response.headers['Content-Type'] = 'text/html'
		self.response.out.write(template.render(path, data))