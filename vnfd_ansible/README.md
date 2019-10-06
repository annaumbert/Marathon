
## build

The build script creates all the following VNFD and NS files:

1. marathon_hydra_server_vnfd.tar.gz
2. marathon_vbs_vnfd.tar.gz
3. marathon_vue1_vnfd.tar.gz
4. marathon_vue2_vnfd.tar.gz
5. marathon_vue3_vnfd.tar.gz
6. marathon_ns.tar.gz

File 6 (marathon_ns.tar.gz) is the basic experiment consisting of a 1 Base Station, 1 Hydra Server and 3 User Equipments.

To execute the build script just type:

```
./build
```

## osm

The osm script is a simple utilitaria to easen the task of installing, uninstalling, creating, and deleting VNDFs and NSDs.
Type the following command to get a detailed usage of it:
```
./osm l
```


### Testing

- From "marathon_vbs" ping  the tap interfaces of "marathon_vue1" with IPs 1.1.1.2, and "marathon_vue2" with IPs 2.2.2.2, and "marathon_vue3" with IPs 2.2.2.3.
```
ping 1.1.1.2
```
or
```
ping 2.2.2.2
```
or
```
ping 2.2.2.3
```

- From "marathon_vue1" ping the tap0 interface of "vbs", IP 1.1.1.1
```
ping 1.1.1.1
```


- From "marathon_vue2" or "marathon_vue3" ping the tap1 interface of "vbs", IP 2.2.2.1
```
ping 2.2.2.1
```

## Troubleshooting

Access each VM and kill the python process.


* In machine "marathon_hydra-server" execute (replace 192.168.5.54 by the ip of iris2):
```
python ~/gr-hydra/grc_blocks/app/ansible_hydra_gr_server.py --ansibleIPPort 192.168.5.54:5000
```

* In machine "marathon_vbs" execute (replace 192.168.5.82 by the IP of iris2):
```
python ~/gr-hydra/grc_blocks/app/ansible_hydra_gr_client_2tx_2rx.py --ansibleIP 192.168.5.82
```

* In machine "marathon_vue1" execute:
```
python ~/gr-hydra/grc_blocks/app/ansible_hydra_vr1_rx.py
```

* In machine "marathon_vue2" and "marathon_vue3"  execute:
```
python ~/gr-hydra/grc_blocks/app/ansible_hydra_vr2_rx.py
```
