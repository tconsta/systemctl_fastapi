import re
from asyncio import subprocess
import logging

from fastapi import FastAPI, Request, HTTPException

from systemctl_parser import SystemctlParser

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('app.log')],
    level=logging.DEBUG,
)
logger = logging.getLogger(__name__)

app = FastAPI()

# allows only lowercase letters, numbers, and the following characters: \-_.
SAFE_REGEX = re.compile(r'^[a-zA-Z0-9\\._-]+$')


@app.get(
    path='/systemctl/status',
    tags=['systemctl'],
    summary='Get service status using systemctl.',
)
async def get_service_status(request: Request):
    logger.info('Received request: %s', request.url)
    service_name = request.query_params.get('service')

    if not service_name or not SAFE_REGEX.match(service_name):
        logger.warning('Invalid service name: %s', service_name)
        raise HTTPException(
            status_code=400,
            detail='Service name is not specified or invalid/unsafe',
        )

    command = ['systemctl', 'status', service_name]
    logger.info('Executing command: %s', ' '.join(command))

    process = await subprocess.create_subprocess_exec(
        *command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if process.returncode:
        logger.error('Failed to execute systemctl status: %s', process.stderr)
        raise HTTPException(status_code=500, detail=process.stderr)

    stdout, stderr = await process.communicate()
    logger.debug('stdout: %s, stderr: %s', stdout, stderr)
    command_output = stdout.decode() or stderr.decode()
    service_info = SystemctlParser().parse(command_output)

    return {
        'service_state': service_info.service_state.value,
        'systemctl_output': service_info.systemctl_output,
    }
