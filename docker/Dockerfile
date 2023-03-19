FROM pytorch/pytorch:1.11.0-cuda11.3-cudnn8-runtime

WORKDIR /root

# No interactive frontend during docker build
ARG DEBIAN_FRONTEND=noninteractive

# Set password for superuser
ARG ROOT_PASSWORD
RUN printf "%s\n%s\n\n" "${ROOT_PASSWORD}" "${ROOT_PASSWORD}" | \
    passwd

# Add custom sshd_config
ADD sshd_config /etc/ssh/sshd_config

# Configure authorized_keys for OpenSSH
ARG PUBLIC_KEY
RUN mkdir --parents "${HOME}/.ssh" && \
    echo "${PUBLIC_KEY}" >"${HOME}/.ssh/authorized_keys"

# Update packages
RUN apt-get update

########################################################################################################################
# Development
# Development utilities, compilers, development environments, libraries, etc.
########################################################################################################################

# Install GNU Compiler Collection - C and C++ compilers
RUN apt-get install --assume-yes gcc

########################################################################################################################
# Editors
# Software to edit files. Programming environments.
########################################################################################################################

# Install NeoVim
RUN apt-get install --assume-yes neovim

########################################################################################################################
# Utilities
# Utilities for file/disk manipulation, backup and archive tools, system monitoring, input systems, etc.
########################################################################################################################

# Install lsof - utility to list open files
RUN apt-get install --assume-yes lsof

########################################################################################################################
# Version Control Systems
# Version control systems and related utilities.
########################################################################################################################

# Install Git - fast, scalable, distributed revision control system
RUN apt-get install --assume-yes git

########################################################################################################################
# Web Software
# Web servers, browsers, proxies, download tools etc.
########################################################################################################################

# Install cURL - command line tool for transferring data with URL syntax
RUN apt-get install --assume-yes curl

########################################################################################################################
# Network
# Daemons and clients to connect your system to the world.
########################################################################################################################

# OpenSSH server - secure shell (SSH) server, for secure access from remote machines
RUN apt-get install --assume-yes openssh-server

# Install Xrdp - Remote Desktop Protocol (RDP) server
RUN apt-get install --assume-yes xrdp
RUN sed -i.bak '/fi/a #xrdp multiple users configuration \nstartxfce4\n' /etc/xrdp/startwm.sh

########################################################################################################################
# Shells
# Command shells. Friendly user interfaces for beginners.
########################################################################################################################

# Z shell - Shell with lots of features
RUN apt-get install --assume-yes zsh

# Change login shell for the superuser
RUN chsh --shell "$(which zsh)" root

# Install Oh My Zsh
ARG OH_MY_ZSH_URL="https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh"
RUN sh -c "$(curl --location ${OH_MY_ZSH_URL}) --unattended"
SHELL ["zsh", "-c"]

########################################################################################################################
# Xfce
# Xfce, a fast and lightweight Desktop Environment.
########################################################################################################################

# Install Xfce - Meta-package for the Xfce Lightweight Desktop Environment
RUN apt-get install --assume-yes xfce4

########################################################################################################################
# X Window System software
# X servers, libraries, fonts, window managers, terminal emulators and many related applications.
########################################################################################################################

# Install Xfce Terminal - Xfce terminal emulator
RUN apt-get install --assume-yes xfce4-terminal && \
    update-alternatives --set x-terminal-emulator /usr/bin/xfce4-terminal.wrapper

########################################################################################################################
# Python
# Everything about Python, an interpreted, interactive object-oriented language.
########################################################################################################################

# Download the installer
ARG CONDA_VERSION
ARG MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-${CONDA_VERSION}-Linux-x86_64.sh"
RUN wget --progress=dot:giga --output-document=miniconda.sh "${MINICONDA_URL}"

# Install conda
RUN rm --force --recursive /opt/conda && \
    mkdir --parents /opt && \
    sh miniconda.sh -b -p /opt/conda && \
    ln --symbolic /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh

# Clean up
RUN rm miniconda.sh

# Enable conda
RUN echo ". /opt/conda/etc/profile.d/conda.sh" >>"${HOME}/.zshrc"

########################################################################################################################

# Set the build arguments
ARG PROJECT_NAME
ARG PROJECT_PATH="/root/${PROJECT_NAME}"
ARG CONDA_BASE="/opt/conda"
ARG CONDA="${CONDA_BASE}/bin/conda"
ARG PYTHON_VERSION
ARG CONDA_ENV="${PROJECT_NAME}-${PYTHON_VERSION}"
ARG PIP="${CONDA_BASE}/envs/${CONDA_ENV}/bin/pip"

# Create a conda environment
RUN "${CONDA}" create --name "${CONDA_ENV}" python="${PYTHON_VERSION}"

# Install Flask - A Python micro framework for building web applications
RUN "${CONDA}" install --name "${CONDA_ENV}" --yes --channel anaconda flask=2.2.2

# Install Transformers - State-of-the-art Natural Language Processing for PyTorch and TensorFlow 2.0
RUN "${CONDA}" install --name "${CONDA_ENV}" --yes --channel huggingface transformers=4.26.1

# Install Pillow - Python Imaging Library (Fork)
RUN "${CONDA}" install --name "${CONDA_ENV}" --yes --channel anaconda pillow=9.4.0

# Install PyTorch - Tensors and Dynamic neural networks in Python with strong GPU acceleration
RUN "${CONDA}" install --name "${CONDA_ENV}" --yes --channel pytorch pytorch=2.0.0

# Install timm - PyTorch Image Models
RUN "${CONDA}" install --name "${CONDA_ENV}" --yes --channel conda-forge timm=0.6.12

# Install python-dotenv - Get and set values in your .env file in local and production servers
RUN "${CONDA}" install --name "${CONDA_ENV}" --yes --channel conda-forge python-dotenv=1.0.0

# Install pycocotools - COCO API for Python
RUN "${CONDA}" install --name "${CONDA_ENV}" --yes --channel conda-forge pycocotools=2.0.6

# Add the project to the container
ADD "${PROJECT_NAME}.tar.gz" "${PROJECT_PATH}"

# Add environment variables to shell configuration file
RUN echo "conda activate ${CONDA_ENV}" >>"${HOME}/.zshrc"
RUN echo "cd ${PROJECT_PATH}" >>"${HOME}/.zshrc"
RUN echo "export PYTHONPATH=\"${PYTHONPATH}:${PROJECT_PATH}\"" >>"${HOME}/.zshrc"
RUN echo "cat ~/.ssh/id_rsa.pub" >>"${HOME}/.zshrc"
RUN ssh-keygen -N "" -f "${HOME}/.ssh/id_rsa"

# Expose ports and add entrypoint script
EXPOSE 22
EXPOSE 80
EXPOSE 3389
ADD entrypoint.sh /entrypoint.sh
ENTRYPOINT ["zsh", "/entrypoint.sh"]
