Questa cartella (pki) è il risultato della generazione di chiavi e certificati (in modo da evitare di ripeterla più volte).
Password client: client-pwd
Password server: server-pwd
Password CA: nsd-pwd

SERVER:
1) copiare l'intera cartella pki nella root con: cp -r ... /root/
2) scrivere dentro /root/pki/ i file per la configurazione di OPENVPN
3) lanciare da /root/pki/ OPENVPN (dopo averlo scaricato)

CLIENT:
1) copiare in /root/ i file: client.key (da /pki/private); client.crt (da /pki/issued); ca.crt (da /pki)
2) scrivere in /root/ i file di configurazione di OPENVPN
3) lanciare da /root/ OPENVPN (dopo averlo scaricato)


I PASSAGGI SALTATI SONO ------------------------------------------------------------------------------------------------------
sudo apt update
sudo apt install openvpn easy-rsa
cd /usr/share/easy-rsa

./easyrsa init-pki
./easyrsa build-ca
./easyrsa build-server-full server
./easyrsa build-client-full client
./easyrsa gen-dh