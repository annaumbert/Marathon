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
        value1=self.slices.exist_value("vue1")
        value2=self.slices.exist_value("vue2")
        value3=self.slices.exist_value("vue3") 
        self.render("templates/modify.html",y=y,value1=value1,value2=value2,value3=value3)
        
        

    def post(self):
        sli={}
        id=self.get_argument('id')
        result=self.slices.update_key('nep_vbs',self.get_argument('nep_vbs'),id)
        sli["nep_vbs"]=self.get_argument('nep_vbs')
        if result:
            print ("Same nep_vbs")
        
        result=self.slices.update_key('nep_vue',self.get_argument('nep_vue'),id)
        sli["nep_vue"]=self.get_argument('nep_vue')    
        if result:
            print ("Same nep_vue")
                    
        result=self.slices.update_key('channelbw_min',self.get_argument('channelbw_min'),id)
        sli["channelbw_min"]=self.get_argument('channelbw_min')    
        if result:
            print ("Same channelbw_min")
                
        result=self.slices.update_key('channelbw_max',self.get_argument('channelbw_max'),id)
        sli["channelbw_max"]=self.get_argument('channelbw_max')
        if result:
            print ("Same channelbw_max")
                
        result=self.slices.update_key('sharingpool',self.get_argument('channelsharingpool'),id)
        sli["sharingpool"]=self.get_argument('channelsharingpool')
        if result:
            print ("Same sharingpool")
                
        result=self.slices.update_key('chairpolicy',self.get_argument('chairpolicy'),id)
        sli["chairpolicy"]=self.get_argument('chairpolicy')
        if result:
            print ("Same chairpolicy")
        result=self.slices.update_key('chairminratio',self.get_argument('chairminratio'),id)
        sli["chairminratio"]=self.get_argument('chairminratio')
        if result:
            print ("Same chairminratio")
        result=self.slices.update_key('chairmaxratio',self.get_argument('chairmaxratio'),id)
        sli["chairmaxratio"]=self.get_argument('chairmaxratio')
        if result:
            print ("Same chairmaxratio")
        result=self.slices.update_key('chairavgint',self.get_argument('chairavgint'),id)
        sli["chairavgint"]=self.get_argument('chairavgint')
        if result:
            print ("Same chairavgint")
        #x=json.dumps(sli)
        x=self.slices.get_slice(id)
        slice.create(self.slices,x,1)
        self.render("templates/modify2.html",id=id)
