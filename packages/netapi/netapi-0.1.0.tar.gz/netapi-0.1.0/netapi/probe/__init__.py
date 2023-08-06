from netapi.probe.eos import pyeapier
from netapi.probe.ios import netmikoer as ios_netmikoer
from netapi.probe.junos import pyezer
from netapi.probe.linux import subprocesser, paramikoer
from netapi.probe.nxos import nxapier
from netapi.probe.xe import netmikoer as xe_netmikoer
from netapi.probe.xr import netmikoer as xr_netmikoer


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


class PingBuilder(ObjectBuilder):
    """
    Helper class used to create Ping object by passing a device `connector` object
    and other parameters value.

    It is a general builder method that calls the respective command and parser
    factories to get the registered implementations
    """

    def create_pings(self, connector, parameters={}, **vlan_params):
        return self.get_objects(ping_factory, connector, parameters, **vlan_params)

    def create_ping(self, connector, parameters={}, **vlan_params):
        return self.get_object(ping_factory, connector, parameters, **vlan_params)

    # def create_ping(self, connector, **kwargs):
    #     # Instantiate Ping with its parameters
    #     PARAMS = [
    #         "target",
    #         "resolve_target",
    #         "target_ip",
    #         "target_name",
    #         "source",
    #         "instance",
    #         "count",
    #         "timeout",
    #         "size",
    #         "df_bit",
    #         "interval",
    #         "ttl",
    #     ]
    #     ping_args = {x: kwargs[x] for x in kwargs if x in PARAMS}
    #     ping = ping_factory.get_builder(
    #         f"{connector.metadata.implementation}", **ping_args
    #     )

    #     # Run
    #     raw_data = connector.run(ping.commands())

    #     # Parse ping(s)
    #     ping_parser = ping_factory.get_parser(f"{connector.implementation}")
    #     ping.result = ping_parser.parse(raw_data, **kwargs)
    #     return ping

    # def update(self, connector, ping_obj, **kwargs):
    #     # Get new data
    #     raw_data = connector.run(ping_obj.commands())

    #     # Parse Ping
    #     ping_parser = ping_factory.get_parser(f"{connector.implementation}")
    #     return ping_parser.update(raw_data, ping_obj, **kwargs)


class PingFactory(ObjectFactory):
    "Registers new implementation for commands to generate ping data"

    def get_builder(self, builder, **kwargs):
        return self.create(builder, **kwargs)

    def get_parser(self, parser, **kwargs):
        return self.parse(parser, **kwargs)


ping_factory = PingFactory()

ping_factory.register_builder(
    "EOS-PYEAPI", {"entity": pyeapier.Ping, "collection": pyeapier.Pings}
)
ping_factory.register_parser("EOS-PYEAPI", pyeapier.PingParser)

ping_factory.register_builder("IOS-NETMIKO", ios_netmikoer.Ping)
ping_factory.register_parser("IOS-NETMIKO", ios_netmikoer.PingParser)

ping_factory.register_builder(
    "LINUX-SUBPROCESS", {"entity": subprocesser.Ping, "collection": subprocesser.Pings}
)
ping_factory.register_parser("LINUX-SUBPROCESS", subprocesser.PingParser)
ping_factory.register_builder(
    "LINUX-PARAMIKO", {"entity": paramikoer.Ping, "collection": paramikoer.Pings}
)
ping_factory.register_parser("LINUX-PARAMIKO", paramikoer.PingParser)

ping_factory.register_builder("XR-NETMIKO", xr_netmikoer.Ping)
ping_factory.register_parser("XR-NETMIKO", xr_netmikoer.PingParser)

ping_factory.register_builder("XE-NETMIKO", xe_netmikoer.Ping)
ping_factory.register_parser("XE-NETMIKO", xe_netmikoer.PingParser)

ping_factory.register_builder("NXOS-NXAPI", nxapier.Ping)
ping_factory.register_parser("NXOS-NXAPI", nxapier.PingParser)

ping_factory.register_builder("JUNOS-PYEZ", pyezer.Ping)
ping_factory.register_parser("JUNOS-PYEZ", pyezer.PingParser)
