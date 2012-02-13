# Fixing the path so I can call modules from parent dir
import os, sys
dirname=os.path.dirname
path=os.path.join(dirname(dirname(__file__)))
sys.path.insert(0,path)

import webapp2

from handlers import home
from handlers import report
from handlers import source

app = webapp2.WSGIApplication([
	('/upload', home.UploadHandler),
	('/report', report.ReportHandler),
	('/r/([0-9]+)', report.ReportByIdHandler),
	('/s/([0-9]+)', source.GetSource),
	('/([a-zA-Z0-9]+)', report.ReportHandler),
	('/', home.HomeHandler)
], debug=True)