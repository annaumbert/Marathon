import tornado.web
import slice
import json

class modify(tornado.web.RequestHandler):
    def initialize(self, slices):
        self.slices = slices
    
    def get(self):
        id=self.get_argument("option")
        result=self.slices.get_slice(id)
        y=json.loads(result)
        self.render("templates/modify.html",y=y)
        
        

    def post(self):
        sli={}
        id=self.get_argument('id')
        result=self.slices.update_key('nep_vbs',self.get_argument('nep_vbs'),id)
        sli["nep_vbs"]=self.get_argument('nep_vbs')
        if result:
            print ("El valor de nep_vbs es el mismo y no se modificara")
        
        result=self.slices.update_key('nep_vue',self.get_argument('nep_vue'),id)
        sli["nep_vue"]=self.get_argument('nep_vue')    
        if result:
            print ("El valor de nep_vue es el mismo y no se modificara")
                    
        result=self.slices.update_key('channelbw_min',self.get_argument('channelbw_min'),id)
        sli["channelbw_min"]=self.get_argument('channelbw_min')    
        if result:
            print ("El valor de channelbw_min es el mismo y no se modificara")
                
        result=self.slices.update_key('channelbw_max',self.get_argument('channelbw_max'),id)
        sli["channelbw_max"]=self.get_argument('channelbw_max')
        if result:
            print ("El valor de channelbw_max es el mismo y no se modificara")
                
        result=self.slices.update_key('sharingpool',self.get_argument('channelsharingpool'),id)
        sli["channelbw_max"]=self.get_argument('channelbw_max')
        if result:
            print ("El valor de sharingpool es el mismo y no se modificara")
                
        result=self.slices.update_key('chairpolicy',self.get_argument('chairpolicy'),id)
        sli["chairpolicy"]=self.get_argument('chairpolicy')
        if result:
            print ("El valor de chairpolicy es el mismo y no se modificara")
        result=self.slices.update_key('chairminratio',self.get_argument('chairminratio'),id)
        sli["chairminratio"]=self.get_argument('chairminratio')
        if result:
            print ("El valor de chairminratio es el mismo y no se modificara")
        result=self.slices.update_key('chairmaxratio',self.get_argument('chairmaxratio'),id)
        sli["chairmaxratio"]=self.get_argument('chairmaxratio')
        if result:
            print ("El valor de chairmaxratio es el mismo y no se modificara")
        result=self.slices.update_key('chairavgint',self.get_argument('chairavgint'),id)
        sli["chairavgint"]=self.get_argument('chairavgint')
        if result:
            print ("El valor de chairavgint es el mismo y no se modificara")
        x=json.dumps(sli)
        slice.create(x)
        self.render("templates/modify2.html",id=id)
