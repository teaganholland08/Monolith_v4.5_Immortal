# 🛠️ PROJECT MONOLITH: MANDATORY HARDWARE MANIFEST

## Complete Device Procurement Guide for Total Sovereignty

**Date:** February 3, 2026  
**Status:** READY FOR PROCUREMENT

---

## 🎯 PROCUREMENT PHILOSOPHY

**Core Principle:** Every device must integrate into the Monolith ecosystem. No cloud dependencies. Local control mandatory.

**Standards:**

- Local API access (no cloud-only devices)
- Open protocols (Matter, Zigbee, Z-Wave)
- NFC support (for YubiKey authentication)
- Offline capability (must work without internet)

---

## 🧠 TIER 1: THE BRAIN (MANDATORY)

### Local AI Workstation

**Purpose:** Run Llama-3 (70B), SDXL, and all Hydra agents locally without cloud dependency.

**Specifications:**

- **GPU:** Dual NVIDIA RTX 5090 (48GB VRAM) - *Training/Rendering*
- **NPU:** Axelera Metis or Hailo-8 AI Accelerator - *Local Inference (Low Wattage)*
- **CPU:** AMD Threadripper 9000 Series (64-Core)

- Model: AMD Threadripper 7980X
- Cores: 64 cores / 128 threads
- Purpose: Multi-threaded CrewAI orchestration
- Cost: ~$5,000

**GPU:** 2x NVIDIA RTX 4090 (24GB VRAM each)

- Total VRAM: 48GB
- Connection: NVLink bridge
- Purpose: Local Llama-3 70B + SDXL inference
- Cost: ~$3,200 × 2 = $6,400

**RAM:** 256GB DDR5

- Speed: DDR5-5600 or higher
- Configuration: 8x 32GB modules
- Purpose: Large vector databases (ChromaDB)
- Cost: ~$800

**Storage:**

- **Primary:** 4TB NVMe Gen5 (OS + Active Agents)
  - Model: Samsung 990 Pro or WD Black SN850X
  - Cost: ~$400
- **Archive:** 20TB Enterprise HDD (Offline Ark)
  - Model: Seagate Exos X20
  - Cost: ~$400

**Motherboard:** TRX50 chipset

- Model: ASUS Pro WS TRX50-SAGE WIFI
- Features: Dual 10GbE, PCIe 5.0
- Cost: ~$1,000

**Power Supply:** 2000W 80+ Platinum

- Model: Corsair AX2000 or EVGA SuperNOVA 2000
- Purpose: Dual RTX 4090s require massive power
- Cost: ~$500

**Cooling:** Custom liquid cooling

- CPU: 360mm AIO (Arctic Liquid Freezer II)
- GPU: Stock coolers sufficient
- Cost: ~$200

**Case:** Full tower with excellent airflow

- Model: Fractal Design Define 7 XL
- Cost: ~$200

**Operating System:** Linux Mint 21.3 (Virginia)

- Free, privacy-focused
- Native Docker/Python support
- Cost: $0

**Total Workstation Cost:** ~$14,500

---

## 🛡️ TIER 2: SECURITY & NETWORKING (MANDATORY)

### Network Security Hardware

**Router/Firewall:** Protectli Vault FW6E

- CPU: Intel i5-8365UE (4 cores)
- RAM: 16GB
- Storage: 256GB mSATA SSD
- OS: OPNsense (free)
- Features: Hardware VPN, IDS/IPS, network ghosting
- Cost: ~$700

**VPN Service:** Mullvad VPN

- Privacy-focused (no logs)
- Accepts Bitcoin
- Cost: $5/month = $60/year

**dVPN (Decentralized):** Mysterium Network

- Multi-hop routing
- No centralized logging
- Cost: Pay-per-use (~$10/month)

**Hardware Security Keys:** 2x YubiKey 5C NFC

- Primary: Daily driver
- Backup: Stored in fireproof safe
- Purpose: Treasury, LLC accounts, crypto wallets
- Cost: $55 × 2 = $110

**Satellite Internet:** Starlink High Performance

- Dish: Flat High Performance
- Speed: 150-500 Mbps
- Latency: 25-50ms
- Purpose: Guaranteed connectivity in Powell River
- Cost: $2,500 (hardware) + $500/month

---

## 🏠 TIER 3: IoT & SMART HOME (MANDATORY)

### Universal Control Hub

#### Home Assistant Yellow

- Purpose: Local control of all smart devices
- Protocols: Zigbee, Z-Wave, Matter, Thread
- No cloud required
- Cost: ~$200

#### Samsung SmartThings Station

- Purpose: Native Samsung device integration
- Works with: Samsung appliances, TVs, phones
- Cost: ~$60

**Power Monitoring:** Sense Home Energy Monitor

- Purpose: Real-time solar/battery data
- Integration: Feeds into Omega Dashboard
- Cost: ~$300

**Smart Devices (Recommended):**

**Lighting:** Philips Hue (Zigbee)

- Bulbs: $15-50 each
- Bridge: Included with starter kit
- Total: ~$300 for 10 bulbs

**Locks:** Schlage Encode Plus (Matter)

- Cost: ~$300 per lock

**Thermostat:** Ecobee SmartThermostat (HomeKit/Matter)

- Cost: ~$250

**Cameras:** Frigate-compatible IP cameras

- Model: Reolink RLC-810A (4K)
- Cost: ~$100 each × 6 = $600

**Sensors:** Aqara Door/Window Sensors (Zigbee)

- Cost: ~$15 each × 10 = $150

---

## 🔋 TIER 4: OFF-GRID POWER (MANDATORY)

### Energy Independence Stack

**Battery Storage:** EG4-LL 48V 100Ah Lithium

- Quantity: 20 batteries (100kWh total)
- Configuration: Rack-mounted
- Cost: ~$1,200 × 20 = $24,000

**Inverter:** Victron Quattro 15kVA

- Model: Quattro 48/15000/200-100/100
- Features: Grid-tie, backup switching
- Cost: ~$5,000

**Solar Panels:** Bifacial 400W panels

- Quantity: 50 panels (20kW system)
- Model: Canadian Solar BiHiKu7
- Cost: ~$200 × 50 = $10,000

**Charge Controller:** Victron SmartSolar MPPT 250/100

- Quantity: 4 units
- Cost: ~$800 × 4 = $3,200

**Portable Power:** EcoFlow Delta Pro

- Capacity: 3.6kWh (expandable to 25kWh)
- Purpose: Go-bag power, vehicle charging
- Cost: ~$3,700

**Portable Solar:** 400W Foldable Solar Panels

- Quantity: 2 panels
- Purpose: Portable charging
- Cost: ~$500 × 2 = $1,000

**Total Off-Grid Power Cost:** ~$47,900

---

## 📱 TIER 5: MOBILE COMMAND (MANDATORY)

### Your Phone as Remote Portal

**Primary Device:** Samsung Galaxy S24 Ultra or Z Fold 5

- Features: DeX, NFC, 5G
- Purpose: Remote God Mode portal
- Cost: ~$1,200

**Required Apps:**

**Termux** (Free)

- Linux terminal on Android
- SSH into main AI server
- Run Python scripts remotely

**Home Assistant Mobile App** (Free)

- Control all smart devices
- Monitor system status

**Tailscale** (Free)

- Secure mesh network
- Access Omega Dashboard from anywhere

**Samsung DeX** (Built-in)

- Turn any monitor into command center
- Plug phone into TV/monitor

**Accessories:**

**DeX Cable/Dock:** USB-C to HDMI

- Cost: ~$50

**Bluetooth Headphones:** Samsung Galaxy Buds Pro

- Purpose: Voice commands to Alfred
- Cost: ~$200

**Thunderbolt 4 Dock:** CalDigit TS4

- Purpose: Switch between workstation and mobile
- Cost: ~$400

---

## 🏥 TIER 6: BIOMETRIC MONITORING (MANDATORY)

### Body Battery Integration

**Wearable:** WHOOP 4.0 or Oura Ring Gen 3

- Metrics: HRV, sleep, recovery, body battery
- Integration: Feeds into Predictive Concierge
- Cost:
  - WHOOP: $0 hardware + $30/month membership
  - Oura: $300 + $6/month membership

**Blood Glucose Monitor:** Dexcom G7 (optional)

- Purpose: Real-time metabolic data
- Cost: ~$200 + $300/month supplies

---

## 🗄️ TIER 7: DATA STORAGE (MANDATORY)

### The Offline Ark

**NAS:** Synology DS923+ (4-bay)

- Purpose: Culture Ark (10,000+ movies, music, books)
- Cost: ~$600

**Hard Drives:** 4x 8TB WD Red Plus

- Total: 24TB usable (RAID 5)
- Cost: ~$200 × 4 = $800

**Backup Drives:** 2x 8TB External USB

- Purpose: Offline backups
- Cost: ~$150 × 2 = $300

**Total Storage Cost:** ~$1,700

---

## 🚗 TIER 8: VEHICLE INTEGRATION (OPTIONAL)

### EV Optimization

**Tesla Model 3/Y** or **Rivian R1T**

- Features: API access for charging automation
- Integration: Alfred charges during solar excess
- Cost: $40,000-80,000

**Alternative:** Any EV with open API

- Check: OpenVehicles.com for compatibility

---

## 💰 COMPLETE PROCUREMENT BUDGET

### Mandatory Components

| Category | Cost |
| -------- | ---- |
| AI Workstation | $14,500 |
| Security & Networking | $3,370 |
| IoT & Smart Home | $1,860 |
| Off-Grid Power | $47,900 |
| Mobile Command | $1,850 |
| Biometric Monitoring | $300 + $6/mo |
| Data Storage | $1,700 |
| **TOTAL (One-Time)** | **$71,480** |
| **TOTAL (Monthly)** | **$516** |

### Optional Components

| Category | Cost |
| -------- | ---- |
| Electric Vehicle | $40,000-80,000 |
| Trading Post Structure | $5,000 |
| Medical Equipment | $2,000 |
| Tools & Workshop | $5,000 |

---

## 🛒 PROCUREMENT PRIORITY

### Phase 1: Core Intelligence (Week 1)

- [ ] AI Workstation components
- [ ] YubiKeys (2x)
- [ ] Protectli Vault router
- [ ] Home Assistant Yellow
- [ ] Samsung phone (if needed)

**Cost:** ~$17,000

### Phase 2: Power Independence (Month 1)

- [ ] Battery storage (EG4-LL)
- [ ] Inverter (Victron Quattro)
- [ ] Solar panels
- [ ] Charge controllers
- [ ] **Starlink Mini 3 Plus** (Portable SAT-COM backup)
- [ ] **XREAL 1S** (AR Command Interface - Lightweight Edition)
- [ ] **Abbott Lingo CGM** (Metabolic Monitoring)

**Cost:** ~$47,900

### Phase 3: Complete Ecosystem (Month 2)

- [ ] Smart home devices
- [ ] Biometric wearable
- [ ] NAS + storage drives
- [ ] Portable power
- [ ] Starlink

**Cost:** ~$6,580

---

## 🔧 SETUP SEQUENCE

### Step 1: Build AI Workstation

1. Assemble hardware
2. Install Linux Mint
3. Install Docker, Python, CUDA drivers
4. Test Llama-3 inference
5. Deploy Hydra agents

### Step 2: Configure Network Security

1. Install OPNsense on Protectli Vault
2. Configure Mullvad VPN
3. Set up MAC rotation scripts
4. Enable IDS/IPS

### Step 3: Deploy Smart Home

1. Set up Home Assistant Yellow
2. Pair all Zigbee/Z-Wave devices
3. Configure automations
4. Test voice commands

### Step 4: Mobile Integration

1. Install Tailscale on workstation + phone
2. Configure SSH access via Termux
3. Test remote dashboard access
4. Set up DeX for external displays

### Step 5: Power Systems

1. Install battery rack
2. Wire inverter
3. Mount solar panels
4. Configure charge controllers
5. Test grid-tie and backup modes

---

## 📋 DEVICE COMPATIBILITY CHECKLIST

### When Buying New Devices

**✅ MUST HAVE:**

- Local API access (no cloud-only)
- Open protocol (Matter, Zigbee, Z-Wave, or documented API)
- Offline operation capability
- Privacy-focused (no mandatory telemetry)

**❌ AVOID:**

- Cloud-only devices (Ring, Nest without local access)
- Proprietary protocols (closed ecosystems)
- Subscription-required features
- Devices that phone home without consent

---

## 🔐 SECURITY HARDWARE NOTES

### YubiKey Usage

**Primary YubiKey (Daily):**

- Wyoming LLC bank accounts
- Crypto exchange accounts
- Password manager (Bitwarden)
- SSH authentication

**Backup YubiKey (Safe):**

- Stored in fireproof safe
- Only used if primary is lost
- Same credentials programmed

### Network Ghosting Hardware

**MAC Rotation:**

- Automatic via network_ghost.py script
- Runs every 30 minutes
- Requires admin/root access

**dVPN:**

- Mysterium Network node
- Multi-hop routing (3+ nodes)
- No centralized logging

---

## 📱 MOBILE SYNC CONFIGURATION

### Tailscale Setup

**On Linux Mint Workstation:**

```bash
# Install Tailscale
curl -fsSL https://tailscale.com/install.sh | sh

# Start Tailscale
sudo tailscale up

# Get IP address
tailscale ip -4
```

**On Samsung Phone:**

1. Install Tailscale from Play Store
2. Log in with same account
3. Connect to network
4. Access dashboard at: `http://100.x.x.x:8501`

### DeX Configuration

**Required:**

- USB-C to HDMI cable or DeX dock
- External monitor/TV
- Bluetooth keyboard/mouse (optional)

**Usage:**

1. Connect phone to monitor via USB-C
2. DeX mode activates automatically
3. Open browser → Navigate to Omega Dashboard
4. Full desktop experience

---

## ✅ FINAL PROCUREMENT CHECKLIST

### Immediate (This Week)

- [ ] Order AI workstation components
- [ ] Purchase YubiKeys (2x)
- [ ] Order Protectli Vault
- [ ] Order Home Assistant Yellow
- [ ] Verify Samsung phone compatibility

### Short-term (This Month)

- [ ] Order battery storage system
- [ ] Order solar panels + inverter
- [ ] Purchase smart home devices
- [ ] Order biometric wearable
- [ ] Set up Starlink

### Long-term (This Quarter)

- [ ] Build trading post structure
- [ ] Acquire medical equipment
- [ ] Purchase workshop tools
- [ ] Consider EV purchase

---

## 💡 COST OPTIMIZATION STRATEGIES

### Budget-Friendly Alternatives

**AI Workstation:**

- Single RTX 4090 instead of dual: -$3,200
- 128GB RAM instead of 256GB: -$400
- Used Threadripper 3000 series: -$2,000

**Off-Grid Power:**

- Start with 50kWh battery bank: -$12,000
- DIY 18650 battery packs: -$15,000
- Used solar panels: -$3,000

**Smart Home:**

- Start with essential devices only: -$800
- DIY sensors (ESP32 + ESPHome): -$500

**Total Potential Savings:** ~$36,900

**Minimum Viable System:** ~$35,000

---

## 🏴 FINAL NOTES

**The hardware is the foundation. The software is the intelligence. Together, they create sovereignty.**

**Every device you purchase becomes a node in your autonomous empire. Choose wisely.**

---

**SYSTEM:** Project Monolith Omega  
**DOCUMENT:** Mandatory Hardware Manifest  
**DATE:** February 3, 2026  
**STATUS:** READY FOR PROCUREMENT  
**CLASSIFICATION:** COMMANDER EYES ONLY
