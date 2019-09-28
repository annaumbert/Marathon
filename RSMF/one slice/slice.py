import json
import sys, time
import hydra
import xmlrpclib
import logging
import logging.config


class Slice_Param:

    def __init__(self):
        self.slices = []

    def add_slice(self,id,rs_name,nep_vbs,nep_vue,channelbw_min,channelbw_max,sharingpool,chairpolicy,chairminratio,chairmaxratio,chairavgint):
        sli_add = {}
        sli_add["id"]=id
        sli_add["rs_name"]=rs_name
        sli_add["nep_vbs"]=nep_vbs
        sli_add["nep_vue"]=nep_vue
        sli_add["channelbw_min"]=channelbw_min
        sli_add["channelbw_max"]=channelbw_min
        sli_add["sharingpool"]=sharingpool
        sli_add["chairpolicy"]=chairpolicy
        sli_add["chairminratio"]=chairminratio
        sli_add["chairmaxratio"]=chairmaxratio
        sli_add["chairavgint"]=chairavgint
        self.slices.append(sli_add)
        return json.dumps(sli_add)

    def del_slice(self, id):
        found = False
        for idx, slice in enumerate(self.slices):
            if slice["id"] == id:
                index = idx
                found = True
                del self.slices[idx]
        
        return found

    def get_all_slices(self):
        return self.slices
    
    def exist_slice(self,id):
        found= False
        for idx, slice in enumerate(self.slices):
            if slice["id"] == id:
                found = True
        return found

    def get_slice(self, id):
        
        for idx, slice in enumerate(self.slices):
            if slice["id"] == id:
                sli_get={}
                sli_get["id"]=slice["id"]
                sli_get["rs_name"]=slice["rs_name"]
                sli_get["nep_vbs"]=slice["nep_vbs"]
                sli_get["nep_vue"]=slice["nep_vue"]
                sli_get["channelbw_min"]=slice["channelbw_min"]
                sli_get["channelbw_max"]=slice["channelbw_min"]
                sli_get["sharingpool"]=slice["sharingpool"]
                sli_get["chairpolicy"]=slice["chairpolicy"]
                sli_get["chairminratio"]=slice["chairminratio"]
                sli_get["chairmaxratio"]=slice["chairmaxratio"]
                sli_get["chairavgint"]=slice["chairavgint"]
                
        return json.dumps(sli_get)
    
    def update_key(self,key,value,id):
       same=False
       
       for idx, slice in enumerate(self.slices):
           if slice["id"] == id:
               index=idx
               if self.slices[index][key] == value:
                   same=True
               else:
                    same=False
                    self.slices[index][key] = value
       return same


    def json_list(self):
        return json.dumps(self.slices)

# This class receives a hydra_client, which interacts with the Hydra-Server,
#       and a xmlrpclib.ServerProxy, which interacts with the UE side.
# Use the methods to configure both the client and ue at the same time.

class Slice:
    def __init__(self, id, hydra, client, ue):
        self.slice_id = id
        self.hydra = hydra
        self.client = client
        self.ue = ue
        self.freqtx = 0.0
        self.freqrx = 0.0
        self.bw = 0.0

    def free(self):
        self.client.free_resources()

    def allocate_tx(self, freq, bandwidth, gain):

        # Configure TX freq for slice
        print("Configure TX")
        spectrum_conf = hydra.rx_configuration(freq, bandwidth, False) 
        print("Spectrum Configuration")
        ret = self.hydra.request_tx_resources( spectrum_conf )

        if self.slice_id == 1:
            self.client.set_mul(gain)
        elif self.slice_id == 2:
            self.client.set_mul2(gain)
        else:
            print("ERROR: Unknown Slice ID")

        if (ret < 0):
            print "Error allocating HYDRA TX resources: freq: %f, bandwidth %f" % (freq, bandwidth)
            return -1

        #  Configure the RX freq for UE (to receive from the slice)
        self.ue.set_freqrx(freq)
        self.ue.set_vr1offset(0)
        self.ue.set_vr2offset(0)
        self.ue.set_samp_rate(bandwidth)

        if (self.ue.get_freqrx() != freq or self.ue.get_samp_rate() != bandwidth):
            print "Error allocating UE RX resources: freq: %f, bandwidth %f" % (freq, bandwidth)
            return -1

        self.freqtx = freq
        self.bw = bandwidth
        return 0

    def allocate_rx(self, freq, bandwidth):
        # Configure RX freq for slice
        spectrum_conf = hydra.rx_configuration(freq, bandwidth, False)
        ret = self.hydra.request_rx_resources( spectrum_conf )

        if (ret < 0):
            print "Error allocating RX resources: freq: %f, bandwidth %f" % (freq, bandwidth)

        #  Configure the TX freq for UE (to transmitt to the slice)
        self.ue.set_freqtx(freq)
        self.ue.set_vr1offset(0)
        self.ue.set_vr2offset(0)
        self.ue.set_samp_rate(bandwidth)

        if (self.ue.get_freqtx() != freq or self.ue.get_samp_rate() != bandwidth):
            print "Error allocating UE TX resources: freq: %f, bandwidth %f" % (freq, bandwidth)
            return -1

        self.freqrx = freq
        self.bw = bandwidth
        return 0

    
def create(result):
    
    # We put the IP of the machine executing this script (This is for the server updates)
    hydra1 = hydra.hydra_client("147.83.105.233", 5000, 1, True)
    
    # We put the IP of the machine running the UE (this is for the RX updates)
    ue1 = xmlrpclib.ServerProxy("http://147.83.105.145:8080")
    
    # We put the IP of the machine running the client (this is for the client updates)
    client1 = xmlrpclib.ServerProxy("http://147.83.105.233:8080")
    
    
    if hydra1.check_connection(3) == "":
        print("client1 could not connect to server")
        sys.exit(1)
    

    slice1 = Slice(1, hydra1, client1, ue1)
    
    freqtx=1.43e9
    freqrx=1.43e9 + 3e6 
    if result == "init":
       
       slice1.allocate_tx(freqtx , 400e3, 0.04)
       slice1.allocate_rx(freqrx , 400e3)
    else:
        
       y=json.loads(result)
       x=y['channelbw_min']
       bw=float(x)
       slice1.allocate_tx(freqtx,bw,0.05)
       slice1.allocate_rx(freqrx,bw) 
    
    

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
    
