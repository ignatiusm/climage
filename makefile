BASEIMAGE := imadj
IMAGE := $(BASEIMAGE):2023-08-27

.PHONY: docker-build docker-run run-serve

## Build docker image
docker:
	docker build -t $(IMAGE) -f ./Dockerfile .

## Run docker image
run:
	docker run --rm -it -u $$(id -u):$$(id -g) $(IMAGE) /bin/bash

## Run docker image to serve the assets
serve:
	docker run --rm -it -u $$(id -u):$$(id -g) -p 8000:8000 $(IMAGE) uvicorn imadj.server:app --host 0.0.0.0
