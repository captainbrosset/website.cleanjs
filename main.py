# Fixing the path so I can call modules from parent dir
import os, sys
dirname=os.path.dirname
path=os.path.join(dirname(dirname(__file__)))
sys.path.insert(0,path)

import webapp2

from handlers import home
from handlers import report

app = webapp2.WSGIApplication([
	('/report', report.ReportHandler),
	('/([a-zA-Z0-9]+)', report.ReportHandler),
	('/', home.HomeHandler)
], debug=True)