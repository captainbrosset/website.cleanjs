import base

class HomeHandler(base.BaseHandler):
	def get(self):
		self.writeTemplateToResponse("home.html", {})