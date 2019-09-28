import tornado.web
import slice
import json


class get(tornado.web.RequestHandler):
    def initialize(self, slices):
        self.slices = slices
        
    def get(self):
        x=self.slices.json_list()
        y=json.loads(x)
        current=self.slices.numero()
        if y:
            self.render("templates/getslice.html",y=y,current=current)
        else:
            
            self.render("templates/getslice2.html")
        

    def post(self):#Delete slice 
        id=self.get_argument('option')
        x=self.slices.get_slice(id)
        slice.create(self.slices,x,-1)
        result=self.slices.del_slice(id)
        if result:
            self.render("templates/delslice.html",id=id)
            print "Deleted slice id: {0} successfully".format(id)    
        
        else:
            self.write("Slice '{0}' not found".format(id))
            self.set_status(404)