import re
from typing import List
from netapi.probe.ping import PingBase, PingParserBaseBSD

PATTERNS = {
    "nxos": re.compile(
        r"(?P<tx>\d+) packets transmitted, (?P<rx>\d+) packets received, "
        r"(?P<loss>\d+\.\d+)% packet loss\nround-trip min/avg/max = "
        r"(?P<min>\d+(\.\d+)?)/(?P<avg>\d+(\.\d+)?)/(?P<max>\d+(\.\d+)?).*",
        re.MULTILINE,
    )
}

TIMEOUT_PATTERNS = {
    "nxos": re.compile(
        r"(?P<tx>\d+) packets transmitted, (?P<rx>\d+) packets received, "
        r"(?P<loss>\d+\.\d+)% packet loss"
    )
}


class Ping(PingBase):
    def __post_init__(self, **_ignore):
        super().__post_init__()
        self.metadata.implementation = "NXOS-NXAPI"

    # Overriding defaults for nxos
    def ping_parameters(self):
        "Ping Parameters for nxos"
        params: List = []
        if self.size:
            params.append(f"packet-size {self.size}")
        if self.count:
            params.append(f"count {self.count}")
        if self.timeout:
            params.append(f"timeout {self.timeout}")
        if self.source:
            params.append(f"source {self.source}")
        if self.df_bit:
            params.append(f"df-bit")
        if self.interval:
            params.append(f"interval {self.interval}")
        if self.ttl:
            params.append(f"ttl {self.ttl}")
        return params

    # Overriding defaults for the nxos
    def ping_base_cmd(self) -> List[str]:
        "Ping base command for nxos"
        # If resolve_target was selected it will use the target IP for the ping
        if self.resolve_target:
            target = str(self.target_ip)
        else:
            target = self.target
        ping_base_cmd: List = ["ping", target]
        if self.instance is not None:
            ping_base_cmd.append(f"vrf {self.instance}")

        return ping_base_cmd


class PingParser(PingParserBaseBSD):
    def ping_pattern(self):
        return PATTERNS["nxos"]

    def ping_timeout_pattern(self):
        return TIMEOUT_PATTERNS["nxos"]
