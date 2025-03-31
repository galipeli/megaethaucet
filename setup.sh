#!/bin/bash

# Update package list
echo "Updating package list..."
sudo apt-get update -y

# Install Python 3 dan pip3 jika belum terinstal
echo "Checking if Python 3 and pip3 are installed..."

# Install Python 3
if ! command -v python3 &> /dev/null
then
    echo "Python3 not found, installing..."
    sudo apt-get install python3 python3-dev python3-venv -y
else
    echo "Python 3 is already installed."
fi

# Install pip3
if ! command -v pip3 &> /dev/null
then
    echo "pip3 not found, installing..."
    sudo apt-get install python3-pip -y
else
    echo "pip3 is already installed."
fi

# Buat virtual environment
echo "Setting up Python virtual environment..."
python3 -m venv myenv

# Aktifkan virtual environment
source myenv/bin/activate

# Install modul yang dibutuhkan (seperti web3)
echo "Installing required Python modules..."
pip install --upgrade pip
pip install web3==6.20.1 requests

# Pastikan skrip Python ada dan bisa dijalankan
if [ -f "./megaethfaucet_sctg.py" ]; then
    echo "Running the Python script..."
    python3 megaethfaucet_sctg.py
else
    echo "Error: Script megaethfaucet_sctg.py not found."
fi

echo "Setup complete."
