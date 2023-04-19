chmod +x compileRpc.sh
chmod +x removeRpc.sh
./removeRpc.sh
sudo apt update
sudo apt install python3-pip
pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt
cd /home/lubuntu/Scaricati
wget http://downloads.sourceforge.net/project/rkhunter/rkhunter/1.4.6/rkhunter-1.4.6.tar.gz
tar -xvf rkhunter-1.4.6.tar.gz
cd rkhunter-1.4.6
sudo ./installer.sh --install
cd /home/lubuntu/Desktop/LAN\ A/Distributed\ System/avres
./compileRpc.sh
export ARG1="10.123.0.4"
export ARG2="rkhunter"
python3 ./av/av.py $ARG1 $ARG2
