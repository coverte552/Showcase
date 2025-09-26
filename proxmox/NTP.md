# NTP Server Change  

**Example IP:** `192.168.1.1`  

---

## DNS Lookup
```bash
cat /etc/resolv.conf
```

---

## Default Gateway Lookup
```bash
ip -c route
```

---

## Open Chrony Config
```bash
nano /etc/chrony/chrony.conf
```

---

## Host Local NTP
```bash
local stratum 10
```

---

## Offer NTP to Subnet
```bash
allow 192.168.1.0/24
```

---

## Accept Local NTP
```bash
192.168.1.1 iburst prefer
```

---

## Force NTP Sync
```bash
chronyc makestep
```

---

## Restart NTP
```bash
systemctl restart chronyd
```
