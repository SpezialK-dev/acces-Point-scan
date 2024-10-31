# What is this about

This repo is here to collect a few scripts and evaluation scripts that will scan your local network for coverage aswell as configuration.

The used network stack will be 
- Systemd-networkd
- iwd
- Systemd-Resolved

this will be enought Networkmanger should also be installed but does not need to be run as a service

## Why this came about

There is no good way to test wifi in your network and I hope this creates a decent way of testing wifi networks with only a laptop.


# Setup

you need to run the deamon in developer mode this is done by stoping the service and then run the following command and let it run.

```shell
sudo /usr/lib/iwd/iwd -E
```

also you need to have normally connected to the network before so that its a knowen network.
