# MONOLITH v4.5 IMMORTAL - SETUP GUIDE

**Target:** Non-Technical User  
**Time Required:** 2-3 hours  
**Status:** Complete Implementation

---

## QUICK START (15 Minutes)

### 1. Secure Your System FIRST

```cmd
Right-click System/Security/windows_debloat.bat
Select "Run as Administrator"
Restart computer when done
```

### 2. Install VPN (CRITICAL)

- **Recommended:** [Surfshark](https://surfshark.com) ($2.19/month)
- **Alternative:** [Mullvad](https://mullvad.net) ($5/month, accepts crypto)
- **Free (Temporary):** ProtonVPN free tier

**Enable Kill Switch in VPN settings!**

### 3. Launch Monolith

```cmd
cd C:\Users\Teagan Holland\Desktop\Monolith_v4.5_Immortal
python monolith_omega.py
```

**You're now running at LEVEL 1 security.**

---

## REVENUE BRIDGES (Make Real Money)

### Bridge 1: Gumroad (Fastest to $$$)

**Time:** 10 minutes  
**Payout:** 2-5 days to bank  
**Fee:** 10%

1. Create account: <https://gumroad.com>
2. Go to: Settings > Advanced > Create Application
3. Copy "Access Token"
4. Open Command Prompt (as Administrator):

```cmd
setx GUMROAD_ACCESS_TOKEN "paste_token_here"
```

5. Restart terminal
2. Test:

```cmd
python System/Revenue/gumroad_bridge.py
```

**How It Works:**

- Genesis creates Python script → Auto-uploads to Gumroad → Listed at $9.99-$14.99
- Sales deposit to YOUR bank account (you provide routing info in Gumroad settings)

### Bridge 2: Medium Partner Program (Passive Income)

**Time:** 30 minutes  
**Payout:** Monthly via Stripe (minimum $10)  
**Fee:** 0% (Medium takes cut from subscription, not you)

1. Create account: <https://medium.com>
2. Apply: <https://medium.com/creators> (need 100 followers first - write 3 articles)
3. Once approved, go to: Settings > Security > Integration tokens
4. Create token, then:

```cmd
setx MEDIUM_INTEGRATION_TOKEN "paste_token_here"
```

5. Test:

```cmd
python System/Revenue/medium_bridge.py
```

**How It Works:**

- Genesis creates article → Auto-publishes to Medium → Earns per read
- 1 viral article (10k reads) = $500-2,000

### Bridge 3: Crypto Trading (Advanced)

**Status:** API integration pending  
**Risk:** Medium-High (can lose money)  
**Setup:** Requires Coinbase Pro account + KYC verification

*This will be added in future update.*

---

## INTELLIGENCE LAYER (Find Opportunities)

### Enable News Scanning

1. Get free API key: <https://newsapi.org/register>
2. Set environment variable:

```cmd
setx NEWSAPI_KEY "your_key_here"
```

### Enable Legal Intelligence

1. Get API key: <https://api.congress.gov/sign-up>
2. Set environment variable:

```cmd
setx CONGRESS_API_KEY "your_key_here"
```

**Now the system will:**

- Scan news 24/7 for money-making signals
- Detect tax law changes
- Alert you to opportunities

---

## SECURITY HARDENING

### LEVEL 2 (GHOST) - Recommended

**What You Have:**

- ✅ Windows debloat (telemetry off)
- ✅ VPN (network anonymity)
- ✅ Kill switch (`KILL_SWITCH.bat`)

**What to Add:**

1. **Burner Payment Card**
   - Sign up: <https://privacy.com>
   - Create virtual card for Gumroad/Medium
   - Protects real bank account

2. **Anonymous Email**
   - ProtonMail: <https://proton.me/mail>
   - Use for all Monolith-related signups

3. **Encrypted Backups**
   - Buy USB drive (32GB minimum)
   - Enable BitLocker: Right-click drive > Turn on BitLocker
   - Backup `System/Logs/ledger.db` and `Brain/Vault` weekly

### LEVEL 3 (MONOLITH) - Maximum Stealth

**Hardware Upgrades:**

- [ ] Google Pixel 7 ($200 used) + GrapheneOS ($0)
- [ ] Raspberry Pi 4 ($50) for Home Assistant
- [ ] M-DISC burner ($80) for permanent archival

**Software Upgrades:**

- [ ] Switch to Linux Mint (keep Windows for development)
- [ ] Tails OS for sensitive research (boots from USB)

**Full guide:** `System/Security/SECURITY_PROTOCOL.md`

---

## HOME ASSISTANT INTEGRATION

### Local-Only Smart Home (No Cloud)

**Hardware Needed:**

- Raspberry Pi 4 (4GB RAM) - $55
- MicroSD card (32GB) - $10
- Power supply - $8

**Installation:**

1. Download: <https://www.home-assistant.io/installation/raspberrypi>
2. Flash to MicroSD using Raspberry Pi Imager
3. Insert into Pi, connect to network, power on
4. Visit: <http://homeassistant.local:8123>
5. Create account (stays LOCAL, never goes to cloud)

**Connect to Monolith:**

1. In Home Assistant: Settings > Add-ons > Install "Terminal & SSH"
2. Generate Long-Lived Access Token
3. Set in Monolith:

```cmd
setx HOMEASSISTANT_TOKEN "your_token_here"
setx HOMEASSISTANT_URL "http://homeassistant.local:8123"
```

**Now voice control works:**

- "Lock the house" → All doors lock
- "Lockdown mode" → Lights off, cameras recording, doors locked

---

## TROUBLESHOOTING

### "pip is not recognized"

**Fix:**

```cmd
python -m pip install requests tenacity yfinance cryptography
```

### VPN Not Detected

**Check:**

```cmd
python System/Security/opsec_hardening.py
```

If status shows "EXPOSED", start VPN before Monolith.

### Gumroad API Error

- Verify token is correct (no extra spaces)
- Check internet connection
- Ensure VPN allows API access (some block it)

### No Intelligence Signals

- Verify NEWSAPI_KEY is set: `echo %NEWSAPI_KEY%`
- Free tier has rate limits (100 requests/day)
- Upgrade to paid if needed ($449/month for unlimited)

---

## UPGRADE PATH

### Month 1: Basic Operation

- [x] VPN active
- [x] Windows debloated
- [ ] Gumroad publishing (1 product)
- [ ] Medium account created

**Expected Revenue:** $50-$250

### Month 2: Intelligence Layer

- [ ] NewsAPI configured
- [ ] First automated opportunity detected
- [ ] 5+ products on Gumroad
- [ ] Medium Partner Program approved

**Expected Revenue:** $250-$750

### Month 3: Full Automation

- [ ] All revenue bridges active
- [ ] Auto-publishing working
- [ ] Tax optimizer running
- [ ] Privacy.com card integrated

**Expected Revenue:** $750-$2,000

### Month 6: Hardware Upgrades

- [ ] Pixel + GrapheneOS
- [ ] Home Assistant running
- [ ] M-DISC backups
- [ ] Consider Linux switch

**Expected Revenue:** $2,000-$5,000

---

## SUPPORT RESOURCES

### Documentation

- [IMMORTAL_MANUAL.md](../IMMORTAL_MANUAL.md) - Full system guide
- [SECURITY_PROTOCOL.md](../System/Security/SECURITY_PROTOCOL.md) - Hardening guide
- [REAL_MONEY_PROTOCOL.md](../REAL_MONEY_PROTOCOL.md) - Revenue strategies

### External Resources

- **Privacy:** <https://www.privacytools.io>
- **GrapheneOS:** <https://grapheneos.org>
- **Home Assistant:** <https://www.home-assistant.io/docs>
- **OSINT:** <https://osintframework.com>

### Emergency Contacts

- **Kill Switch:** Double-click `KILL_SWITCH.bat`
- **System Reset:** Reinstall from GitHub (backup ledger.db first)

---

## LEGAL DISCLAIMER

This system is designed for **legal** tax optimization, content creation, and automation. You are responsible for:

- Reporting all income to tax authorities
- Complying with API terms of service
- Following local laws and regulations

Using this system for tax evasion, fraud, or illegal activities is **YOUR responsibility**, not the system's.

**Consult a tax professional and attorney before implementing any strategies.**

---

## NEXT STEPS

1. ✅ Run Windows debloat script
2. ✅ Install and configure VPN
3. ✅ Set up Gumroad API
4. ⬜ Generate first product with Genesis
5. ⬜ Verify product appears on Gumroad
6. ⬜ Set up Medium account
7. ⬜ Enable Intelligence Layer (NewsAPI)
8. ⬜ Weekly: Check ledger.db for revenue
9. ⬜ Monthly: Backup vault to encrypted USB
10. ⬜ When ready: Upgrade to Pixel + GrapheneOS

**Welcome to Project Monolith. You are now autonomous.**
