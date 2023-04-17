export LAN=macsec0
export EXT=enp0s3

iptables -F

iptables -P FORWARD DROP
iptables -A FORWARD -m state --state ESTABLISHED -j ACCEPT
iptables -A FORWARD -i $LAN -o $EXT -j ACCEPT
iptables -A POSTROUTING -t nat -o $EXT -j SNAT --to-source 10.23.0.1

iptables -P INPUT DROP
iptables -A INPUT -i $LAN -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -i $LAN -p icmp -j ACCEPT

iptables -P OUTPUT ACCEPT
iptables -A INPUT -m state --state ESTABLISHED -j ACCEPT

iptables -A PREROUTING -t nat -i $EXT -p tcp --dport 80 -m statistic --mode nth --every 2 --packet 0 -j DNAT --to-destination 10.23.0.2:80
iptables -A PREROUTING -t nat -i $EXT -p tcp --dport 80 -m statistic --mode nth --every 2 --packet 0 -j DNAT --to-destination 10.23.0.3:80
iptables -A FORWARD -i $EXT -o $LAN -p tcp --dport 80 -j ACCEPT

