"""
EOS Pyeapi module.

Contains the method to create Network Objects for the EOS-PYEAPI implementation.
"""
import datetime
from netapi.net import vlan, vrrp, interface


class Vlans(vlan.VlansBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.metadata.implementation = "EOS-PYEAPI"

    def command(self, vlan_range=None, **kwargs):
        "Returns commands necessary to build a collection of entities"
        if not vlan_range:
            raise ValueError("Must provide vlan_range or vlan.")
        if vlan_range == "all":
            return ["show vlan"]
        elif vlan_range:
            return [f"show vlan id {vlan_range}"]

    def update_all_command(self, **_ignore):
        "Gets all VLAN IDs in the instance to create the vlan range"
        _vlan_ids = list(self.keys())
        _vlan_range = f"{_vlan_ids[0]} - {_vlan_ids[-1]}"
        return [f"show vlan id {_vlan_range}"]

    def get_all(self, connector):
        "Automatic trigger a data collection. A connector object has to be passed"
        if connector.metadata.implementation != "EOS-PYEAPI":
            raise ValueError(
                "Connector is not of the correct implementation: EOS-PYEAPI"
            )
        VlanParser().collector_parse(connector.run(self.update_all_command()), self)
        self.metadata.updated_at = datetime.datetime.now()
        self.metadata.collection_count += 1
        return True


class Vlan(vlan.VlanBase):
    def __post_init__(self, **_ignore):
        super().__post_init__(**_ignore)
        self.metadata.implementation = "EOS-PYEAPI"
        self._vlan_api_generator()

    def _vlan_api_generator(self):
        if self.connector is not None:
            if self.connector.metadata.implementation != "EOS-PYEAPI":
                raise ValueError(
                    "Connector is not of the correct implementation: EOS-PYEAPI"
                )
            self.vlan_api = self.connector.connector.api("vlans")
            return True
        else:
            return False

    def command(self, **_ignore):
        "Returns commands necessary to build the entity"
        return [f"show vlan id {self.id}"]

    def get(self):
        "Automatic trigger a data collection"
        if self.connector is None:
            raise NotImplementedError("Need to have the connector defined")
        VlanParser().parse(self.connector.run(self.command()), self)
        self.metadata.updated_at = datetime.datetime.now()
        self.metadata.collection_count += 1
        return True

    def enable(self):
        "Enable VLAN"
        if not hasattr(self, "vlan_api"):
            if not self._vlan_api_generator():
                raise NotImplementedError("Need to have the connector API defined")
        return self.vlan_api.set_state(self.id, value="active")

    def disable(self):
        "Disable VLAN"
        if not hasattr(self, "vlan_api"):
            if not self._vlan_api_generator():
                raise NotImplementedError("Need to have the connector API defined")
        return self.vlan_api.set_state(self.id, value="suspend")


class VlanParser:
    "Vlan data parser for the returned PYEAPI - EOS implementation"

    def get_keys(self, raw_data_values):
        "Retrieves all the vlans names fro the outputs returned by the device"
        _vlans_names = []
        for _response in raw_data_values:
            if not _response:
                continue
            vlan_data = _response.get("vlans")
            if vlan_data:
                _vlans_names.extend(vlan_data.keys())
        return set(_vlans_names)

    def _data_available(self, vlan, command_data):
        "Just verifies that the command actually returned any data"
        if not command_data:
            return False
        if not command_data.get("vlans"):
            return False
        if not command_data.get("vlans").get(vlan):
            return False
        return True

    def data_parser(self, vl, data, **kwargs):
        "Updates the VLAN object by parsing the returned data"
        # Attributes
        if data.get("name"):
            vl.name = data.get("name")
        if data.get("dynamic"):
            vl.dynamic = data.get("dynamic")
        if data.get("interfaces"):
            vl.interfaces = list(data.get("interfaces").keys())

        # Status
        if data.get("status"):
            vl.status, vl.status_up = vlan.status_conversion(data.get("status"))

    def parse(self, raw_data, vl, **kwargs):
        "Parses the ID of the VLANs and the associated data to be parsed"
        # Retrieve messages info
        data = list(raw_data.values())[0].get("vlans").get(str(vl.id))
        if not data:
            raise ValueError(f"No data returned from device")

        # Return true parsed data
        self.data_parser(vl, data, **kwargs)
        return True

    def collector_parse(self, raw_data, vlans, **kwargs):
        """
        It takes the ouput from device and parses it into separate Vlan instances
        to be updated into the main Vlans object
        """
        _vlans_ids = self.get_keys(raw_data.values())
        for _vlan_id in _vlans_ids:
            _vlan = Vlan(id=int(_vlan_id))

            for command, value in raw_data.items():
                if not self._data_available(_vlan_id, value):
                    continue
                self.data_parser(vl=_vlan, data=value.get("vlans").get(_vlan_id))

            # Update Vlans
            vlans.update({_vlan.id: _vlan})

        return vlans


class Vrrps(vrrp.VrrpsBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.metadata.implementation = "EOS-PYEAPI"

    def command(self, instance=None, interface=None, **kwargs):
        "Returns commands necessary to build a collection of entities"
        if interface:
            return [f"show vrrp interface {interface} all"]
        elif instance:
            return [f"show vrrp vrf {instance} all"]
        else:
            return [f"show vrrp all"]

    def update_all_command(self, **_ignore):
        """
        Gets all VRRP Group IDs and Interface and Instance in the object
        to create the vrrp range
        """
        # _vrrps_ids = list(self.keys())
        # _vlan_range = f"{_vrrps_ids[0]} - {_vrrps_ids[-1]}"
        # return [f"show vlan id {_vlan_range}"]
        return ["show vrrp all"]

    def get_all(self, connector):
        "Automatic trigger a data collection. A connector object has to be passed"
        if connector.metadata.implementation != "EOS-PYEAPI":
            raise ValueError(
                "Connector is not of the correct implementation: EOS-PYEAPI"
            )
        # TODO: Need to fix since the commands gets all the vrrp groups
        VrrpParser().collector_parse(connector.run(self.update_all_command()), self)
        self.metadata.updated_at = datetime.datetime.now()
        self.metadata.collection_count += 1
        return True


class Vrrp(vrrp.VrrpBase):
    def __post_init__(self, **_ignore):
        super().__post_init__(**_ignore)
        self.metadata.implementation = "EOS-PYEAPI"
        self._vrrp_api_generator()

    def _vrrp_api_generator(self):
        if self.connector is not None:
            if self.connector.metadata.implementation != "EOS-PYEAPI":
                raise ValueError(
                    "Connector is not of the correct implementation: EOS-PYEAPI"
                )
            self.vrrp_api = self.connector.connector.api("vrrp")
            return True
        else:
            return False

    def command(self, **_ignore):
        "Returns commands necessary to build the entity"
        if self.interface:
            return [f"show vrrp group {self.group_id} interface {self.interface} all"]
        elif self.instance:
            return [f"show vrrp group {self.group_id} vrf {self.instance} all"]
        else:
            return [f"show vrrp group {self.group_id} vrf all"]

    def get(self, **_ignore):
        "Automatic trigger a data collection"
        if self.connector is None:
            raise NotImplementedError("Need to have the connector defined")
        VrrpParser().parse(self.connector.run(self.command()), self)
        self.metadata.updated_at = datetime.datetime.now()
        self.metadata.collection_count += 1
        return True

    def enable(self):
        "Enable VRRP group"
        if not hasattr(self, "vrrp_api"):
            if not self._vrrp_api_generator():
                raise NotImplementedError("Need to have the connector API defined")
        return self.vrrp_api.set_enable(self.interface, self.group_id, value=True)

    def disable(self):
        "Disable VRRP group"
        if not hasattr(self, "vrrp_api"):
            if not self._vrrp_api_generator():
                raise NotImplementedError("Need to have the connector API defined")
        return self.vrrp_api.set_enable(self.interface, self.group_id, value=False)


class VrrpParser:
    "Vrrp data parser for the returned PYEAPI - EOS implementation"

    def get_keys(self, raw_data_values):
        "Retrieves all the vrrps names fro the outputs returned by the device"
        _vrrps_names = []
        for _response in raw_data_values:
            if not _response:
                continue
            vrrp_data = _response.get("virtualRouters")
            if vrrp_data:
                # _vrrps_names.extend(vrrp_data.keys())
                _vrrps_names.extend([(x["groupId"], x["interface"]) for x in vrrp_data])
        return set(_vrrps_names)

    def _data_available(self, vrrp, command_data):
        "Just verifies that the command actually returned any data"
        if not command_data:
            return False
        if not command_data.get("virtualRouters"):
            return False
        return True

    def data_parser(self, vr, data, **kwargs):
        # Attributes
        if data.get("vrfName"):
            vr.instance = data.get("vrfName")
        if data.get("description"):
            vr.description = data.get("description")
        if data.get("virtualMac"):
            vr.virtual_mac = data.get("virtualMac")
        if data.get("virtualIpSecondary"):
            vr.virtual_ip_secondary = data.get("virtualIpSecondary")
        if data.get("masterAddr"):
            vr.master_ip = data.get("masterAddr")
        if data.get("virtualIp"):
            vr.virtual_ip = data.get("virtualIp")
        if data.get("priority"):
            vr.priority = data.get("priority")
        if data.get("skewTime"):
            vr.skew_time = float(data.get("skewTime"))
        if data.get("version"):
            vr.version = int(data.get("version"))

        # Preempt
        if data.get("preempt"):
            vr.preempt = data.get("preempt")
        if data.get("preemptDelay"):
            vr.preempt_delay = float(data.get("preemptDelay"))
        if data.get("preemptReload"):
            vr.preempt_reload = float(data.get("preemptReload"))

        # BFD Peer
        if data.get("bfdPeerAddr"):
            vr.bfd_peer_ip = data.get("bfdPeerAddr")

        # Timers
        if data.get("macAddressInterval"):
            vr.mac_advertisement_interval = float(data.get("macAddressInterval"))
        if data.get("masterInterval"):
            vr.master_interval = float(data.get("masterInterval"))
        if data.get("masterDownInterval"):
            vr.master_down_interval = float(data.get("masterDownInterval")) / 1000.0
        if data.get("vrrpAdvertInterval"):
            vr.advertisement_interval = float(data.get("vrrpAdvertInterval"))

        # Tracked Objects
        if data.get("trackedObjects"):
            vr.tracked_objects = data.get("trackedObjects")

        # Status
        if data.get("state"):
            vr.status, vr.status_up = vrrp.status_conversion(data.get("state"))

        # VR ID Disabled
        if data.get("vrIdDisabled") or data.get("vrIdDisabled") is False:
            vr.vr_id_disabled = data.get("vrIdDisabled")
        if data.get("vrIdDisabledReason"):
            vr.vr_id_disabled_reason = data.get("vrIdDisabledReason")

    def parse(self, raw_data, vr, **kwargs):
        "Parses the VRRP group returned and the associated data to be parsed"
        # Retrieve messages info
        print(raw_data)
        rdata = list(raw_data.values())[0].get("virtualRouters")
        if not rdata:
            raise ValueError(f"No data returned from device")
        else:
            # Because the data returned is in a list type format
            data = rdata[0]

        # Return true parsed data
        self.data_parser(vr, data, **kwargs)
        return True

    def collector_parse(self, raw_data, vrrps_obj, **kwargs):
        """
        It takes the ouput from device and parses it into separate VRRP instances
        to be updated into the main VRRP object
        """
        # Since the data returned is a global list of resources under the
        # virtualRouters field, I will parse on each element and create a Vrrp object
        # So there is no need for a get_keys method call
        data = list(raw_data.values())[0]
        for vrrp_data in data.get("virtualRouters"):
            # Placeholder
            _vrrp = Vrrp(
                group_id=int(vrrp_data.get("groupId")),
                interface=vrrp_data.get("interface"),
            )
            # Parsing
            self.data_parser(_vrrp, vrrp_data)
            vrrps_obj.update({(_vrrp.group_id, _vrrp.interface): _vrrp})

        return vrrps_obj


class Interfaces(interface.InterfacesBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.metadata.implementation = "EOS-PYEAPI"

    def command(self, interface_range=None, **kwargs):
        "Returns commands necessary to build the collection of entities"
        if interface_range:
            self.interface_range = interface_range
            return [
                f"show interfaces {interface_range}",
                f"show ip interface {interface_range}",
                f"show interfaces {interface_range} transceiver",
            ]
        else:
            self.interface_range = None
            return [
                "show interfaces",
                "show ip interface",
                "show interfaces transceiver",
            ]

    def get_all(self, connector):
        "Automatic trigger a data collection. A connector object has to be passed"
        if connector.metadata.implementation != "EOS-PYEAPI":
            raise ValueError(
                "Connector is not of the correct implementation: EOS-PYEAPI"
            )
        intf = self.interface_range if hasattr(self, "interface_range") else None
        InterfaceParser().collector_parse(
            connector.run(self.commands(interface_range=intf), silent=True), self
        )
        self.metadata.updated_at = datetime.datetime.now()
        self.metadata.collection_count += 1
        return True


class Interface(interface.InterfaceBase):
    def __post_init__(self, **_ignore):
        super().__post_init__(**_ignore)
        self.metadata.implementation = "EOS-PYEAPI"
        self._interface_api_generator()

    def _interface_api_generator(self):
        if self.connector is not None:
            if self.connector.metadata.implementation != "EOS-PYEAPI":
                raise ValueError(
                    "Connector is not of the correct implementation: EOS-PYEAPI"
                )
            self.interface_api = self.connector.connector.api("interfaces")
            return True
        else:
            return False

    def command(self, **_ignore):
        "Returns commands necessary to build the entity"
        return [
            f"show interfaces {self.name}",
            f"show ip interface {self.name}",
            f"show interfaces {self.name} transceiver",
        ]

    def get(self, **_ignore):
        "Automatic trigger a data collection"
        if self.connector is None:
            raise NotImplementedError("Need to have the connector defined")
        InterfaceParser().parse(
            self.connector.run(self.command(), silent=True), self
        )
        self.metadata.updated_at = datetime.datetime.now()
        self.metadata.collection_count += 1
        return True

    def enable(self):
        "Enable Interface"
        if not hasattr(self, "interface_api"):
            if not self._interface_api_generator():
                raise NotImplementedError("Need to have the connector API defined")
        return self.interface_api.set_shutdown(self.name, disable=True)

    def disable(self):
        "Disable Interface"
        if not hasattr(self, "interface_api"):
            if not self._interface_api_generator():
                raise NotImplementedError("Need to have the connector API defined")
        return self.interface_api.set_shutdown(self.name, disable=False)


class InterfaceParser:
    "Interface data parser for the returned PYEAPI - EOS implementation"

    def get_keys(self, raw_data_values):
        "Retrieves all the interfaces names fro the outputs returned by the device"
        _interfaces_names = []
        for _response in raw_data_values:
            if not _response:
                continue
            interface_data = _response.get("interfaces")
            if interface_data:
                _interfaces_names.extend(interface_data.keys())
        return set(_interfaces_names)

    def _data_available(self, interface, command_data):
        "Just verifies that the command actually returned any data"
        if not command_data:
            return False
        if not command_data.get("interfaces"):
            return False
        if not command_data.get("interfaces").get(interface):
            return False
        return True

    def data_parser(self, intf, data, **kwargs):
        # Forwarding model
        if data.get("forwardingModel"):
            intf.forwarding_model = data.get("forwardingModel")  # routerd or bridged

        # Physical attributes
        if data.get("description"):
            intf.description = data.get("description")
        if data.get("physicalAddress"):
            intf.physical.mac = data.get("physicalAddress")
        if data.get("mtu"):
            intf.physical.mtu = data.get("mtu")
        if data.get("duplex"):
            intf.physical.duplex = data.get("duplex")
        if data.get("bandwidth"):
            intf.physical.bandwidth = data.get("bandwidth")

        # Status
        if data.get("interfaceStatus"):
            intf.status, intf.status_up, intf.enabled = interface.status_conversion(
                data.get("interfaceStatus")
            )
        if data.get("lastStatusChangeTimestamp"):
            intf.last_status_change = datetime.datetime.fromtimestamp(
                data.get("lastStatusChangeTimestamp")
            )

        # IP Attributes
        intf_address = data.get("interfaceAddress")
        if intf_address and isinstance(intf_address, dict):
            if intf_address.get("dhcp"):
                intf.addresses.dchp = intf_address.get("dhcp")
            if intf_address.get("secondaryIpsOrderedList"):
                for ip in intf_address.get("secondaryIpsOrderedList"):
                    intf.addresses.secondary_ipv4.append(
                        f"{ip['address']}/{ip['maskLen']}"
                    )
            if intf_address.get("primaryIp"):
                # TODO: Retrieve IPv6 address as well - test on docker
                ip = intf_address.get("primaryIp")
                intf.addresses.ipv4 = f"{ip['address']}/{ip['maskLen']}"

        # VRF
        if data.get("vrf"):
            intf.instance = data.get("vrf")

        # Counters
        intf_counters = data.get("interfaceCounters")
        if intf_counters:
            if intf_counters.get("lastClear"):
                intf.last_clear = datetime.datetime.fromtimestamp(
                    intf_counters.get("lastClear")
                )
            if intf_counters.get("counterRefreshTime"):
                intf.counter_refresh = datetime.datetime.fromtimestamp(
                    intf_counters.get("counterRefreshTime")
                )
            if intf_counters.get("linkStatusChanges"):
                intf.number_status_changes = intf_counters.get("linkStatusChanges")
            intf.counters.tx_broadcast_pkts = float(
                intf_counters.get("outBroadcastPkts", 0)
            )
            intf.counters.tx_unicast_pkts = float(intf_counters.get("outUcastPkts", 0))
            intf.counters.rx_multicast_pkts = float(
                intf_counters.get("inMulticastPkts", 0)
            )
            intf.counters.rx_broadcast_pkts = float(
                intf_counters.get("inBroadcastPkts", 0)
            )
            intf.counters.rx_octets = float(intf_counters.get("inOctets", 0))
            intf.counters.tx_octets = float(intf_counters.get("outOctets", 0))
            intf.counters.rx_unicast_pkts = float(intf_counters.get("inUcastPkts", 0))
            intf.counters.tx_multicast_pkts = float(
                intf_counters.get("outMulticastPkts", 0)
            )
            # Tx Errors
            intf.counters.tx_errors_general = float(
                intf_counters.get("totalOutErrors", 0)
            )
            intf.counters.tx_discards = float(intf_counters.get("outDiscards", 0))
            if intf_counters.get("outputErrorsDetail"):
                tx_errors = intf_counters.get("outputErrorsDetail", {})
                intf.counters.tx_errors_collisions = float(
                    tx_errors.get("collisions", 0)
                )
                intf.counters.tx_errors_deferred_transmissions = float(
                    tx_errors.get("deferredTransmissions", 0)
                )
                intf.counters.tx_errors_tx_pause = float(tx_errors.get("txPause", 0))
                intf.counters.tx_errors_late_collisions = float(
                    tx_errors.get("lateCollisions")
                )
            # Rx Errors
            intf.counters.rx_errors_general = float(
                intf_counters.get("totalInErrors", 0)
            )
            intf.counters.rx_discards = float(intf_counters.get("inDiscards", 0))
            if intf_counters.get("inputErrorsDetail"):
                rx_errors = intf_counters.get("inputErrorsDetail", {})
                intf.counters.rx_errors_runt = float(rx_errors.get("runtFrames", 0))
                intf.counters.rx_errors_rx_pause = float(rx_errors.get("rxPause", 0))
                intf.counters.rx_errors_fcs = float(rx_errors.get("fcsErrors", 0))
                intf.counters.rx_errors_crc = float(rx_errors.get("alignmentErrors", 0))
                intf.counters.rx_errors_giant = float(rx_errors.get("giantFrames", 0))
                intf.counters.rx_errors_symbol = float(rx_errors.get("symbolErrors", 0))

        # Statistics
        intf_statistics = data.get("interfaceStatistics")
        if intf_statistics:
            intf.counters.rx_bits_rate = float(intf_statistics.get("inBitsRate", 0))
            intf.counters.rx_pkts_rate = float(intf_statistics.get("inPktsRate", 0))
            intf.counters.tx_bits_rate = float(intf_statistics.get("outBitsRate", 0))
            intf.counters.tx_pkts_rate = float(intf_statistics.get("outPktsRate", 0))
            if intf_statistics.get("updateInterval"):
                intf.update_interval = float(intf_statistics.get("updateInterval"))

        # Member Interfaces
        if data.get("memberInterfaces"):
            intf.members = set(data.get("memberInterfaces").keys())

    def parse(self, raw_data, intf, **kwargs):
        "Parses the Interface returned and the associated data to be parsed"
        for intf_data in raw_data.values():
            # Skip interfaces command results that did not return data
            if not intf_data:
                continue
            # Retrieve messages info
            try:
                data = intf_data["interfaces"][intf.name]
            except KeyError:
                continue

            # TODO: Create method to raise "No data returned from device"
            # Return true parsed data
            self.data_parser(intf, data, **kwargs)

        return True

    def collector_parse(self, raw_data, interfaces_obj, **kwargs):
        """
        Main method to create Interfaces objects.

        It first retrieves all the interfaces from the output gathered and creates
        Interface objects placeholder

        Then populates all the attributes by checking the returned output of the command

        Returns the gathered Interface objects
        """
        _interfaces_names = self.get_keys(raw_data.values())
        for _interface_name in _interfaces_names:
            _interface = Interface(
                name=_interface_name,
                physical=interface.InterfacePhysical(),
                addresses=interface.InterfaceIP(),
                optical=interface.InterfaceOptical(),
                counters=interface.InterfaceCounters(),
            )

            for command, value in raw_data.items():
                if not self._data_available(_interface_name, value):
                    continue
                self.data_parser(
                    intf=_interface, data=value.get("interfaces").get(_interface_name)
                )

            interfaces_obj.update({_interface.name: _interface})

        return interfaces_obj
