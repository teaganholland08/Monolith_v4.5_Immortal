# 🔐 HOME ASSISTANT SECURITY HARDENING GUIDE

**Based on 2026 Best Practices**

---

## 🎯 SECURITY PRINCIPLES

### Defense in Depth

Multiple layers of security - no single point of failure.

### Privacy First

Local control, minimal cloud dependencies.

### Zero Trust

Verify everything, trust nothing by default.

---

## 1. AUTHENTICATION & ACCESS CONTROL

### Multi-Factor Authentication (MFA)

- [ ] Enable MFA for ALL user accounts
- [ ] Use authenticator app (Google Authenticator, Authy)
- [ ] Store backup codes in physical safe

### Strong Passwords

- [ ] Minimum 16 characters
- [ ] Use password manager (Bitwarden, 1Password)
- [ ] Unique password for Home Assistant
- [ ] Different password for each integration

### User Management

- [ ] Limit number of admin accounts
- [ ] Create read-only accounts for viewing only
- [ ] Remove unused accounts immediately
- [ ] Audit user permissions quarterly

### IP Banning

```yaml
# configuration.yaml
http:
  ip_ban_enabled: true
  login_attempts_threshold: 3
```

### Failed Login Notifications

```yaml
# automations.yaml
- alias: "Alert on Failed Login"
  trigger:
    platform: state
    entity_id: persistent_notification.http_login
  action:
    service: notify.mobile_app
    data:
      message: "Failed login attempt detected!"
```

---

## 2. NETWORK SECURITY

### NEVER Expose Directly to Internet

- ❌ DO NOT open ports 8123, 443, or 80 to public internet
- ✅ USE VPN for remote access

### HTTPS/SSL Encryption

**Option 1: Home Assistant Cloud (Easiest)**

- Managed SSL certificates
- Automatic renewal
- $6.50/month

**Option 2: DuckDNS + Let's Encrypt (Free)**

```yaml
# configuration.yaml
http:
  ssl_certificate: /ssl/fullchain.pem
  ssl_key: /ssl/privkey.pem
```

**Option 3: Local DNS + Self-Signed Cert**

- For local network only
- No external access

### VPN Remote Access (MOST SECURE)

**Recommended: WireGuard**

- Fastest VPN protocol
- Minimal attack surface
- Easy to configure

**Setup Steps:**

1. Install WireGuard on router or dedicated device
2. Configure client on phone/laptop
3. Access Home Assistant via local IP through VPN

### Network Segmentation (VLANs)

**Recommended Setup:**

- **VLAN 10:** Trusted devices (phones, laptops)
- **VLAN 20:** Smart home devices (IoT)
- **VLAN 30:** Guest network

**Firewall Rules:**

- VLAN 20 → VLAN 10: DENY (IoT can't access trusted)
- VLAN 10 → VLAN 20: ALLOW (Control IoT from trusted)
- VLAN 20 → Internet: ALLOW (IoT needs updates)

### IP Filtering

```yaml
# configuration.yaml
http:
  ip_ban_enabled: true
  trusted_proxies:
    - 192.168.1.0/24  # Local network only
```

---

## 3. ADD-ONS & INTEGRATIONS

### Minimize Third-Party Add-ons

- Only install what you NEED
- Prefer official add-ons over community
- Review permissions before installing

### Audit Add-on Permissions

- [ ] Check what data each add-on accesses
- [ ] Verify add-on doesn't phone home unnecessarily
- [ ] Remove add-ons that request excessive permissions

### HACS (Home Assistant Community Store)

**Use with caution:**

- Only install from well-known developers
- Check GitHub stars and recent updates
- Monitor for security advisories

### Secure `www` Folder

**WARNING:** Files in `/config/www/` are publicly accessible!

- ❌ DO NOT store sensitive data here
- ❌ DO NOT put API keys or passwords
- ✅ Only use for public images/icons

---

## 4. UPDATES & MAINTENANCE

### Keep Everything Updated

- [ ] Home Assistant Core (monthly)
- [ ] Home Assistant OS (monthly)
- [ ] All add-ons (weekly)
- [ ] Router firmware (quarterly)

### Automated Update Notifications

```yaml
# automations.yaml
- alias: "Notify on HA Update"
  trigger:
    platform: state
    entity_id: binary_sensor.updater
    to: 'on'
  action:
    service: notify.mobile_app
    data:
      message: "Home Assistant update available!"
```

---

## 5. BACKUP & RECOVERY

### Automated Backups

- [ ] Daily automated backups
- [ ] Store backups OFF the Home Assistant device
- [ ] Encrypt backups
- [ ] Test restore procedure quarterly

**Backup Locations:**

1. Local NAS (Synology, TrueNAS)
2. External USB drive (encrypted)
3. Cloud storage (encrypted) - Google Drive, Dropbox

### Backup Automation

```yaml
# automations.yaml
- alias: "Daily Backup"
  trigger:
    platform: time
    at: "03:00:00"
  action:
    service: hassio.backup_full
    data:
      name: "Automated Backup {{ now().strftime('%Y-%m-%d') }}"
```

---

## 6. MONITORING & ALERTS

### Security Monitoring

```yaml
# configuration.yaml
logger:
  default: warning
  logs:
    homeassistant.components.http.ban: warning
```

### Critical Alerts

- [ ] Failed login attempts
- [ ] Unexpected device connections
- [ ] Add-on crashes
- [ ] Disk space low
- [ ] Backup failures

---

## 7. PHYSICAL SECURITY

### Secure the Hardware

- [ ] Lock Home Assistant device in secure location
- [ ] Disable physical ports (USB, HDMI) if not needed
- [ ] Use encrypted storage (LUKS)

### Backup Power

- [ ] UPS (Uninterruptible Power Supply)
- [ ] Graceful shutdown on power loss

---

## 8. ADVANCED HARDENING

### Cloudflare Tunnel (Optional)

**Pros:**

- DDoS protection
- Bot filtering
- No port forwarding needed

**Cons:**

- Requires Cloudflare account
- Adds external dependency

### Fail2Ban Integration

Automatically ban IPs after failed attempts:

```yaml
# Add-on: Fail2Ban
```

### Security Headers

```yaml
# configuration.yaml
http:
  cors_allowed_origins:
    - https://your-domain.com
  use_x_forwarded_for: true
  trusted_proxies:
    - 192.168.1.0/24
```

---

## 9. PRIVACY CONSIDERATIONS

### Minimize Data Collection

- Only enable sensors you need
- Disable history for sensitive entities
- Use local processing (no cloud)

### Disable Unnecessary Integrations

```yaml
# configuration.yaml
default_config:  # Remove this
# Instead, manually enable only what you need:
automation:
frontend:
config:
```

---

## 10. SECURITY CHECKLIST

### Initial Setup

- [ ] Change default passwords
- [ ] Enable MFA
- [ ] Configure HTTPS/SSL
- [ ] Set up VPN
- [ ] Create VLANs for IoT devices
- [ ] Enable IP banning
- [ ] Configure automated backups

### Monthly

- [ ] Review user accounts
- [ ] Check for updates
- [ ] Audit add-on permissions
- [ ] Review failed login attempts
- [ ] Test backup restore

### Quarterly

- [ ] Full security audit
- [ ] Update router firmware
- [ ] Rotate passwords
- [ ] Review firewall rules
- [ ] Test emergency procedures

---

## 🚨 INCIDENT RESPONSE

### If Compromised

1. **Immediate Actions:**
   - Disconnect from internet
   - Change all passwords
   - Review logs for unauthorized access
   - Restore from clean backup

2. **Investigation:**
   - Check which integrations were accessed
   - Review automation history
   - Identify entry point

3. **Recovery:**
   - Fresh install if necessary
   - Re-enable integrations one by one
   - Monitor for 30 days

---

## 📚 RESOURCES

### Official Documentation

- Home Assistant Security: <https://www.home-assistant.io/docs/configuration/securing/>
- Authentication Providers: <https://www.home-assistant.io/docs/authentication/>

### Community Resources

- Home Assistant Community Forum
- r/homeassistant on Reddit
- Home Assistant Discord

---

**SYSTEM:** Project Monolith Omega  
**GUIDE:** Home Assistant Security Hardening  
**UPDATED:** February 3, 2026  
**STATUS:** PRODUCTION READY
