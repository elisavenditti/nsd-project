chmod +x compileRpc.sh
chmod +x removeRpc.sh
./removeRpc.sh
sudo apt update
sudo apt install python3-pip
pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt
./compileRpc.sh
export FLASK_APP=./centralnode/centralnode.py
python3 -m flask run --host 10.23.1.2
