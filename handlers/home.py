import base

class HomeHandler(base.BaseHandler):
	def get(self):
		self.writeTemplateToResponse("home.html", {})

class UploadHandler(base.BaseHandler):
	def post(self):

		self.response.out.write("<textarea>"+self.request.get("script")+"</textarea>")