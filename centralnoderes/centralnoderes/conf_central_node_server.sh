chmod +x compileRpc.sh
chmod +x removeRpc.sh

./removeRpc.sh

sudo apt update

# installazione PIP
sudo apt install python3-pip

# Installazione delle librerie richieste per l'esecuzione
pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# A questo punto, ho a disposizione Python, PIP, Flask e GRPC

# Produco i proto file
./compileRpc.sh

# Setto la variabile d'ambiente per indicare l'applicazione
export FLASK_APP=./centralnode/centralnode.py

# Avvio Flask
python3 -m flask run --host 192.168.0.2
