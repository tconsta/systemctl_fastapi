import re
import logging

from structures import ServiceInfo, ServiceState

logger = logging.getLogger(__name__)


class SystemctlParser:
    def parse(self, command_output: str) -> ServiceInfo:
        service_state: str | None = None

        for line in command_output.splitlines():
            if line.lstrip().startswith('Active:'):
                service_state = line.split()[1]

        not_found_regex = re.compile(r'Unit (.+) could not be found')
        match = not_found_regex.search(command_output)

        if match:
            logger.warning('Service not found: %s', match.group(1))
            service_state = ServiceState.NOT_FOUND.value

        if not service_state:
            logger.error('Systemctl output is invalid: %s', command_output)
            raise ValueError('Systemctl output is invalid')

        return ServiceInfo(
            service_state=ServiceState(service_state),
            systemctl_output=command_output,
        )
