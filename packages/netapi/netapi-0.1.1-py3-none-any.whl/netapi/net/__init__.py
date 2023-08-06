"""
Interfaces module.

It contains the initializer where the Command and Parser implementations need
to register.

Also contains the `entity.py` which houses the
Interface dataclass with all of its attributes and sub-dataclasses
"""
from netapi.net.eos import pyeapier


class ObjectFactory:
    "General Factory Method"

    def __init__(self):
        self._builders = {}
        self._parsers = {}

    def register_builder(self, key, builder):
        self._builders[key] = builder

    def register_parser(self, key, parser):
        self._parsers[key] = parser

    # def create(self, key, **kwargs):
    #     builder = self._builders.get(key)
    #     if not builder:
    #         raise NotImplementedError(key)
    #     return builder(**kwargs)

    def create(self, key, sub_key, **kwargs):
        builder_dict = self._builders.get(key)
        if not builder_dict:
            raise NotImplementedError(key)
        builder = builder_dict.get(sub_key)
        if not builder:
            raise NotImplementedError(f"{sub_key} not implemented for {key}")
        return builder(**kwargs)

    def parse(self, key, **kwargs):
        parser = self._parsers.get(key)
        if not parser:
            raise NotImplementedError(key)
        return parser(**kwargs)


class HideIntfPrivateAttrs(dict):
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
            # Manipulation of values if they are objects to standard builtins
            if any(x in str(type(value)) for x in HideIntfPrivateAttrs.KNOWN_CLASSES):
                _iterable.append((key, str(value)))
            else:
                _iterable.append((key, value))
        return super().__init__(_iterable)


class ObjectBuilder:
    """
    Helper class used to create network objects by passing a device `connector` and the
    remaining parameters.

    It is a general builder method that calls the respective command and parser
    factories to get the registered implementations
    """

    def get_objects(self, factory, connector, parameters, **objs_params):
        # Get Object class and instantiate it
        obj_key = f"{connector.metadata.implementation}"
        obj_collector = factory.get_builder(obj_key, sub_key="collection")

        # Execute obj command
        raw_data = connector.run(obj_collector.command(**objs_params), **parameters)

        # Parse data and update object
        obj_parser = factory.get_parser(obj_key)

        return obj_parser.collector_parse(raw_data, obj_collector, **parameters)

    def get_object(self, factory, connector, parameters, **obj_params):
        # Get Object class to instantiate it
        obj_key = f"{connector.metadata.implementation}"

        # Pass obj_params because the object might have some required arguments
        obj = factory.get_builder(
            obj_key, sub_key="entity", connector=connector, **obj_params
        )

        # Execute obj command
        raw_data = connector.run(obj.command(**obj_params), **parameters)

        # Parse data and update object
        obj_parser = factory.get_parser(obj_key)
        obj_parser.parse(raw_data, obj, **parameters)
        return obj


class InterfacesBuilder(ObjectBuilder):
    """
    Helper class used to create interfaces object by passing a device `connector` object
    and interface/interface_range value.

    It is a general builder method that calls the respective command and parser
    factories to get the registered implementations
    """

    def get_interfaces(self, connector, parameters={}, **interface_params):
        parameters.update(silent=True)
        return self.get_objects(
            interface_factory, connector, parameters, **interface_params
        )

    def get_interface(self, connector, parameters={}, **interface_params):
        parameters.update(silent=True)
        return self.get_object(
            interface_factory, connector, parameters, **interface_params
        )


class InterfaceFactory(ObjectFactory):
    "Registers new implementation for commands to generate interface data"

    def get_builder(self, builder, **kwargs):
        return self.create(builder, **kwargs)

    def get_parser(self, builder, **kwargs):
        return self.parse(builder, **kwargs)


class VlansBuilder(ObjectBuilder):
    """
    Helper class used to create vlans object by passing a device `connector` object
    and vlan/vlan_range value.

    It is a general builder method that calls the respective command and parser
    factories to get the registered implementations
    """

    def get_vlans(self, connector, parameters={}, **vlan_params):
        return self.get_objects(vlan_factory, connector, parameters, **vlan_params)

    def get_vlan(self, connector, parameters={}, **vlan_params):
        return self.get_object(vlan_factory, connector, parameters, **vlan_params)


class VlanFactory(ObjectFactory):
    "Registers new implementation for commands to generate vlan data"

    def get_builder(self, builder, **kwargs):
        return self.create(builder, **kwargs)

    def get_parser(self, builder, **kwargs):
        return self.parse(builder, **kwargs)


class VrrpsBuilder(ObjectBuilder):
    """
    Helper class used to create vrrps object by passing a device `connector` object
    and vrrp/vrrp_range value.

    It is a general builder method that calls the respective command and parser
    factories to get the registered implementations
    """

    def get_vrrps(self, connector, parameters={}, **vrrp_params):
        return self.get_objects(vrrp_factory, connector, parameters, **vrrp_params)

    def get_vrrp(self, connector, parameters={}, **vrrp_params):
        return self.get_object(vrrp_factory, connector, parameters, **vrrp_params)


class VrrpFactory(ObjectFactory):
    "Registers new implementation for commands to generate vrrp data"

    def get_builder(self, builder, **kwargs):
        return self.create(builder, **kwargs)

    def get_parser(self, builder, **kwargs):
        return self.parse(builder, **kwargs)


interface_factory = InterfaceFactory()
# factory.register_builder("EOS-SNMP", InterfaceBuilderSnmp)
# factory.register_builder("EOS-RAW", InterfaceBuilderEosRaw)

interface_factory.register_builder(
    "EOS-PYEAPI", {"entity": pyeapier.Interface, "collection": pyeapier.Interfaces}
)
interface_factory.register_parser("EOS-PYEAPI", pyeapier.InterfaceParser)


vlan_factory = VlanFactory()
# factory.register_builder("EOS-SNMP", VlanBuilderSnmp)
# factory.register_builder("EOS-RAW", VlanBuilderEosRaw)

vlan_factory.register_builder(
    "EOS-PYEAPI", {"entity": pyeapier.Vlan, "collection": pyeapier.Vlans}
)
vlan_factory.register_parser("EOS-PYEAPI", pyeapier.VlanParser)


vrrp_factory = VrrpFactory()
# factory.register_builder("EOS-SNMP", VrrpBuilderSnmp)
# factory.register_builder("EOS-RAW", VrrpBuilderEosRaw)

vrrp_factory.register_builder(
    "EOS-PYEAPI", {"entity": pyeapier.Vrrp, "collection": pyeapier.Vrrps}
)
vrrp_factory.register_parser("EOS-PYEAPI", pyeapier.VrrpParser)
