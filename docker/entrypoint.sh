#!/bin/bash

# Set options to exit immediately if any command in the script fails,
# if any variable is unset, and if any command in a pipeline fails
set -o errexit -o nounset -o pipefail

# This command restarts the ssh service
service ssh restart

# This command restarts the xrdp service using the init script
/etc/init.d/xrdp restart

# This command starts the zsh shell
zsh
