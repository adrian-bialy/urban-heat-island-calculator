#!/bin/bash
set -e

# Update package lists and install build-essential if needed
sudo apt update
sudo apt install -y build-essential

# Install Miniconda
MINICONDA_INSTALLER="Miniconda3-latest-Linux-x86_64.sh"
MINICONDA_URL="https://repo.anaconda.com/miniconda/$MINICONDA_INSTALLER"
INSTALL_DIR="$HOME/miniconda3"

if [ -d "$INSTALL_DIR" ]; then
    echo "Updating existing Miniconda installation..."
    wget -q $MINICONDA_URL
    bash $MINICONDA_INSTALLER -b -u -p $INSTALL_DIR
    rm $MINICONDA_INSTALLER
else
    echo "Installing Miniconda..."
    wget -q $MINICONDA_URL
    bash $MINICONDA_INSTALLER -b -p $INSTALL_DIR
    rm $MINICONDA_INSTALLER
fi

# Initialize Conda for Bash shell
$INSTALL_DIR/bin/conda init bash