import os
import sys
import hashlib
import logging
import secrets

from fastapi import FastAPI, Response, status, Depends, HTTPException, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import FileResponse
import uvicorn

from registry.config import Config


logger = logging.getLogger()
conf = Config()
username = "username"
password = "password"

app = FastAPI()
sec = HTTPBasic()


def verify_auth(credentials: HTTPBasicCredentials = Depends(sec)):
    correct_username = secrets.compare_digest(credentials.username, username)
    correct_password = secrets.compare_digest(credentials.password, password)
    if not (correct_password and correct_username):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="",
            headers={"WWW-Authenticate": "Basic"}
        )
    return credentials.username


@app.get("/v2/", status_code=200)
async def ping(response: Response, request: Request):
    logger.debug(request.headers)
    response.headers["Docker-Distribution-Api-Version"] = "registry/2.0"
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    response.headers["Content-Length"] = "2"
    response.status_code = status.HTTP_200_OK
    logger.debug(response.headers)
    return {}


@app.get("/v2/_catalog", status_code=200)
async def list_repo(request: Request):
    logger.debug(request.headers)
    registry = conf.get_registry_dir()
    m_dir = os.path.join(registry, "manifests")
    repos = list()
    for pro in os.listdir(m_dir):
        for name in os.listdir(os.path.join(m_dir, pro)):
            repos.append("{}/{}".format(pro, name))
    resp = {
        "repositories": repos
    }
    logger.debug(resp)
    response = Response(content=json.dumps(resp))
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    response.status_code = status.HTTP_200_OK
    logger.debug(response.headers)
    return response


@app.get("/v2/{name:path}/tags/list", status_code=200)
async def list_tags(name, request: Request):
    logger.debug(request.headers)
    registry = conf.get_registry_dir()
    resp = {
        "name": name,
        "tags": [
            tag.strip()
            for tag in os.listdir(os.path.join(registry, "manifests", name))
            if tag.strip()
        ]
    }
    logger.debug(resp)
    response = Response(content=json.dumps(resp))
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    response.status_code = status.HTTP_200_OK
    logger.debug(response.headers)
    return response


@app.get("/v2/{name:path}/manifests/{reference}", status_code=200)
async def get_manifests(name, reference, request: Request):
    logger.debug(request.headers)
    registry = conf.get_registry_dir()
    file_name = os.path.join(registry, "manifests", name, reference)
    with open(file_name, "rb") as f:
        chunk = f.read()
    sha256 = hashlib.sha256(chunk).hexdigest()
    response = FileResponse(file_name)
    response.headers["Docker-Distribution-Api-Version"] = "registry/2.0"
    response.headers["Docker-Content-Digest"] = "sha256:{}".format(sha256)
    response.headers["Content-Type"] = "application/vnd.docker.distribution.manifest.v2+json"
    response.headers["Content-Length"] = str(len(chunk))
    response.status_code = status.HTTP_200_OK
    logger.debug(response.headers)
    return response


@app.get("/v2/{name:path}/blobs/{digest}", status_code=200)
async def get_blobs(name, digest, request: Request):
    logger.debug(request.headers)
    registry = conf.get_registry_dir()
    file_name = os.path.join(registry, "blobs", digest)
    response = FileResponse(file_name)
    response.headers["Docker-Distribution-Api-Version"] = "registry/2.0"
    response.headers["Docker-Content-Digest"] = digest
    response.headers["Content-Type"] = "application/octet-stream"
    response.headers["Content-Length"] = str(os.stat(file_name).st_size)
    response.status_code = status.HTTP_200_OK
    logger.debug(response.headers)
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(conf.get_port()), log_level="debug", ssl_keyfile="", ssl_certfile="")
