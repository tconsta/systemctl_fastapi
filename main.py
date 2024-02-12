import re
from asyncio import subprocess

from fastapi import FastAPI, Request, HTTPException

from systemctl_parser import SystemctlParser

app = FastAPI()

# allows only lowercase letters, numbers, and the following characters: \-_.
SAFE_REGEX = re.compile(r'^[a-zA-Z0-9\\._-]+$')


@app.get(
    path='/systemctl/status',
    tags=['systemctl'],
    summary='Get service status using systemctl.',
)
async def get_service_status(request: Request):
    service_name = request.query_params.get('service')

    if not service_name or not SAFE_REGEX.match(service_name):
        raise HTTPException(
            status_code=400,
            detail='Service name is not specified or invalid/unsafe',
        )

    command = ['systemctl', 'status', service_name]
    process = await subprocess.create_subprocess_exec(
        *command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if process.returncode:
        raise HTTPException(status_code=500, detail=process.stderr)

    stdout, _ = await process.communicate()
    service_info = SystemctlParser().parse(stdout.decode())

    return {
        'service_state': service_info.service_state.value,
        'systemctl_output': service_info.systemctl_output,
    }
