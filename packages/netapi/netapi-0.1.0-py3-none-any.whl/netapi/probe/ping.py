import abc
import re
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List, Pattern, Match
from netaddr import IPAddress
from netapi.metadata import Metadata, EntityCollections
from netapi.probe.utils import addresser


@dataclass(unsafe_hash=True)
class PingBase:
    """
    Ping instance creator. It creates a ping object based on parameters passed to it for
    construction.

    Attributes:
        `target` (str): IP or Host target
        `resolve_target` (bool): Resolve IP address and name assigned to attributes
        for the likes of `target_ip` and `target_name`
        `target_ip` (str): IPAddress object returned (Optional)
        `target_name` (str): Hostname of target (Optional)
        `source` (str): IP or Interface source of the request
        `instance` (str): instance/vrf for the ping object
        `count` (int): Number of probes
        `timeout` (int): Timeout for when a probe is marked as unreachable
        `size` (int): Packet size of the ping probes
        `df_bit` (bool): Do not fragment bit to be set
        `interval` (float): Time interval between each probe
        `ttl` (int): Time-to-live value for the probes
    """

    target: str
    resolve_target: bool = True
    target_ip: Optional[Any] = None
    _target_ip: Optional[Any] = field(init=False, repr=False)
    target_name: Optional[str] = field(init=False, repr=True, default=None)
    source: Optional[str] = None
    instance: Optional[str] = None
    count: Optional[int] = 5
    timeout: Optional[int] = 2
    size: Optional[int] = 692
    df_bit: Optional[bool] = False
    interval: Optional[float] = 1.0
    ttl: Optional[int] = None
    result: Dict = field(default_factory=dict, init=False)
    connector: Optional[Any] = field(default=None, repr=False)

    def __post_init__(self, **_ignore):
        self.metadata = Metadata(name="ping", type="entity")
        if self.resolve_target and not self.target_ip:
            self.target_ip, self.target_name = addresser(
                self.target, dns_query_attempt=3
            )
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
    def target_ip(self) -> IPAddress:
        return self._target_ip

    @target_ip.setter
    def target_ip(self, value: Any) -> None:
        # Workaround for when the value is not set
        if str(type(value)) in "<class 'property'>":
            self._target_ip = None
        else:
            self._target_ip = IPAddress(value)

    def ping_parameters(self) -> List[str]:
        "General Ping parameters in most platforms"
        params: List = []
        if self.size:
            params.append(f"size {self.size}")
        if self.count:
            params.append(f"repeat {self.count}")
        if self.timeout:
            params.append(f"timeout {self.timeout}")
        if self.source:
            params.append(f"source {self.source}")
        return params

    def ping_base_cmd(self) -> List[str]:
        "General base ping command"
        ping_base_cmd: List = []
        # If resolve_target was selected it will use the target IP for the ping
        if self.resolve_target:
            target = str(self.target_ip)
        else:
            target = self.target
        if self.instance is not None:
            ping_base_cmd = ["ping", f"vrf {self.instance}", target]

        else:
            ping_base_cmd = ["ping", target]
        return ping_base_cmd

    def command(self, **kwargs) -> str:
        """
        Generate the command used to execute the ping

        Returns:
            command: String of complete ping command
        """
        params = self.ping_parameters()
        ping_base_cmd = self.ping_base_cmd()

        return " ".join(ping_base_cmd + params)


class PingParserBase(metaclass=abc.ABCMeta):
    def parse(self, raw_data, **kwargs):
        data = list(raw_data.values())[0].get("messages")[0]
        result = self.data_parser(data, **kwargs)
        return result

    def data_parser(
        self,
        data: str,
        verbose: Optional[bool] = False,
        warning_threshold: Optional[int] = None,
        critical_threshold: Optional[int] = None,
        **_ignore,
    ) -> dict:
        """
        Accepts the raw input of the remote ping and returns its parsed output

        Args:
            result: Raw string of ping output
            verbose: Set verbose output

        Returns:
            parsed_result: Dictionary with the results of the parsing

            parsed_result = dict(
                probes_sent=10,
                probes_received=10,
                packet_loss=0.0,
                rtt_min=2.3,
                rtt_avg=2.4,
                rtt_max=2.5,
                flag='green',
                alert=False,
                status_code=0,
                status_up: True
            )
        """
        result: Dict = {}
        _ping_match = re.search(self.ping_pattern(), data)
        _ping_timeout_match = re.search(self.ping_timeout_pattern(), data)

        # Execute parser logic
        self._data_parser_logic(result, _ping_match, _ping_timeout_match, verbose)

        # Apply basic analysis metadata
        self.result_apply_analysis(
            result,
            warning_threshold=warning_threshold,
            critical_threshold=critical_threshold,
        )
        return result

    def _data_parser_logic(self, result, ping_match_obj, timeout_match_obj, verbose):
        # result: Dict = {}
        if ping_match_obj:
            if verbose:
                print("[DEBUG] MATCH FOUND: {}".format(ping_match_obj.groupdict()))
            result.update(self.ping_match_data(ping_match_obj))
        elif timeout_match_obj:
            if verbose:
                print(
                    "[DEBUG] MATCH TIMEOUT FOUND: {}".format(
                        timeout_match_obj.groupdict()
                    )
                )
            result.update(self.ping_match_timeout_data(timeout_match_obj))

        # Verification if no match was performed
        if not result:
            raise ValueError("[WARNING] Not able to parse ping output")

    def _default_analysis(self, result: Dict):
        if result["packet_loss"] < 1.0:
            if result["packet_loss"] != 0.0:
                result.update(flag="yellow", alert=True, status_code=1, status_up=True)

            else:
                result.update(flag="green", alert=False, status_code=0, status_up=True)
        else:
            result.update(flag="red", status_code=2, status_up=False, alert=True)

    def result_apply_analysis(
        self,
        result: Dict,
        warning_threshold: Optional[int] = None,
        critical_threshold: Optional[int] = None,
    ):
        """
        Applies warning/critical thresholds for the analysis.

        Args:
            `critical_threshold`: Packet loss above this value is flagged as `red`
            `warning_threshold`: Packet loss above this value is flagged as `yellow`

            Note: If `warning_threshold` was set and packer loss is below the percentage
            it is then flagged as `green`

        Default it uses the built-in analysis:
        `packet_loss` >= 100 -> `red`
        `packet_loss` == 0   -> `green`
        `packet_loss` != 0   -> `yellow`
        """
        _packet_loss = result["packet_loss"]
        if warning_threshold is None and critical_threshold is None:
            _method = "default"
        else:
            _method = "trigger"

        if _method == "trigger":
            _analysed = False
            if critical_threshold:
                if _packet_loss * 100 > critical_threshold:
                    result.update(
                        flag="red", alert=True, status_code=2, status_up=False
                    )
                    _analysed = True
            if warning_threshold:
                if _packet_loss * 100 > warning_threshold:
                    result.update(
                        flag="yellow", alert=True, status_code=1, status_up=True
                    )
                    _analysed = True
                else:
                    if not _analysed:
                        result.update(
                            flag="green", alert=True, status_code=0, status_up=True
                        )
                        _analysed = True
            if not _analysed:
                self._default_analysis(result)

        elif _method == "default":
            self._default_analysis(result)

    @abc.abstractmethod
    def ping_pattern(self) -> Pattern:
        pass

    @abc.abstractmethod
    def ping_timeout_pattern(self) -> Pattern:
        pass

    @abc.abstractmethod
    def ping_match_data(self, match_obj: Match) -> Dict:
        pass

    @abc.abstractmethod
    def ping_match_timeout_data(self, match_obj: Match) -> Dict:
        pass


class PingParserBaseBSD(PingParserBase):
    def ping_match_data(self, match_obj):
        return dict(
            probes_sent=int(match_obj.group("tx")),
            probes_received=int(match_obj.group("rx")),
            packet_loss=float("{:.4f}".format(float(match_obj.group("loss")) / 100)),
            rtt_min=float(match_obj.group("min")),
            rtt_avg=float(match_obj.group("avg")),
            rtt_max=float(match_obj.group("max")),
        )

    def ping_match_timeout_data(self, match_obj):
        return dict(
            probes_sent=int(match_obj.group("tx")),
            probes_received=int(match_obj.group("rx")),
            packet_loss=float("{:.4f}".format(float(match_obj.group("loss")) / 100)),
        )


class PingParserBaseIos(PingParserBase):
    def ping_match_data(self, match_obj):
        return dict(
            probes_sent=int(match_obj.group("tx")),
            probes_received=int(match_obj.group("rx")),
            packet_loss=float(
                "{:.4f}".format(1 - (int(match_obj.group("rate")) / 100))
            ),
            rtt_min=float(match_obj.group("min")),
            rtt_avg=float(match_obj.group("avg")),
            rtt_max=float(match_obj.group("max")),
        )

    def ping_match_timeout_data(self, match_obj):
        return dict(
            probes_sent=int(match_obj.group("tx")),
            probes_received=int(match_obj.group("rx")),
            packet_loss=float(
                "{:.4f}".format(1 - (int(match_obj.group("rate")) / 100))
            ),
        )


class PingsBase(EntityCollections):
    ENTITY = "ping"

    def __init__(self, *args, **kwargs):
        super().__init__(entity=self.ENTITY, *args, **kwargs)
        self.metadata = Metadata(name="pings", type="collection")

    def __setitem__(self, *args, **kwargs):
        super().__setitem__(*args, entity=self.ENTITY, **kwargs)
