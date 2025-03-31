#!/bin/bash

# Pastikan menjalankan skrip ini dengan hak akses root
if [ "$(id -u)" -ne 0 ]; then
  echo "Harap jalankan skrip ini sebagai root (sudo)."
  exit 1
fi

# Update dan upgrade paket-paket yang ada
echo "Memperbarui dan meng-upgrade sistem..."
apt-get update -y && apt-get upgrade -y

# Instal Python 3 dan pip jika belum ada
echo "Memastikan Python 3 dan pip sudah terinstal..."
apt-get install -y python3 python3-pip python3-venv

# Instal dependensi lainnya (misalnya web3)
echo "Menginstal dependensi..."
pip3 install --upgrade pip
pip3 install web3==6.20.1

# Buat dan aktifkan virtual environment
echo "Membuat environment virtual Python..."
python3 -m venv myenv
source myenv/bin/activate

# Menginstal kembali dependensi dalam environment virtual
echo "Menginstal dependensi dalam virtual environment..."
pip install -r requirements.txt

# Beri izin eksekusi pada file skrip Python
echo "Memberi izin eksekusi pada skrip Python..."
chmod +x megaethfaucet_sctg.py

# Jalankan skrip Python
echo "Menjalankan skrip Python..."
python megaethfaucet_sctg.py
