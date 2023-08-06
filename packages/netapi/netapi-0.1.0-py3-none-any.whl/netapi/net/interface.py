"""
Interface main dataclass object.

Contains all attributes and hints about the datatype (some attributes have the
attribute forced when is assigned).
"""
import re
from dataclasses import dataclass, field
from typing import Optional, Any, List, Dict
from netaddr import IPNetwork, EUI
from netapi.metadata import Metadata, EntityCollections


def interface_converter(raw_interface):
    """
    Method that reads interface data and returns it on extended name format
    Example:
    raw_interface = Eth0/0
    new_interface = Ethernet0/0
    """
    pattern = re.compile(r"^(?P<value>\D+)(?P<remainder>\S+)")
    name_map = {
        "Eth": "Ethernet",
        "ethernet": "Ethernet",
        "Fa": "FastEthernet",
        "fastethernet": "FastEthernet",
        "Gi": "GigabitEthernet",
        "Ge": "GigabitEthernet",
        "gigabitethernet": "GigabitEthernet",
        "Te": "TenGigabitEthernet",
        "tengigabitethernet": "TenGigabitEthernet",
        "Po": "Port-channel",
        "port-channel": "Port-channel",
        "Vl": "Vlan",
        "vlan": "Vlan",
        "Lo": "Loopback",
        "lo": "Loopback",
        "loopback": "Loopback",
        "Tu": "Tunnel",
        "tunnel": "Tunnel",
    }

    match = re.search(pattern, raw_interface)
    try:
        value = match.group("value")
        remainder = match.group("remainder")

        if value in name_map.keys():
            new_interface = name_map[value] + remainder

        else:
            new_interface = raw_interface
    except AttributeError:
        # Leaving interface as is if no match
        new_interface = raw_interface

    return new_interface


def sort_interface(intf):
    """
    Based on the inteface name it collects the interface name ID and the numbers of the
    slots/port number (up to 3 digits value) and returns them.

    It is useful for when is called on the sorted method. Like:
    sorted(list_intf, key=sort_interface)
    """
    pattern = re.compile(
        r"(?P<id>[a-zA-Z]+(-[a-zA-Z]+)?)-?(?P<slot1>\d+)?(/|-)?(?P<slot2>\d+)?(/|-)?"
        r"(?P<slot3>\d+)?"
    )

    result = pattern.search(intf).groupdict()

    number = ""
    if result["slot1"]:
        number += result["slot1"]
    if result["slot2"]:
        number += result["slot2"]
    if result["slot3"]:
        number += result["slot3"]
    if not number:
        # Set a placeholder when only names have been passed (for those unique intf)
        number = "0"

    return result["id"], int(number)


def status_conversion(raw_status):
    """
    Based on a raw (known) status of the interface, it returns a standard status (UP,
    DOWN) string and its boolean representation.
    """
    if raw_status == "connected":
        status = "UP"
        enabled = True
        status_up = True
    elif raw_status == "notconnect":
        status = "DOWN"
        enabled = True
        status_up = False
    elif raw_status == "disabled":
        status = "DOWN"
        enabled = False
        status_up = False
    # elif raw_status == 2:
    #     status = 'DOWN'
    #     status_up = False
    #     status_code = 2
    # elif raw_status == 3:
    #     status = 'TESTING'
    #     status_up = True
    #     status_code = 1
    # elif raw_status == 4:
    #     status = 'UNKNOWN'
    #     status_up = False
    #     status_code = 10
    # elif raw_status == 5:
    #     status = 'DORMANT'
    #     status_up = False
    #     status_code = 1
    # elif raw_status == 6:
    #     status = 'ABSENT'
    #     status_up = False
    #     status_code = 1
    # elif raw_status == 7:
    #     status = 'LOWERLAYERDOWN'
    #     status_up = False
    #     status_code = 2
    else:
        # For unknown cases
        status = raw_status
        enabled = None
        status_up = False

    return status, status_up, enabled


def light_levels_alert(tx_power, rx_power, net_os=None):
    """
    Returns flag and alert based on light level values and predefined thresholds
    """
    # Power alert thresholds (from Cisco)
    tx_low_warning = -7.61
    tx_high_warning = -1.00
    tx_low_alarm = -11.61
    tx_high_alarm = 1.99
    rx_low_warning = -9.50
    rx_high_warning = 2.39
    rx_low_alarm = -13.56
    rx_high_alarm = 3.39
    if net_os == "junos":
        rx_low_warning = -23.01
        rx_high_warning = -1.00
        rx_low_alarm = -23.98
        rx_high_alarm = 0.00

    if rx_power >= rx_high_alarm or rx_power <= rx_low_alarm:
        flag = "red"

    elif tx_power >= tx_high_alarm or tx_power <= tx_low_alarm:
        flag = "red"

    elif rx_power >= rx_high_warning or rx_power <= rx_low_warning:
        flag = "yellow"

    elif tx_power >= tx_high_warning or tx_power <= tx_low_warning:
        flag = "yellow"

    else:
        flag = "green"

    return flag


@dataclass
class InterfaceCounters:
    """
    Houses interface counters. All attributes are optional, but their default value is
    a float -> 0.0

    The exception are the `rate` attributes, since they can be either captured but
    most of the time they do not appear since they are a result of a calculation
    """

    rx_bits_rate: Optional[float] = None
    tx_bits_rate: Optional[float] = None
    rx_pkts_rate: Optional[float] = None
    tx_pkts_rate: Optional[float] = None
    rx_unicast_pkts: Optional[float] = 0.0
    tx_unicast_pkts: Optional[float] = 0.0
    rx_multicast_pkts: Optional[float] = 0.0
    tx_multicast_pkts: Optional[float] = 0.0
    rx_broadcast_pkts: Optional[float] = 0.0
    tx_broadcast_pkts: Optional[float] = 0.0
    rx_octets: Optional[float] = 0.0
    tx_octets: Optional[float] = 0.0
    rx_discards: Optional[float] = 0.0
    tx_discards: Optional[float] = 0.0
    rx_errors_general: Optional[float] = 0.0
    tx_errors_general: Optional[float] = 0.0
    rx_errors_fcs: Optional[float] = 0.0
    rx_errors_crc: Optional[float] = 0.0
    rx_errors_runt: Optional[float] = 0.0
    rx_errors_rx_pause: Optional[float] = 0.0
    rx_errors_giant: Optional[float] = 0.0
    rx_errors_symbol: Optional[float] = 0.0
    tx_errors_collisions: Optional[float] = 0.0
    tx_errors_late_collisions: Optional[float] = 0.0
    tx_errors_deferred_transmissions: Optional[float] = 0.0
    tx_errors_tx_pause: Optional[float] = 0.0


@dataclass
class InterfaceOptical:
    """
    Houses interface optical levels and status. It automatically sets the status based
    on the light_levels_alert if is not assigned
    """

    tx: Optional[float] = None
    rx: Optional[float] = None
    status: Optional[str] = None
    _status: Optional[str] = field(init=False, repr=False)

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str) -> None:
        # Workaround for when the value is not set
        if str(type(value)) in "<class 'property'>":
            self._status = None
        else:
            if self.tx and self.rx:
                self._status = light_levels_alert(self.tx, self.rx)
            else:
                self._status = value


@dataclass
class InterfaceIP:
    """
    Houses interface IP attributes.

    It has @property methods embedded for ipv4 and ipv6 attributes to return IPNetwork
    objects.
    """

    ipv4: Optional[Any] = None
    _ipv4: Optional[Any] = field(init=False, repr=False)
    ipv6: Optional[Any] = None
    _ipv6: Optional[Any] = field(init=False, repr=False)
    # TODO: Make a property that when it calls to append the secondary IP - transform to
    #  a valid IPNetwork object
    secondary_ipv4: Optional[List] = field(default_factory=lambda: [])
    dhcp: Optional[bool] = None

    @property
    def ipv4(self) -> IPNetwork:
        return self._ipv4

    @ipv4.setter
    def ipv4(self, value: Any) -> None:
        # Workaround for when the value is not set
        if str(type(value)) in "<class 'property'>":
            self._ipv4 = None
        else:
            self._ipv4 = IPNetwork(value)

    @property
    def ipv6(self) -> IPNetwork:
        return self._ipv6

    @ipv6.setter
    def ipv6(self, value: Any) -> None:
        # Workaround for when the value is not set
        if str(type(value)) in "<class 'property'>":
            self._ipv6 = None
        else:
            self._ipv6 = IPNetwork(value)


@dataclass
class InterfacePhysical:
    """
    Houses interface physical attributes.

    It has @property methods embedded for mac attribute to return EUI
    objects.
    """

    # TODO: Add more specialized attributes like interface type
    mtu: Optional[int] = None
    bandwidth: Optional[int] = None
    duplex: Optional[str] = None
    mac: Optional[Any] = None
    _mac: Optional[Any] = field(init=False, repr=False)

    @property
    def mac(self):
        return self._mac

    @mac.setter
    def mac(self, value: Any) -> None:
        # Workaround for when the value is not set
        if str(type(value)) in "<class 'property'>":
            self._mac = None
        else:
            self._mac = EUI(value)


@dataclass(unsafe_hash=True)
class InterfaceBase:
    """
    Main Interface object. Houses general information of the interface and other
    subclasses.

    It has embedded @property for attributes like address, counters, physical and
    optical.

    It also has the status and datetime objects regarding collection-data, last status
    change, last clear of counters, among others
    """

    name: str
    _name: str = field(init=False, repr=False)
    description: Optional[str] = None
    enabled: Optional[bool] = None
    status_up: Optional[bool] = None
    status: Optional[str] = None
    last_status_change: Optional[Any] = None
    number_status_changes: Optional[float] = None
    forwarding_model: Optional[str] = None
    physical: Optional[Any] = None
    _physical: Optional[Any] = field(init=False, repr=False)
    optical: Optional[Any] = None
    _optical: Optional[Any] = field(init=False, repr=False)
    addresses: Optional[Any] = None
    _addresses: Optional[Any] = field(init=False, repr=False)
    instance: Optional[str] = None
    counters: Optional[Dict] = field(repr=False, default=None)
    members: Optional[set] = None
    last_clear: Optional[Any] = None
    counter_refresh: Optional[Any] = None
    update_interval: Optional[float] = None
    connector: Optional[Any] = field(default=None, repr=False)

    def __post_init__(self, **_ignore):
        self.metadata = Metadata(name="interface", type="entity")
        if self.connector:
            if not hasattr(self.connector, "metadata"):
                raise ValueError(
                    f"It does not contain metadata attribute: {self.connector}"
                )
            if self.connector.metadata.name != "device":
                raise ValueError(
                    f"It is not a valid connector object: {self.connector}"
                )

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = interface_converter(value)

    @property
    def addresses(self) -> InterfaceIP:
        return self._addresses

    @addresses.setter
    def addresses(self, value: Any) -> None:
        # Workaround for when the value is not set
        if str(type(value)) in "<class 'property'>":
            self._addresses = InterfaceIP()
        elif isinstance(value, dict):
            self._addresses = InterfaceIP(**value)
        else:
            self._addresses = value

    @property
    def optical(self) -> InterfaceOptical:
        return self._optical

    @optical.setter
    def optical(self, value: Any) -> None:
        # Workaround for when the value is not set
        if str(type(value)) in "<class 'property'>":
            self._optical = InterfaceOptical()
        elif isinstance(value, dict):
            self._optical = InterfaceOptical(**value)
        else:
            self._optical = value

    @property
    def physical(self) -> InterfacePhysical:
        return self._physical

    @physical.setter
    def physical(self, value: Any) -> None:
        # Workaround for when the value is not set
        if str(type(value)) in "<class 'property'>":
            self._physical = InterfacePhysical()
            # self._physical = None
        elif isinstance(value, dict):
            self._physical = InterfacePhysical(**value)
        else:
            self._physical = value

    @property
    def counters(self) -> InterfaceCounters:
        return self._counters

    @counters.setter
    def counters(self, value: Any) -> None:
        # Workaround for when the value is not set
        if str(type(value)) in "<class 'property'>":
            self._counters = InterfaceCounters()
            # self._counters = None
        elif isinstance(value, dict):
            self._counters = InterfaceCounters(**value)
        else:
            self._counters = value


class InterfacesBase(EntityCollections):
    ENTITY = "interface"

    def __init__(self, *args, **kwargs):
        super().__init__(entity=self.ENTITY, *args, **kwargs)
        self.metadata = Metadata(name="interfaces", type="collection")

    def __setitem__(self, *args, **kwargs):
        super().__setitem__(*args, entity=self.ENTITY, **kwargs)
