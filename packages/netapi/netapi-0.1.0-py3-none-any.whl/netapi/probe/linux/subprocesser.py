import datetime
import re
from typing import List
from netapi.probe.ping import PingBase, PingsBase, PingParserBaseBSD

PATTERNS = {
    "linux": re.compile(
        r"(?P<tx>\d+) packets transmitted, (?P<rx>\d+) (packets )?received,"
        r"(\s+\+\d+\serrors,)? (?P<loss>\d+(\.\d+)?)% packet loss(, time .*|, .*)?"
        r"\n(rtt|round-trip) min/avg/max/(mdev|stddev) = (?P<min>\d+\.\d+)/"
        r"(?P<avg>\d+\.\d+)/(?P<max>\d+\.\d+)/(?P<mdev>\d+\.\d+).*",
        re.MULTILINE,
    )
}

TIMEOUT_PATTERNS = {
    "linux": re.compile(
        r"(?P<tx>\d+) packets transmitted, (?P<rx>\d+) (packets )?received,"
        r"(\s+\+\d+\serrors,)? (?P<loss>\d+(\.\d+)?)% packet loss(, time .*)?"
    )
}


class Pings(PingsBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.metadata.implementation = "LINUX-SUBPROCESS"

    def command(self, targets, **kwargs):
        "Creates Ping objects on a per target basis"
        if not isinstance(targets, list):
            raise TypeError("targets must be a list")
        _commands = []
        for _target in targets:
            _ping = Ping(target=_target)
            self.update({_target: _ping})
            _commands.append(_ping.command())
        return _commands

    def get_all(self, connector):
        "Automatic trigger an update. A connector object has to be passed"
        if connector.metadata.implementation != "LINUX-SUBPROCESS":
            raise ValueError(
                "Connector is not of the correct implementation: LINUX-SUBPROCESS"
            )
        for _ping in self:
            PingParser().parse(connector.run(self[_ping].command()), self[_ping])
            self[_ping].metadata.updated_at = datetime.datetime.now()
            self[_ping].metadata.collection_count += 1
        return True


class Ping(PingBase):
    def __post_init__(self, **_ignore):
        super().__post_init__()
        self.metadata.implementation = "LINUX-SUBPROCESS"

    # Overriding defaults for linux
    def ping_parameters(self):
        "Ping Parameters for linux"
        params: List = []
        if self.size:
            params.append(f"-s {self.size}")
        if self.count:
            params.append(f"-c {self.count}")
        if self.timeout:
            params.append(f"-W {self.timeout}")
        if self.source:
            params.append(f"-I {self.source}")
        if self.interval:
            params.append(f"-i {self.interval}")
        if self.ttl:
            params.append(f"-t {self.ttl}")
        return params

    # Overriding defaults for the linux
    def ping_base_cmd(self) -> List[str]:
        "Ping base command for linux"
        # If resolve_target was selected it will use the target IP for the ping
        if self.resolve_target:
            target = str(self.target_ip)
        else:
            target = self.target
        if self.instance is not None:
            ping_base_cmd = [f"ip netns exec {self.instance} ping", target]
        else:
            ping_base_cmd = ["ping", target]

        return ping_base_cmd

    def execute(self):
        """
        Automatic execution of entity to retrieve results.

        NOTE: It does NOT update the `updated_at` timestamp.
        """
        if self.connector is None:
            raise NotImplementedError("Need to have the connector defined")
        PingParser().parse(self.connector.run(self.command()), self)
        self.metadata.updated_at = datetime.datetime.now()
        self.metadata.collection_count += 1
        return True


class PingParser(PingParserBaseBSD):
    def parse(self, raw_data, ping_obj, **kwargs):
        "Parses the Ping output"
        data = str(list(raw_data.values())[0])
        if not data:
            raise ValueError(f"No data returned from device")

        ping_obj.result = self.data_parser(data, **kwargs)
        return True

    def collector_parse(self, raw_data, ping_objs, **kwargs):
        """
        It takes the ouput from multiple pings executions and parses them.
        NOTE: This can only be used if targets are not the same, even if they are on
        a diffent VRF.
        """
        for _command in raw_data:
            for _ping in ping_objs.values():
                if _ping.command() == _command:
                    _ping.result = self.data_parser(raw_data[_command])
        return ping_objs

    def ping_pattern(self):
        return PATTERNS["linux"]

    def ping_timeout_pattern(self):
        return TIMEOUT_PATTERNS["linux"]
