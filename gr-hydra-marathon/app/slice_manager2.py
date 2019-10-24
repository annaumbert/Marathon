#!/usr//bin/env python2

import sys, time

import hydra
import xmlrpclib
import json



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
        self.hydra.free_resources()

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


def main():
    ## IMPORTANT: The script ansible_hydra_client_2tx_2rx already allocated resources for transmission and reception
    ##            These resources are under the use of clients ID 1 and ID 2. The trick of this script is to connect
    #           with the server using the same ID (1 and 2), and them releasing the resources allocated.
    #           We can then allocate new resources from this python without impacting the slices.

    # We put the IP of the machine executing this script (This is for the server updates)
    hydra1 = hydra.hydra_client("192.168.5.84", 5000, 1, True)
    # We put the IP of the machine running the UE (this is for the RX updates)
    ue1 = xmlrpclib.ServerProxy("http://192.168.5.91:8080")
    # We put the IP of the machine running the client (this is for the client updates)
    client1 = xmlrpclib.ServerProxy("http://192.168.5.84:8080")

    if hydra1.check_connection(3) == "":
        print("client1 could not connect to server")
        sys.exit(1)

    # put both the client and the ue in a slice class.
    slice1 = Slice(1, hydra1, client1, ue1)
    # This configuration is just to "clear" the offsets in the gnuradio file.
    # Dont remove it.
    slice1.allocate_tx(2.43e9 - 300e3, 400e3, 0.04)
    slice1.allocate_rx(2.43e9 + 3e6 - 300e3, 400e3)

    if (True):
        # We put the IP of the machine executing this script
        hydra2 = hydra.hydra_client("192.168.5.84", 5000, 2, True)
        # We put the IP of the machine running the UE
        ue2 = xmlrpclib.ServerProxy("http://192.168.5.85:8080")
        # We put the IP of the machine running the client (this is for the client updates)
        client2 = xmlrpclib.ServerProxy("http://192.168.5.84:8080")

        if hydra2.check_connection(3) == "":
            print("hydra2 could not connect to server")
            sys.exit(1)
        slice2 = Slice(2, hydra2, client2, ue2)
        slice2.allocate_tx(2.43e9 + 300e3, 200e3, 0.08)
        slice2.allocate_rx(2.43e9 + 3e6 + 300e3, 200e3)


    ## YOUR CODE HERE
    ## YOUR CODE HERE
    ## YOUR CODE HERE
    ## YOUR CODE HERE
    ## YOUR CODE HERE
    ## YOUR CODE HERE
    ## YOUR CODE HERE
    ## YOUR CODE HERE
    ## YOUR CODE HERE
    while True:
        c = ""
        try:
            c = raw_input("Type: \"1 <FREQ_SHIFT> <BW_SHIFT> <GAIN>\" to change slice 1 freq and bw. Press CTRL-C to quit.\n")

            sl, freq_shift, bw_shift, gain = c.split()
            freq_shift = float(freq_shift)
            bw_shift   = float(bw_shift)        
            gain   = float(gain)        

            if sl == "1":
                slice1.allocate_tx(slice1.freqtx + freq_shift, slice1.bw + bw_shift, gain)
                result=slice1.allocate_rx(slice1.freqrx + freq_shift, slice1.bw + bw_shift)
            elif sl == "2":
                slice2.allocate_tx(slice2.freqtx + freq_shift, slice2.bw + bw_shift, gain)
                slice2.allocate_rx(slice2.freqrx + freq_shift, slice2.bw + bw_shift)
            else:
                print("Unknown slice number")
        except KeyboardInterrupt:
            print("\n")
            return
        except:
            print(c + " : invalid configuration")


if __name__ == "__main__":
    main()

