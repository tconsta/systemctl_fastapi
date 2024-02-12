import dataclasses
import enum


class ServiceState(enum.Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    NOT_FOUND = 'not-found'


@dataclasses.dataclass(frozen=True)
class ServiceInfo:
    service_state: ServiceState
    systemctl_output: str
