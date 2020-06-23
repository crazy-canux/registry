"""
client workflow:
0. running inside container on CSa.
1. http API to dump metadata.
2. implement registry v2 http API.
3. decrypt and unzip upload files.
"""
import glob
import hashlib
import os
import logging

from .config import Config


logger = logging.getLogger()


def generate_metadata():
    config = Config()
    metadata = config.get_metadata()
    location = config.get_path()
    fd = open(metadata, "w")
    for file in glob.glob(os.path.join(location, "*/**"), recursive=True):
        if os.path.isfile(file):
            logger.info("processing {}".format(file))
            relative = file[10:]
            sha256 = hashlib.sha256()
            f = open(file, "rb")
            while True:
                chunk = f.read(65536)
                if not chunk:
                    break
                sha256.update(chunk)
            sha256 = sha256.hexdigest()
            fd.write("%s %s\n" % (sha256, relative))
