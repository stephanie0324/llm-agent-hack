#!/bin/bash -e

# === Set project directory ===
PRJ_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"/..
cd "${PRJ_DIR}"

# === Load environment variables from .env ===
ENV_FILE="./deploy/.env"
if [ -f "$ENV_FILE" ]; then
    export $(grep -v '^#' "$ENV_FILE" | xargs)
else
    echo "❌ .env file not found at $ENV_FILE"
    exit 1
fi

# === Set SSL certificates fallback if not already set ===
export REQUESTS_CA_BUNDLE="${REQUESTS_CA_BUNDLE:-/etc/ssl/certs/ca-certificates.crt}"
export SSL_CERT_FILE="${SSL_CERT_FILE:-$REQUESTS_CA_BUNDLE}"

# === Get Docker image name ===
IMAGE_NAME=$(bash script/get-image-name.sh)

# === Run Docker ===
docker run \
    -p "${HOST_PORT}:8501" \
    -v "${PRJ_DIR}/app:/app" \
    --rm \
    -it \
    --entrypoint bash \
    --dns 140.96.216.194 \
    --dns 140.96.216.196 \
    -e REQUESTS_CA_BUNDLE \
    -e SSL_CERT_FILE \
    -e LOCAL_MODEL_NAME="${LOCAL_MODEL_NAME}" \
    -e LOCAL_MODEL_API="${LOCAL_MODEL_API}" \
    -e AZURE_DEPLOYMENT="${AZURE_DEPLOYMENT}" \
    -e AZURE_OPENAI_ENDPOINT="${AZURE_OPENAI_ENDPOINT}" \
    -e AZURE_OPENAI_API_KEY="${AZURE_OPENAI_API_KEY}" \
    -e AZURE_API_VERSION="${AZURE_API_VERSION}" \
    -e WEATHER_API_KEY="${WEATHER_API_KEY}" \
    -v /etc/ssl/certs:/etc/ssl/certs \
    "$IMAGE_NAME"
