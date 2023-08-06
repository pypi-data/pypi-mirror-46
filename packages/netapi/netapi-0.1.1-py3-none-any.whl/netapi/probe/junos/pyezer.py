import re
from typing import List
from netapi.probe.ping import PingBase, PingParserBaseBSD

PATTERNS = {
    "junos": re.compile(
        r"(?P<tx>\d+) packets transmitted, (?P<rx>\d+) packets received, "
        r"(?P<loss>\d+)% packet loss\nround-trip min/avg/max/stddev = "
        r"(?P<min>\d+\.\d+)/(?P<avg>\d+\.\d+)/(?P<max>\d+\.\d+).*",
        re.MULTILINE,
    )
}

TIMEOUT_PATTERNS = {
    "junos": re.compile(
        r"(?P<tx>\d+) packets transmitted, (?P<rx>\d+) packets received, "
        r"(?P<loss>\d+)% packet loss"
    )
}


class Ping(PingBase):
    def __post_init__(self, **_ignore):
        super().__post_init__()
        self.metadata.implementation = "JUNOS-PYEZ"

    # Overriding defaults for Junos
    def ping_parameters(self):
        "General Ping parameters in most platforms"
        params: List = []
        if self.size:
            params.append(f"size {self.size}")
        if self.count:
            params.append(f"count {self.count}")
        if self.timeout:
            params.append(f"wait {self.timeout}")
        if self.source:
            params.append(f"source {self.source}")
        if self.df_bit:
            params.append(f"do-not-fragment")
        if self.interval:
            params.append(f"interval {self.interval}")
        if self.ttl:
            params.append(f"ttl {self.ttl}")
        return params

    # verriding defaults for the Junos
    def ping_base_cmd(self) -> List[str]:
        "Ping base command for Junos"
        # If resolve_target was selected it will use the target IP for the ping
        if self.resolve_target:
            target = str(self.target_ip)
        else:
            target = self.target
        ping_base_cmd: List = ["ping", target]
        if self.instance is not None:
            ping_base_cmd.append(f"routing-instance {self.instance}")

        return ping_base_cmd


class PingParser(PingParserBaseBSD):
    def ping_pattern(self):
        return PATTERNS["junos"]

    def ping_timeout_pattern(self):
        return TIMEOUT_PATTERNS["junos"]
