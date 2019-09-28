#!/usr//bin/env python2

import sys, time

import hydra
import xmlrpclib
import logging
import logging.config
import tornado.ioloop
import tornado.web, tornado.options
import json
import os
from slice import Slice_Param



# This class receives a hydra_client, which interacts with the Hydra-Server,
#       and a xmlrpclib.ServerProxy, which interacts with the UE side.
# Use the methods to configure both the client and ue at the same time.


class Slice:
    def __init__(self,client,ue):
        self.client = client
        self.ue = ue

    
        


    #def free(self):
     #   self.client.free_resources()
    
    def allocate_tx(self, freq, bandwidth):
        print "hola"
        
        # Configure TX freq for slice
      #  spectrum_conf = hydra.rx_configuration(freq, bandwidth, False)
       # ret = self.client.request_tx_resources( spectrum_conf )

        #if (ret < 0):
        #    print "Error allocating HYDRA TX resources: freq: %f, bandwidth %f" % (freq, bandwidth) 
        #    return -1

        #  Configure the RX freq for UE (to receive from the slice)
        #self.ue.set_freqrx(freq)
        #self.ue.set_vr1offset(0)
        #self.ue.set_vr2offset(0)
        #self.ue.set_samp_rate(bandwidth)

        #if (self.ue.get_freqrx() != freq or self.ue.get_samp_rate() != bandwidth):
        #    print "Error allocating UE RX resources: freq: %f, bandwidth %f" % (freq, bandwidth) 
        #    return -1

        #return 0

    #def allocate_rx(self, freq, bandwidth):
        # Configure RX freq for slice
     #   spectrum_conf = hydra.rx_configuration(freq, bandwidth, False)
     #   ret = self.client.request_rx_resources( spectrum_conf )

        #if (ret < 0):
        #    print "Error allocating TX resources: freq: %f, bandwidth %f" % (freq, bandwidth) 

        #  Configure the RX freq for UE (to receive from the slice)
        #self.ue.set_freqtx(freq)
        #self.ue.set_vr1offset(0)
        #self.ue.set_vr2offset(0)
        #self.ue.set_samp_rate(bandwidth)

        #if (self.ue.get_freqtx() != freq or self.ue.get_samp_rate() != bandwidth):
        #    print "Error allocating UE TX resources: freq: %f, bandwidth %f" % (freq, bandwidth) 
        #    return -1

        #return 0


       
    
     

#def main():
    ## IMPORTANT: The script ansible_hydra_client_2tx_2rx already allocated resources for transmission and reception
    ##            These resources are under the use of clients ID 1 and ID 2. The trick of this script is to connect
    #           with the server using the same ID (1 and 2), and them releasing the resources allocated.
    #           We can then allocate new resources from this python without impacting the slices.

    # We put the IP of the machine executing this script
    #client1 = hydra.hydra_client("192.168.5.70", 5000, 1, True)
    # We put the IP of the machine running the UE
    #ue1 = xmlrpclib.ServerProxy("http://192.168.5.78:8080")

    #if client1.check_connection(3) == "":
    #    print("client1 could not connect to server")
    #    sys.exit(1)

    # put both the client and the ue in a slice class.
    #slice1 = Slice( client1, ue1)
    # This configuration is just to "clear" the offsets in the gnuradio file.
    # Dont remove it.
    #slice1.allocate_tx(2.43e9 - 300e3, 400e3)
    #slice1.allocate_rx(2.43e9 + 3e6 - 300e3, 400e3)

  #  if (True):
        # We put the IP of the machine executing this script
   #     client2 = hydra.hydra_client("192.168.5.70", 5000, 2, True)
        # We put the IP of the machine running the UE
    #    ue2 = xmlrpclib.ServerProxy("http://192.168.5.81:8080")

    #    if client2.check_connection(3) == "":
    #        print("client2 could not connect to server")
    #        sys.exit(1)
    #    slice2 = Slice( client2, ue2)
    #    slice2.allocate_tx(2.43e9 + 200e3, 200e3)
    #    slice2.allocate_rx(2.43e9 + 3e6 + 200e3, 200e3)
def create(id):
    
    
    client1 = hydra.hydra_client("192.168.5.70", 5000, 1, "True")
    #ue1 = xmlrpclib.ServerProxy("http://192.168.5.78:8080")
    #client2 = hydra.hydra_client("192.168.5.70", 5000, 1, True)
    #ue2 = xmlrpclib.ServerProxy("http://192.168.5.78:8080")
    


    ## IMPORTANT: The script ansible_hydra_client_2tx_2rx already allocated resources for traNsmission and reception
    ##            These resources are under the use of clients ID 1 and ID 2. The trick of this script is to connect
    #           with the server using the same ID (1 and 2), and them releasing the resources allocated.
    #           We can then allocate new resources from this python without impacting the slices. 
    


    #Start Hydra Clients          
    # We put the IP of the machine executing this script
    
    #client1 = hydra.hydra_client("192.168.5.70", 5000, 1, True)
    #if client1.check_connection(3) == "":
    #    print("client1 could not connect to server")
    #    sys.exit(1)
    logging.info("Hydra client 1 connected to server")


    # We put the IP of the machine executing this script
    #client2 = hydra.hydra_client("192.168.5.70", 5000, 2, True)
    #if client2.check_connection(3) == "":
    #    print("client2 could not connect to server")
    #    sys.exit(1)
    logging.info("Hydra client 2 connected to server")


    #Start VBS Connection
    logging.info("VBS connection established")



    #Start VUE Connections 
    # We put the IP of the machine running the UE
    #vue1 = xmlrpclib.ServerProxy("http://192.168.5.78:8080")
    logging.info("VUE#1 connection established")

    # We put the IP of the machine running the UE
    
    logging.info("VUE#2 connection established")

    # We put the IP of the machine running the UE
    
    logging.info("VUE#3 connection established")
    
    
  
