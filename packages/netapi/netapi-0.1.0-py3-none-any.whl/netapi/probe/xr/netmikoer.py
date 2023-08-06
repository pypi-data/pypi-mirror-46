import re
from typing import List
from netapi.probe.ping import PingBase, PingParserBaseIos

PATTERNS = {
    "xr": re.compile(
        r"Success rate is (?P<rate>\d+) percent \((?P<tx>\d+)/(?P<rx>\d+)\),"
        r" round-trip min/avg/max = (?P<min>\d+)/(?P<avg>\d+)/(?P<max>\d+) .*"
    )
}

TIMEOUT_PATTERNS = {
    "xr": re.compile(
        r"Success rate is (?P<rate>\d+) percent \((?P<tx>\d+)/(?P<rx>\d+)\)"
    )
}


class Ping(PingBase):
    def __post_init__(self, **_ignore):
        super().__post_init__()
        self.metadata.implementation = "XR-NETMIKO"

    def ping_parameters(self):
        "Ping parameters for XR"
        params = super().ping_parameters()
        if self.df_bit:
            params.append(f"donotfrag")
        return params

    def ping_base_cmd(self) -> List[str]:
        "Ping base command for xr"
        # If resolve_target was selected it will use the target IP for the ping
        if self.resolve_target:
            target = str(self.target_ip)
        else:
            target = self.target
        ping_base_cmd: List = ["ping", target]
        if self.instance is not None:
            ping_base_cmd.append(f"vrf {self.instance}")

        return ping_base_cmd


class PingParser(PingParserBaseIos):
    def ping_pattern(self):
        return PATTERNS["xr"]

    def ping_timeout_pattern(self):
        return TIMEOUT_PATTERNS["xr"]
