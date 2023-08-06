# allow
Personal Website Safe and Block List Management Script

Requires `dnsmasq` installed and configured. To see how to setup:
- https://computingforgeeks.com/install-and-configure-dnsmasq-on-ubuntu-18-04-lts/
- https://www.linuxquestions.org/questions/linux-networking-3/how-to-block-all-websites-except-2-a-667350/


For dynamic control:
- sudo iptables -t nat -A OUTPUT -p tcp -d 1.1.1.1 -j DNAT --to-destination 127.0.0.1:7777
- sudo sysctl -w net.ipv4.conf.all.route_localnet=1
