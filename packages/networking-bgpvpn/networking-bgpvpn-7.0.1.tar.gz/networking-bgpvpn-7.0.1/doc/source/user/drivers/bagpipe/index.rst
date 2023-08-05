..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==================
OVS/BaGPipe driver
==================

Introduction
------------

The **BaGPipe** driver for the BGPVPN service plugin is designed to work jointly with the openvswitch
ML2 mechanism driver.

It relies on the use of the bagpipe-bgp BGP VPN implementation on compute nodes
and the MPLS implementation in OpenVSwitch.

Architecture overview
---------------------

The bagpipe driver for the BGPVPN service plugin interacts with the openvswitch agent on each
compute node, which is extended to support new RPCs to trigger the local configuration on compute
nodes of BGP VPN instances and of their MPLS dataplane.

.. blockdiag:: overview.blockdiag

Limitations
-----------

On DHCP ports, Router interface ports, external network ports, etc.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

No connectivity will be setup with BGP VPNs for DHCP ports or Router
interface ports, or other network specific ports. This improves the load on network nodes by
avoiding them to import/export a significant amount of routes, without limiting BGP VPN
deployment scenarios because no useful traffic would be exchanged between a router or DHCP
interface of a network associated to a BGP VPN.

Similarly, the driver will not bind a port on an external network. This behavior will be
revisited once a use case is well identified.

How to use ?
------------

On an Openstack Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

[TBC (package installation + config)]

In devstack
~~~~~~~~~~~

* follow the instruction in README.rst

* ``local.conf``:

  * add the following to enable the BaGPipe driver for the BGPVPN service plugin:

    .. code-block:: ini

       NETWORKING_BGPVPN_DRIVER="BGPVPN:BaGPipe:networking_bgpvpn.neutron.services.service_drivers.bagpipe.bagpipe.BaGPipeBGPVPNDriver:default"

  * enable networking-bagpipe_, which contains code for agent extensions:

    .. code-block:: ini

       enable_plugin networking-bagpipe https://git.openstack.org/openstack/networking-bagpipe.git
       # enable_plugin networking-bagpipe https://git.openstack.org/openstack/networking-bagpipe.git stable/ocata

* on a control node, if you want to run the Fake Route-Reflector there (relevant only for a multinode setup):

  .. code-block:: none

     enable_service b-fakerr

* on compute nodes:

  * the compute node Neutron agent is the Neutron openvswitch agent, with the ``bagpipe_bgpvpn`` agent extension:

    * install networking-bagpipe_  (the code to interact with ``bagpipe-bgp`` comes from there):

      .. code-block:: ini

         enable_plugin networking-bagpipe https://git.openstack.org/openstack/networking-bagpipe.git
         # enable_plugin networking-bagpipe https://git.openstack.org/openstack/networking-bagpipe.git stable/ocata

    * define ``Q_AGENT=openvswitch`` in ``local.conf``  (optional, this is actually the default now)

    * the ``bagpipe_bgpvpn`` agent extension is automatically added to the agent configuration by the devstack plugin

  * bagpipe-bgp will be installed automatically (part of networking-bagpipe since Pike, or as a submodule before)

  * you need to enable and configure bagpipe-bgp, typically with a peering to a BGP Route-Reflector or BGP router(s):

    .. code-block:: ini

       enable_service b-bgp

       BAGPIPE_DATAPLANE_DRIVER_IPVPN=mpls_ovs_dataplane.MPLSOVSDataplaneDriver
       # BAGPIPE_DATAPLANE_DRIVER_IPVPN=ovs # simpler config available > after Ocata

       # IP of your route-reflector or BGP router, or fakeRR
       # BAGPIPE_BGP_PEERS defaults to $SERVICE_HOST, which will point to the controller in a
       # multi-node devstack setup
       #BAGPIPE_BGP_PEERS=1.2.3.4,2.3.4.5

.. _networking-bagpipe: https://docs.openstack.org/networking-bagpipe/latest/

