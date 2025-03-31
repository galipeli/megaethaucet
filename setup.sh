screen -S faucet-mega
python3 -m venv myenv
source myenv/bin/activate
sudo apt-get install python3.12-dev
pip install web3==6.20.1
python megaethfaucet_sctg.py
