# RSMF (Radio Slice Management Function)
The Radio Slice Management Function (RSMF) is the new component developed in Marathon to carry out the lifecycle management of the Radio Slices (RSs).

Note that to use the RSMF you must have all the hydra components of the Marathon experiment running (details in [https://github.com/maiconkist/gr-hydra/tree/marathon](https://github.com/maiconkist/gr-hydra/tree/marathon)). That is the hydra_server, the VBS, three VUEs. The Marathon architecture is:

![Marathon architecture](img/Marathon-components.png) 

The final version is the *multi slice* one, and it includes the RSMF code, the VNFDs, the NS, and the Ansible files.

The first operational version, *one slice*, is also included in a different module.