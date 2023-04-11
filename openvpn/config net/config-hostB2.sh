sudo apt-get update
sudo apt install -y openvpn
sudo ip a a 192.168.16.2/24 dev enp0s3
sudo ip r a default via 192.168.16.1
