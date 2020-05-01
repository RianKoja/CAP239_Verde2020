#!/bin/bash
###########################################################################################################
# Prepares environment, builds docker image to run a Python project and executes it.
#
# Written by Rian Koja to publish in a GitHub repository with specified licence.
###########################################################################################################

# Prepare environment:
echo "Running $0 script..."

PATH_SCRIPT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $PATH_SCRIPT

# Prepare x-host
#if not installed, then install it:
if [ $(dpkg-query -W -f='${Status}' x11-xserver-utils 2>/dev/null | grep -c "ok installed") -eq 0 ];
then
    sudo apt-get install x11-xserver-utils
    xhost +
fi
# Set up monitor:
xhost local:root

# Check if target project is specified at the input:
if [ $# -lt 1 ]; then
    echo "Call this script with the folder name of the required project."
    exit 1
fi

# Build docker image:
docker build --build-arg target_dir="./$1" -t runner_$1 -f ./DockerFiles/Dockerfile . \
      || { echo "Building image with $1 failed, exiting $0"; exit 1; }

# Run docker image:
docker run -it --rm \
           -v /tmp/.X11-unix:/tmp/.X11-unix \
           -e DISPLAY=unix$DISPLAY \
           -v "$PATH_SCRIPT/$1/mount:/project/mount" \
           --user $(id -u):$(id -g) \
           "runner_$1" \
           || { echo "Running container for $1 failed, exiting $0"; exit 1; }

echo "Finished $0 script."