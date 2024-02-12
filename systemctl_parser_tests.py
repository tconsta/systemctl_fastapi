import pytest

from structures import ServiceInfo, ServiceState
from systemctl_parser import SystemctlParser


@pytest.mark.parametrize('command_output, expected_service_info', [
    (
        (
            '● some_service.service - Some service\n'
            '   Loaded: loaded (/lib/systemd/system/some_service.service; '
            'enabled; vendor preset: enabled)\n'
            '   Active: active (running) since Fri 2021-09-24 14:00:00 MSK;'
            ' 1 day 2h ago\n'
            ' Main PID: 1234 (some_service)\n'
            '   CGroup: /system.slice/some_service.service\n'
            '           └─1234 /usr/bin/some_service\n'
        ),
        ServiceInfo(
            service_state=ServiceState.ACTIVE,
            systemctl_output=(
                '● some_service.service - Some service\n'
                '   Loaded: loaded (/lib/systemd/system/some_service.service; '
                'enabled; vendor preset: enabled)\n'
                '   Active: active (running) since Fri 2021-09-24 14:00:00 MSK;'
                ' 1 day 2h ago\n'
                ' Main PID: 1234 (some_service)\n'
                '   CGroup: /system.slice/some_service.service\n'
                '           └─1234 /usr/bin/some_service\n'
            ),
        ),
    ),
    (
        (
            '● some_service.service - Some service\n'
            '   Loaded: loaded (/lib/systemd/system/some_service.service; '
            'enabled; vendor preset: enabled)\n'
            '   Active: inactive (dead) since Fri 2021-09-24 14:00:00 MSK;'
            ' 1 day 2h ago\n'
            ' Main PID: 1234 (some_service)\n'
            '   CGroup: /system.slice/some_service.service\n'
            '           └─1234 /usr/bin/some_service\n'
        ),
        ServiceInfo(
            service_state=ServiceState.INACTIVE,
            systemctl_output=(
                '● some_service.service - Some service\n'
                '   Loaded: loaded (/lib/systemd/system/some_service.service; '
                'enabled; vendor preset: enabled)\n'
                '   Active: inactive (dead) since Fri 2021-09-24 14:00:00 MSK;'
                ' 1 day 2h ago\n'
                ' Main PID: 1234 (some_service)\n'
                '   CGroup: /system.slice/some_service.service\n'
                '           └─1234 /usr/bin/some_service\n'
            ),
        ),
    ),
    (
        (
            'Unit some_service.service could not be found.'
        ),
        ServiceInfo(
            service_state=ServiceState.NOT_FOUND,
            systemctl_output='Unit some_service.service could not be found.',
        ),
    ),
])
def test_parser(
    command_output: str,
    expected_service_info: str,
) -> None:
    parser = SystemctlParser()

    assert parser.parse(command_output) == expected_service_info


def test_parser_raises_value_error_on_invalid_output() -> None:
    parser = SystemctlParser()

    with pytest.raises(ValueError):
        parser.parse('invalid output')
