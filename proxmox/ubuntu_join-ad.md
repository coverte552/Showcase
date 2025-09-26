# Ubuntu 24.04 to Windows Server 2025 AD Join (Unsecured Method)

## 1. Background & Problem
Windows Server 2025 introduced a Kerberos protocol regression that breaks Linux domain joins. When using `realm join` or `adcli`, the process fails at the password setting stage due to a malformed Kerberos response from the domain controller.

This document was made in conjunction with ChatGPT 4o.  
OpenAI. (2025). *ChatGPT (May 2025 version) [Large language model]*. https://chat.openai.com/

⚠️ **Warning:** This process will expose plaintext traffic on your network and should only be followed in a **lab environment**.  
This is a workaround for academic purposes, not a production solution.

---

## 2. Network Requirements
Ensure the following:
- DNS points to the AD domain controller (e.g., `172.16.42.12`)
- Time is synchronized and in the same timezone (e.g., `America/New_York`)
- Hostname is properly set (e.g., `tripp-lite`)
- The domain controller is reachable (`ping` or DNS resolution)

---

## 3. Install Required Packages
Run the following command:

```bash
sudo apt update && sudo apt install -y sssd realmd adcli oddjob oddjob-mkhomedir samba-common-bin packagekit
```

---

## 4. Configure SSSD
Create the config file at `/etc/sssd/sssd.conf` with the following content:

```ini
[sssd]
domains = BIGDATA.NET
config_file_version = 2
services = nss, pam

[domain/BIGDATA.NET]
id_provider = ad
ad_domain = BIGDATA.NET
krb5_realm = BIGDATA.NET
realmd_tags = manages-system joined-with-adcli
fallback_homedir = /home/%u@%d
default_shell = /bin/bash
ad_machine_account_password_renewal = false
```

Set permissions:

```bash
sudo chmod 600 /etc/sssd/sssd.conf
```

---

## 5. Join the Domain (Unsecured)
Run this command to join using plaintext LDAP:

```bash
sudo adcli join --verbose --domain=BIGDATA.net --login-user=Administrator --ldap-passwd
```

---

## 6. Keytab Confirmation
You should see confirmation that the keytab was created successfully.

---

## 7. Restart and Enable SSSD
Run the following:

```bash
sudo systemctl restart sssd && sudo systemctl enable sssd
```

---

## 8. Verify Join
Check for Kerberos ticket:

```bash
klist
```

Test domain user lookup:

```bash
id ecovert@BIGDATA.NET
```

---

## 9. Security Notes
- The join step used **unencrypted LDAP (plaintext password)**.  
- All authentication from this point on uses **encrypted Kerberos**.

---

## 10. Final Recommendation
- Set up **LDAPS** on your domain controller.  
- Rejoin using **Kerberos or LDAPS** in the future.  
- Monitor machine account password manually since rotation is disabled.
