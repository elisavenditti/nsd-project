apt update
apt install openvpn
ip a a 192.168.16.2/24 dev enp0s3
ip r a default via 192.168.16.1