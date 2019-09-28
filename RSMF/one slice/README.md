#RSMF one slice
This code implements the first operational version of the RSMF that allows to create, modify and delete only one slice.

Before starting the RSMF you must run the hydra components (hydra_server, hydra_vr1_rx, hydra_vr2_rx, hydra_vr3_rx and hydra_client_2tx_rx).

Then you must edit the file slice.py and change the IPaddresses of the machines running the VBS, and VUEs.

Now you can run the RSMF:

```
sudo python rsmf.py
```

Open a web browser and go to:

```
*IP_machine*:8888
```

And start managing from the RSMF homepage. 