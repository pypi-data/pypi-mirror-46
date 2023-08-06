import re
from netapi.probe.ping import PingBase, PingParserBaseIos

PATTERNS = {
    "ios": re.compile(
        r"Success rate is (?P<rate>\d+) percent \((?P<tx>\d+)/(?P<rx>\d+)\),"
        r" round-trip min/avg/max = (?P<min>\d+)/(?P<avg>\d+)/(?P<max>\d+) .*"
    )
}

TIMEOUT_PATTERNS = {
    "ios": re.compile(
        r"Success rate is (?P<rate>\d+) percent \((?P<tx>\d+)/(?P<rx>\d+)\)"
    )
}


class Ping(PingBase):
    # Minimalistic ping
    def __post_init__(self, **_ignore):
        super().__post_init__()
        self.metadata.implementation = "IOS-NETMIKO"


class PingParser(PingParserBaseIos):
    def ping_pattern(self):
        return PATTERNS["ios"]

    def ping_timeout_pattern(self):
        return TIMEOUT_PATTERNS["ios"]
