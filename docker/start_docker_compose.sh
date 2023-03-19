#!/usr/bin/env bash
# Set options to exit immediately if any command in the script fails,
# if any variable is unset, and if any command in a pipeline fails
set -o errexit -o nounset -o pipefail

# Get the absolute path of the script file
script_path="$(readlink --canonicalize "${0}")"

# Get the directory path of the script file
docker_path="$(dirname "${script_path}")"

# Get the directory path of the project folder
project_path="$(dirname "${docker_path}")"

# Load environment variables from .env file
set -a
. "${docker_path}/.env"
set +a

# Set the filename of the tar archive
filename="${PROJECT_NAME}.tar.gz"

# Change to the docker directory
cd "${docker_path}"

# Create a temporary file for the tar archive
tmp_file=$(mktemp)

# Create the tar archive in the temporary file
tar --create --gzip --file "${tmp_file}" --directory="${project_path}" .

# Move the tar archive to the target directory
mv "${tmp_file}" "${docker_path}/${filename}"

# Build and start the Docker Compose project
docker-compose --file "docker-compose.yml" up --detach

# Remove the tar archive
rm "${filename}"
