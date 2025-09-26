# NTP Server Change
Example IP = 192.168.1.1
Dns lookup
  cat /etc/resolv.conf
Default gateway lookup:
	ip -c route
Open chrony config
	nano /etc/chrony/chrony.conf
Host local NTP
	local stratum 10 
Offer NTP to subnet
	allow 192.168.1.0/24
Accept local NTP
	192.168.1.1 iburst prefer
Force NTP sync
  chronyc makestep
Restart NTP:
  systemctl restart chronyd
