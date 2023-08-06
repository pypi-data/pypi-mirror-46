import uuid
import reprlib
import datetime
from collections import ChainMap
from dataclasses import dataclass, field
from typing import Optional, Any


@dataclass
class Metadata:
    name: str
    type: str
    implementation: str = None
    created_at: Any = field(init=False)
    id: Any = field(init=False)
    updated_at: Optional[Any] = None
    collection_count: int = 0
    parent: Optional[str] = None

    def __post_init__(self, **_igonre):
        self.created_at = datetime.datetime.now()
        self.id = uuid.uuid4()


class EntityCollections(ChainMap):
    """
    Main entity collection object. Used for fast lookup and higher level wrapper.
    Should not be instantiated directly

    This allows Objects to be created and accessed like:
    >>> repr(vl177)
    Vlan(id=177, name='NATIVE', ... metadata=Metadata(name='vlan', ... parent=None))

    >>> vlan_collection = Vlans({177: vl177})
    >>> repr(vlan_collection)
    Vlans(177)

    >>> vlan_collection.update({178: vl178})
    >>> repr(vlan_collection)
    Vlans(177, 178)

    >>> vlan_collection[177]
    Vlan(id=177, name='NATIVE', ... metadata=Metadata(name='vlan', ... parent=None))

    >>> len(vlan_collection)
    2
    """

    def __init__(self, *args, entity=None, **kwargs):
        "Initializing ChainMap object and verifying values"
        for arg in args:
            for value in arg.values():
                self._attr_verify(value, entity)
        super().__init__(*args, **kwargs)

    def _attr_verify(self, attribute, expected_type):
        "Verify that each value inserted are of the expected type"
        try:
            if attribute.metadata.name != expected_type:
                raise ValueError(
                    f"{attribute} -> It is not a valid {expected_type} object"
                )
        except AttributeError:
            raise ValueError(f"{attribute} -> It is not a valid {expected_type} object")

    def __setitem__(self, *args, entity=None, **kwargs):
        "Verifying values when updating"
        value = args[-1]
        self._attr_verify(value, entity)
        super().__setitem__(*args, **kwargs)

        # Update the metadata timestamp if possible
        if hasattr(self, "metadata"):
            self.metadata.updated_at = datetime.datetime.now()

    @reprlib.recursive_repr()
    def __repr__(self):
        "Show repr as calling class with the ID of each entity"
        return f"{self.__class__.__name__}(" + ", ".join(map(repr, self)) + ")"


class HidePrivateAttrs(dict):
    """
    Used as dict_factory for hiding private attributes and also returning string
    values of embeded objects
    """

    KNOWN_CLASSES = [
        "netaddr.ip.IPNetwork",
        "netaddr.ip.IPAddress",
        "netaddr.eui.EUI",
        "datetime.datetime",
    ]

    def __init__(self, iterable):
        _iterable = []
        for key, value in iterable:
            # Hides the private attributes when creating dict
            if key.startswith("_"):
                continue
            if key == "connector":
                continue
            # Manipulation of values if they are objects to standard builtins
            if any(x in str(type(value)) for x in HidePrivateAttrs.KNOWN_CLASSES):
                _iterable.append((key, str(value)))
            else:
                _iterable.append((key, value))
        return super().__init__(_iterable)
