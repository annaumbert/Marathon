import json
import sys, time
import hydra
import xmlrpclib
import logging
import logging.config

contshared=0
contnonshared=0
h2_ocup=0

vbs_ip="192.168.5.94"
vue1_ip="192.168.5.95"
vue2_ip="192.168.5.96"
vue3_ip="192.168.5.100"
        

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
        sli_add["channelbw_max"]=channelbw_max
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

    def exist_value(self,value):
        found=False
        for idx, slice in enumerate(self.slices):
            if slice["nep_vue"] == value:
               found=True
        return found

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
                sli_get["channelbw_max"]=slice["channelbw_max"]
                sli_get["sharingpool"]=slice["sharingpool"]
                sli_get["chairpolicy"]=slice["chairpolicy"]
                sli_get["chairminratio"]=slice["chairminratio"]
                sli_get["chairmaxratio"]=slice["chairmaxratio"]
                sli_get["chairavgint"]=slice["chairavgint"]
                
        return json.dumps(sli_get)
    def numero(self):
        uno=len(self.slices)
        return uno     
    def contador(self):
        cont=False
        count=0
                
        if  len(self.slices) == 2:
            for idx, slice in enumerate(self.slices):
                if slice["sharingpool"]=="nonshared":
                    count=count+1
                    if count == 2:
                        cont=True
                    else:
                        cont=False
        return cont
      
    
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
#       a xmlrpclib.ServerProxy, which interacts with the VBS side,
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
        self.hydra.free_resources()

    def allocate_tx(self, freq, bandwidth, gain, h_id):

        # Configure TX freq for slice
        print("Configure TX")
        spectrum_conf = hydra.rx_configuration(freq, bandwidth, False) 
        print("Spectrum Configuration")
        ret = self.hydra.request_tx_resources( spectrum_conf )

        #NOT NECESSARY WITH THE LATEST VERSION 
        #if h_id == 1:
        #    self.client.set_mul(gain)
        #    print "mul(gain)"
        #elif h_id == 2:
        #    self.client.set_mul2(gain)
        #    print "mul2(gain)"
        #else:
        #    print("ERROR: Unknown Hydra Client ID")

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

    
def create(slices,result,mf):
    ## IMPORTANT: The script ansible_hydra_client_2tx_2rx already allocated resources for transmission and reception
    ##            These resources are under the use of hydra_clients ID 1, and ID 2. The trick of this script is to connect
    ##            with the server using the same ID (1 and 2), and them releasing the resources allocated.
    ##            We can then allocate new resources from this python without impacting the slices.
    
    #Start Hydra Clients    
    # We put the IP of the machine executing the VBS (This is for the server updates)
    #hydra1 = hydra.hydra_client("192.168.5.94", 5000, 1, True)
    hydra1 = hydra.hydra_client(vbs_ip, 5000, 1, True)
    #hydra2 = hydra.hydra_client("192.168.5.94", 5000, 2, True)
    hydra2 = hydra.hydra_client(vbs_ip, 5000, 2, True)

    if mf==0 or mf==1:#Add or Modify slice (When init mf=0)
                
        freqtx=2.48e9 #Change to free spectrum space
        freqrx=2.48e9 + 3e6 #Change accordingly
        
        #Start VUE Control Connections 
        # We put the IP of the machine running the VUEs (this is for the RX updates)
        #vue1 = xmlrpclib.ServerProxy("http://192.168.5.95:8080")
        vue1 = xmlrpclib.ServerProxy("http://%s:8080" %vue1_ip)
        vue2 = xmlrpclib.ServerProxy("http://%s:8080" %vue2_ip) 
        vue3 = xmlrpclib.ServerProxy("http://%s:8080" %vue3_ip) 

        #Start VBS Control Connection
        # We put the IP of the machine running the client (this is for the client updates, mul, mul1,...)
        client = xmlrpclib.ServerProxy("http://%s:8080" %vbs_ip)
        #client = xmlrpclib.ServerProxy("http://192.168.5.94:8080")

        if hydra1.check_connection(3) == "":
            print("hydra1 could not connect to server")
            sys.exit(1)
        if hydra2.check_connection(3) == "":
           print("hydra2 could not connect to server")
           sys.exit(1)

        if result == "init":
            print "Initialising with default values"
            
            logging.info("VUE#1 control connection established")
            logging.info("VUE#2 control connection established")
            logging.info("VUE#3 control connection established")
            
            logging.info("VBS control connection established")    

            logging.info("Hydra client 1 connected to server")
            logging.info("Hydra client 2 connected to server")        
        
        else:
            print "Slice counter:"
            current=slices.numero()
            print current
            global contshared
            global contnonshared
            global h2_ocup
            y=json.loads(result)
            
            s=y['sharingpool']
            if mf==0:#Add new slice 
                if s == "shared":
                    if (contshared < 2 and contnonshared < 2) or (contshared==2 and contnonshared==0):
                        contshared= contshared+1 #Must be decreased when delete the slice
                        print "contshared"
                        print contshared
                    else:
                        print "ERROR: creation of a shared slice is not possible."
                        sys.exit(1)
                else:
                    if contnonshared <1 or (contnonshared==1 and contshared==0):
                        contnonshared=contnonshared+1 #Must be decreased when delete the slice
                        print "contador non shared"
                        print contnonshared
                    else: 
                        print "ERROR: creation of a non-shared slice is not possible."
                        sys.exit(1)
                x=y['channelbw_min']
                
            elif mf==1:#Modify slice 
                x=y['channelbw_max']
            
            bw=float(x)
            slice_id=y['id']
            ID=int(slice_id) 

            if y['nep_vue']=='vue1':
                slice_vue = vue1
                hydra_id =1
            elif y['nep_vue']=='vue2':
                slice_vue = vue2
                hydra_id =2
                h2_ocup=h2_ocup+1
            elif y['nep_vue']=='vue3':
                slice_vue = vue3
                hydra_id =2
                h2_ocup=h2_ocup+1
            else:
                print("Nep_vue does not exist")

            if hydra_id == 2:
                slice1 = Slice (ID, hydra2, client, slice_vue)
                slice1.allocate_tx(freqtx + 300e3,bw,0.05,2)
                slice1.allocate_rx(freqrx + 300e3,bw)
                slice1.allocate_rx(freqrx,bw)
            else:
                slice1 = Slice (ID, hydra1, client, slice_vue)
                slice1.allocate_tx(freqtx - 300e3,bw,0.05,1)
                slice1.allocate_rx(freqrx - 300e3,bw)

    elif mf==-1:#Delete slice 
        y=json.loads(result)
        s=y['sharingpool']
        if y['nep_vue']=='vue1':
            hydra1.free_resources()
        elif ((y['nep_vue']=='vue2' or y['nep_vue']=='vue3') and h2_ocup==1):
            hydra2.free_resources()
            h2_ocup = 0

        if s == "shared":
            contshared= contshared-1 #Decreased when delete the slice
            print "Decrease contshared counter to"
            print contshared
        else:
            contnonshared=contnonshared-1 #Decreased when delete the slice
            print "Decrease non-shared counter to"
            print contnonshared

