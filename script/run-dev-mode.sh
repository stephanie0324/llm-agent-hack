#!/bin/bash -e

# Ensure you're in the correct directory
PRJ_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"/..
cd ${PRJ_DIR}

# Set the Docker image name explicitly
IMAGE_NAME=$(bash script/get-image-name.sh)

# Run the Docker container with bash as the entrypoint
# Expose port
docker run \
    -p 8501:8501 \
    -v ${PRJ_DIR}/app:/app \
    --rm \
    -it \
    --entrypoint bash \
    $IMAGE_NAME
