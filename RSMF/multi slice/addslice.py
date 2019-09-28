#!/usr//bin/env python2

import sys, time
import hydra
import logging
#import logging.config
import tornado.ioloop
import tornado.web, tornado.options
import slice
import json
import xmlrpclib
import os


class add(tornado.web.RequestHandler):
    def initialize(self,slices):
        self.slices=slices

    def get(self):
        cont=self.slices.contador() 
        if cont:
            self.render("templates/error_nonshared.1.html")
        else:
            res_id_1=self.slices.exist_slice("1")
            res_id_2=self.slices.exist_slice("2")
            res_id_3=self.slices.exist_slice("3")
            value1=self.slices.exist_value("vue1")
            value2=self.slices.exist_value("vue2")
            value3=self.slices.exist_value("vue3")     
            self.render("templates/addslice.html", result1 = res_id_1, result2 = res_id_2, result3= res_id_3, value1=value1 ,value2=value2, value3=value3)
        

    def post(self):
        
        rs_name=self.get_argument('rs_name')
        nep_vbs = self.get_argument('nep_vbs')
        nep_vue = self.get_argument('nep_vue')
        channelbw_min=self.get_argument('channelbw_min')
        channelbw_max=self.get_argument('channelbw_max')
        channelsharingpool=self.get_argument('channelsharingpool')
        chairpolicy=self.get_argument('chairpolicy')
        chairminratio=self.get_argument('chairminratio')
        chairmaxratio=self.get_argument('chairmaxratio')
        chairavgint=self.get_argument('chairavgint')
        if channelbw_min=="":
            channelbw_min="100000"
        if channelbw_max=="":
            channelbw_max="100000"
        res_id_1=self.slices.exist_slice("1")
        res_id_2=self.slices.exist_slice("2")
        res_id_3=self.slices.exist_slice("3")
        if not res_id_1:
            id="1"
            logging.info("Processing Slice Attributes. Deciding what to send to the corresponding Hydra clients, VBS and VUE")
            logging.info("Configuration of Hydra client1 or client2")
            # We put the IP of the machine executing this script
            #slice.create("1")
            logging.info("Configuration of vbs")
            logging.info("Configuration of vue1")
            
        elif not res_id_2:
            id="2"
            logging.info("Processing Slice Attributes. Deciding what to send to the corresponding Hydra clients, VBS and VUE")
            logging.info("Configuration of Hydra client1 or client2")
            
            logging.info("Configuration of vbs")
            logging.info("Configuration of vue2")
        elif not res_id_3:
            id="3"
            logging.info("Processing Slice Attributes. Deciding what to send to the corresponding Hydra clients, VBS and VUE")
            logging.info("Configuration of Hydra client1 or client2")
            
            logging.info("Configuration of vbs")
            logging.info("Configuration of vue3")    
                  
        else:
            id="0"
            
        if id == "0":
            self.render("templates/error_ad.html",id=id)
            print "Error. Slice" +id+ " exist. The maximun number of slices is 3." 
        else:
                slic = {
                    "id" : id,
                    "rs_name" : rs_name,
                    "nep_vbs" : nep_vbs,
                    "nep_vue" : nep_vue,
                    "channelbw_min" : channelbw_min,
                    "channelbw_max" : channelbw_max,
                    "channelsharingpool": channelsharingpool,
                    "chairpolicy" : chairpolicy,
                    "chairminratio": chairminratio,
                    "chairmaxratio" : chairmaxratio,
                    "chairavgint" : chairavgint,
                }
                      
                result=self.slices.add_slice(id,rs_name,nep_vbs,nep_vue,channelbw_min,channelbw_max,channelsharingpool,chairpolicy,chairminratio,chairmaxratio,chairavgint)
            
                slice.create(self.slices,result,0)
                logging.info("The Slice has been correctly introduced")
                self.render("templates/addslice2.html",id=id)


            
            
            
