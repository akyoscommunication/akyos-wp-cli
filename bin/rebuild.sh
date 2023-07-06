#!/bin/bash

cwd=$(pwd)

docker build -t aky-cli -f ./../.docker/Dockerfile --no-cache .
# docker run --rm --network="host" -it -v "$(pwd)":/cwd -v "$HOME/.aky/config.json":"/root/.aky/config.json" aky-cli "$@"

cd "$cwd" || exit
