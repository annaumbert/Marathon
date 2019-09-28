import tornado.web
import slice
import json

class view(tornado.web.RequestHandler):
    def initialize(self, slices):
        self.slices = slices
    
    def post(self):
        id=self.get_argument("option")
        result=self.slices.get_slice(id)
        y=json.loads(result)
        self.render("templates/view.html",y=y)
        

