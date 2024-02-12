# Web service allowing to check systemctl status X.

It's a test assignment for a job.

## Task

> Create a simple FastAPI service that will check the status of the transferred service on a Linux server (systemctl status X)  
> The service must accept GET requests with one parameter - the service name.  
> The response to the request should return the result of the command in JSON or an error message if the service was not found."
 
## Solution

Currently, the service is up and running on AWS, and can be accessed here:

https://35.156.224.125/systemctl/status?service=boot-efi.mount

`curl -X GET "https://35.156.224.125/systemctl/status?service=boot-efi.mount"`

Server: t2.micro, Ubuntu.

Although it would be much easier to use Docker, instead I installed pyenv (+ Python build dependencies), Python 3.12, pipx, poetry.
