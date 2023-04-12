apt update
apt install openvpn
ip a a 2.0.0.1/30 dev enp0s3
ip a a 192.168.17.1/24 dev enp0s8
ip r a default via 2.0.0.2

iptables -t nat -A POSTROUTING -o enp0s3 -j MASQUERADE
echo 1 > /proc/sys/net/ipv4/ip_forward