import tornado.web
import slice
import json


class delete(tornado.web.RequestHandler):
    def initialize(self, slices):
        self.slices = slices
        
    def get(self):
    
        id = self.get_argument('id')
        result = self.books.del_slice(id)
        if result:
            self.render("delslice.html",id=id)
            print ("Deleted slice id: {0} succsessfully".format(id))
            
        else:
            print ("Slice '{0}' not found".format(id))
            
