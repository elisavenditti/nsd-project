sudo ip a a 10.0.37.2/30 dev enp0s3
sudo ip a a 10.123.0.1/16 dev enp0s8
sudo ip r a default via 10.0.37.1
sudo -s
echo 1 > /proc/sys/net/ipv4/ip_forward
