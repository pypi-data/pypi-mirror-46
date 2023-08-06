"""
Vrrp main dataclass object.

Contains all attributes and hints about the datatype (some attributes have the
attribute forced when is assigned).
"""
from netaddr import EUI, IPAddress
from dataclasses import dataclass, field
from typing import Optional, Any, List, Dict
from netapi.metadata import Metadata, EntityCollections


def status_conversion(raw_status):
    """
    Based on a raw (known) status of the vrrp, it returns a standard status (UP,
    DOWN) string and its boolean representation.
    """
    if raw_status == "master":
        status = "master"
        status_up = True
    elif raw_status == "backup":
        status = "backup"
        status_up = True
    elif raw_status == "stopped":
        status = "stopped"
        status_up = False
    else:
        # For unknown cases
        status = raw_status
        status_up = False

    return status, status_up


@dataclass(unsafe_hash=True)
class VrrpBase:
    group_id: int
    # TODO: Create builder methods for populating interfaces with the VRRP information
    interface: str
    description: Optional[str] = None
    version: Optional[int] = None
    status: Optional[str] = None
    status_up: Optional[bool] = None
    instance: Optional[str] = None
    priority: Optional[int] = None
    master_priority: Optional[int] = None
    master_interval: Optional[float] = None  # seconds
    master_down_interval: Optional[float] = None  # seconds
    mac_advertisement_interval: Optional[float] = None  # seconds
    preempt: Optional[bool] = None
    preempt_delay: Optional[float] = None  # seconds
    preempt_reload: Optional[float] = None  # seconds
    skew_time: Optional[float] = None  # seconds
    virtual_ip: Optional[Any] = None
    _virtual_ip: Optional[Any] = field(init=False, repr=False)
    virtual_mac: Optional[Any] = None
    _virtual_mac: Optional[Any] = field(init=False, repr=False)
    master_ip: Optional[Any] = None
    _master_ip: Optional[Any] = field(init=False, repr=False)
    bfd_peer_ip: Optional[Any] = None
    _bfd_peer_ip: Optional[Any] = field(init=False, repr=False)
    tracked_objects: Optional[List[Dict]] = None
    virtual_ip_secondary: Optional[List] = field(default_factory=lambda: [])
    vr_id_disabled: Optional[bool] = None
    vr_id_disabled_reason: Optional[str] = None
    advertisement_interval: Optional[float] = None  # seconds
    connector: Optional[Any] = field(default=None, repr=False)

    def __post_init__(self, **_ignore):
        self.metadata = Metadata(name="vrrp", type="entity")
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
    def virtual_ip(self) -> IPAddress:
        return self._virtual_ip

    @virtual_ip.setter
    def virtual_ip(self, value: Any) -> None:
        # Workaround for when the value is not set
        if str(type(value)) in "<class 'property'>":
            self._virtual_ip = None
        else:
            self._virtual_ip = IPAddress(value)

    @property
    def virtual_mac(self) -> EUI:
        return self._virtual_mac

    @virtual_mac.setter
    def virtual_mac(self, value: Any) -> None:
        # Workaround for when the value is not set
        if str(type(value)) in "<class 'property'>":
            self._virtual_mac = None
        else:
            self._virtual_mac = EUI(value)

    @property
    def master_ip(self) -> IPAddress:
        return self._master_ip

    @master_ip.setter
    def master_ip(self, value: Any) -> None:
        # Workaround for when the value is not set
        if str(type(value)) in "<class 'property'>":
            self._master_ip = None
        else:
            self._master_ip = IPAddress(value)

    @property
    def bfd_peer_ip(self) -> IPAddress:
        return self._bfd_peer_ip

    @bfd_peer_ip.setter
    def bfd_peer_ip(self, value: Any) -> None:
        # Workaround for when the value is not set
        if str(type(value)) in "<class 'property'>":
            self._bfd_peer_ip = None
        else:
            self._bfd_peer_ip = IPAddress(value)


class VrrpsBase(EntityCollections):
    ENTITY = "vrrp"

    def __init__(self, *args, **kwargs):
        super().__init__(entity=self.ENTITY, *args, **kwargs)
        self.metadata = Metadata(name="vrrps", type="collection")

    def __setitem__(self, *args, **kwargs):
        super().__setitem__(*args, entity=self.ENTITY, **kwargs)
