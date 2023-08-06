import re
from netapi.probe.ping import PingBase, PingParserBaseIos

PATTERNS = {
    "xe": re.compile(
        r"Success rate is (?P<rate>\d+) percent \((?P<tx>\d+)/(?P<rx>\d+)\),"
        r" round-trip min/avg/max = (?P<min>\d+)/(?P<avg>\d+)/(?P<max>\d+) .*"
    )
}

TIMEOUT_PATTERNS = {
    "xe": re.compile(
        r"Success rate is (?P<rate>\d+) percent \((?P<tx>\d+)/(?P<rx>\d+)\)"
    )
}


class Ping(PingBase):
    def __post_init__(self, **_ignore):
        super().__post_init__()
        self.metadata.implementation = "XE-NETMIKO"

    def ping_parameters(self):
        "Ping parameters for XE"
        # Retrieve parameters from main class and expand
        params = super().ping_parameters()
        if self.df_bit:
            params.append(f"df-bit")
        return params


class PingParser(PingParserBaseIos):
    def ping_pattern(self):
        return PATTERNS["xe"]

    def ping_timeout_pattern(self):
        return TIMEOUT_PATTERNS["xe"]
