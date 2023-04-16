chmod +x compileRpc.sh
chmod +x removeRpc.sh

./removeRpc.sh

sudo apt update

sudo apt install python3-pip

pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Installazione antivirus
sudo apt-get update
sudo apt-get install clamav
sudo apt-get install mlocate
sudo updatedb

# sudo systemctl stop clamav-freshclam.service
# sudo freshclam
# sudo systemctl start clamav-freshclam.service

./compileRpc.sh

python3 ./av/av.py
