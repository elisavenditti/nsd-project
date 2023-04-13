export LAN=enp0s8
export EXT=enp0s3

iptables -F
iptables -P FORWARD DROP
iptables -P INPUT DROP
iptables -P OUTPUT DROP

# accetto le connessioni tra "end host": CENTRAL NODE >> AV#
iptables -A FORWARD -i $EXT -o $LAN -s 10.23.1.2 -d 10.123.0.0/16 -j ACCEPT
# accetto le connessioni tra "end host": AV# >> CENTRAL NODE
iptables -A FORWARD -i $LAN -o $EXT -s 10.123.0.0/16 -d 10.23.1.2 -j ACCEPT

# accetto le connessioni tra gli spoke
iptables -A FORWARD -i $EXT -o $EXT -s 10.23.0.0/24 -d 10.23.1.0/24 -j ACCEPT
iptables -A FORWARD -i $EXT -o $EXT -s 10.23.1.0/24 -d 10.23.0.0/24 -j ACCEPT
