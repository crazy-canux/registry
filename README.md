# registry 

registry used to upgrade docker images on air-gap mode.

***

## How to use

build docker image and deploy with docker

    $ make image
    $ docker stack deploy -c ./docker-compose.yml registry
    
***

## How to debug

swagger UI:

    http://IP:PORT/docs

ReDoc:

    http://IP:PORT/redoc
    
from cli:

    $ uvicorn registry.main:app --reload --host 0.0.0.0 --port 8080 --log-level debug
    $ gunicorn -w 2 -k uvicorn.workers.UvicornWorker --log-level debug -b 0.0.0.0:8080 registry.main:app

