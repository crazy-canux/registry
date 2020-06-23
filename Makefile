VERSION = $(shell awk -F '=' '$$1~/version/ {print $$2}' ./fish/__init__.py | awk -F '"' '{print $$2}')

help:
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "install - install the package to the active Python's site-packages"
	@echo "whl - package wheel"
	@echo "tgz - package tgz"
	@echo "gitlab - tag on gitlab"
	@echo "release PW=<release server password> - package upload to release server"
	@echo "image - build docker image"
	@echo "fileset - build docker image with fileset"
	@echo "harbor PW=<release server password> - push image to harbor"
	@echo "deps - make dependency image"
	@echo "debug - make debug image"

clean: clean-build clean-pyc

clean-build:
	rm -rf build/
	rm -rf registry.egg-info/
	rm -rf dist/
	rm -f registry*_image.tgz

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

install: clean
	pip3 install -r requirements.txt
	python3 setup.py install --force

image:
	docker build --network=host --no-cache -t harbor.domain.com/registry/registry:$(VERSION) .
	docker tag harbor.domain.com/registry/registry:$(VERSION) harbor.domain.com/registry/registry:latest

