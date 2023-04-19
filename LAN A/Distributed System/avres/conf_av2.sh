chmod +x compileRpc.sh
chmod +x removeRpc.sh
./removeRpc.sh
sudo apt update
sudo apt install python3-pip
pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt
sudo apt-get update
sudo apt-get install chkrootkit
./compileRpc.sh
export ARG1="10.123.0.3"
export ARG2="chkrootkit"
python3 ./av/av.py $ARG1 $ARG2
