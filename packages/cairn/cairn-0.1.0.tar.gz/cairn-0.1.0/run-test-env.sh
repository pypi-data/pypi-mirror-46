#!/bin/bash
set -e

# run the docker container
docker run -it --rm -v $(pwd):/src python-tox
