import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'service_name, expected_status',
    [
        ('boot-efi.mount', 'active'),
        ('vgauth.service', 'inactive'),
        ('asdf', 'not-found'),
    ],
)
async def test_get_service_status(
    service_name: str,
    expected_status: str,
) -> None:
    response = client.get(f"/systemctl/status?service={service_name}")
    service_info = response.json()
    assert response.status_code == 200
    assert service_info['service_state'] == expected_status
    assert 'systemctl_output' in response.json()
