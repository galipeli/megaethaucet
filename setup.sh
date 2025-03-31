#!/bin/bash

# Update package list dan instal Python 3, pip3, python3-venv jika belum terinstal
echo "Updating package list and installing Python3, pip3, python3-venv..."

# Instal Python 3, pip3, python3-venv, dan dependencies lain jika belum ada
sudo apt-get update -y
sudo apt-get install python3 python3-pip python3-venv -y

# Membuat virtual environment
echo "Creating Python virtual environment..."
python3 -m venv myenv

# Aktifkan virtual environment
source myenv/bin/activate

# Install pip dan modul yang dibutuhkan (seperti web3)
echo "Installing required Python modules..."
pip install --upgrade pip
pip install web3==6.20.1 requests

# Pastikan file Python ada dan jalankan
if [ -f "./megaethfaucet_sctg.py" ]; then
    echo "Running the Python script..."
    python3 megaethfaucet_sctg.py
else
    echo "Error: Script megaethfaucet_sctg.py not found."
fi

echo "Setup complete."
