import re

from structures import ServiceInfo, ServiceState


class SystemctlParser:
    def parse(self, command_output: str) -> ServiceInfo:
        service_state: str | None = None

        for line in command_output.splitlines():
            if line.lstrip().startswith('Active:'):
                service_state = line.split()[1]

        not_found_regex = re.compile(r'Unit (.+) could not be found')
        match = not_found_regex.search(command_output)

        if match:
            service_state = ServiceState.NOT_FOUND.value

        if not service_state:
            raise ValueError('Systemctl output is invalid')

        return ServiceInfo(
            service_state=ServiceState(service_state),
            systemctl_output=command_output,
        )
