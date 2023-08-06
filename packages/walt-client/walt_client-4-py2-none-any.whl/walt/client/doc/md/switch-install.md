
# How to add or configure a switch into the WALT platform

## Introduction

This documentation page assumes you are familiar with WalT network architecture (see [`walt help show networking`](networking.md)).
If you just want to configure an existing switch connected on `walt-adm` network, you can skip the two next sections.


## Buying a new switch

We recommend the switch Netgear GS110TP. It is a cost-effective and robust switch.

It provides all features WALT expects:
* remote management through SNMP
* LLDP (Link Layer Discovery Protocol) and the ability to read the table using SNMP
* PoE (Power over Ethernet) on 8 ports and the ability to control them using SNMP

It also handles VLANs if you need them (e.g. scenario 3b described in [`walt help show server-network-config`](server-network-config.md)).


## Connecting the switch

You should connect the switch to WALT platform network (`walt-net`).


## Identifying the new switch

WALT server will detect this new device. If it recognizes the mac address range of this new device, it may deduce
it is switch, and call it `switch-<6-hex-chars>` (for instance switch-8a7bef). Otherwise, it will be named
`unknown-<6-hex-chars>`. The hex chars are taken from the right side of the switch mac address.

If LLDP (link layer discovery protocol) is available, just wait a little (10 minutes) for the LLDP tables to
be updated.

Then run:
```
$ walt device rescan
$ walt device tree
```

The tree view should display your new switch.

If LLDP is not available, use `walt device show` and look for devices named 'switch-<6-hex-chars>' or
'unknown-<6-hex-chars>'.

In any case, as soon as the switch is identified, it is strongly advised to rename it. A naming scheme
such as `switch-<location>-<id>` is handy. For instance, considering the new switch is in room 412:
```
$ walt device rename unknown-8a7bef switch-412-C
```

Troubleshooting notes:
* In case of trouble, you can monitor walt service logs on the server, while rebooting the switch,
  by typing `journalctl -f -u walt-server`. Or use a network sniffer (such as wireshark).


## Configuring the switch

By default, WALT is not allowed to send SNMP queries to a given switch, thus LLDP network discovery
and PoE hard-reboots will not be available.

You should explicitely enable them by running the following command and answering questions:
```
$ walt device admin <switch>
```

If the device was not detected as a switch, the command will first ask if this device is a switch.
Then, it will prompt for the SNMP configuration parameters WALT should use to interact with this switch.
For instance, the default parameters for read & write access to a switch Netgear GS110TP are snmp
version 2 and community `private`.
Then, next questions will allow you to enable PoE and LLDP queries, if your switch supports them.

If you allowed LLDP, you can now rescan the network:
```
$ walt device rescan
$ walt device tree
```

The tree view should now display equipments (nodes or other switches) connected to your switch.

