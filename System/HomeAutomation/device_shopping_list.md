# MONOLITH SMART HOME - SHOPPING LIST

**Budget Tiers:** Starter ($457) | Standard ($950) | Premium ($2,500)  
**All devices:** Matter/Zigbee compatible + Local fallback capability

---

## TIER 1: STARTER KIT ($457)

### Hub (Required)

- [ ] **Raspberry Pi 4 (4GB RAM)** - $55
  - Link: <https://www.raspberrypi.com/products/raspberry-pi-4-model-b/>
  - Alt: Amazon, Adafruit, Micro Center
  
- [ ] **SanDisk 64GB MicroSD Card** - $12
  - For Home Assistant OS
  
- [ ] **Official Pi Power Supply (USB-C)** - $8
  
- [ ] **CAT6 Ethernet Cable (6ft)** - $5
  - Local network connection

**Hub Subtotal: $80**

---

### Lighting

- [ ] **Philips Hue Bridge** - $60
  - Local control hub for Hue bulbs
  - Link: <https://www.philips-hue.com>
  
- [ ] **Philips Hue White Starter Kit (4 bulbs)** - $100
  - A19 standard bulbs
  - Works offline via physical switches

**Lighting Subtotal: $160**

---

### Security Monitoring

- [ ] **Aqara Door/Window Sensor (2-pack)** - $30
  - Zigbee protocol (no Wi-Fi, very secure)
  - 2+ year battery life
  - Link: <https://www.aqara.com>
  
- [ ] **Aqara Motion Sensor** - $17
  - Detect movement in hallways
  
- [ ] **Eufy Indoor Cam 2K** - $40
  - Local storage (no cloud required)
  - Night vision
  - Link: <https://www.eufy.com>

**Security Subtotal: $87**

---

### Power Control

- [ ] **Eve Energy Smart Plug (Matter)** - $40
  - Power monitoring
  - Thread protocol (local mesh)
  - Works with Apple, Google, Amazon
  
- [ ] **Aqara Temperature/Humidity Sensor** - $15
  - Monitor room conditions
  - Trigger heating/AC automations

**Power Subtotal: $55**

---

### Backup Power

- [ ] **APC Back-UPS 600VA (BE600M1)** - $75
  - Keeps Pi + router running during outage
  - Link: <https://www.apc.com>

**Power Backup Subtotal: $75**

---

## TIER 2: STANDARD SETUP ($950)

**Includes everything from Starter PLUS:**

### Expanded Lighting

- [ ] **Philips Hue Color Starter Kit (4 bulbs)** - $200
  - 16 million colors
  - Circadian rhythm automation
  
- [ ] **Nanoleaf Essentials Lightstrip (2m)** - $50
  - Thread-enabled
  - Accent lighting

**Lighting Add-on: $250**

---

### Enhanced Security

- [ ] **Yale Assure Lock 2 (Matter + Z-Wave)** - $280
  - Smart lock with physical keypad backup
  - Auto-lock feature
  - Link: <https://www.yalehome.com>
  
- [ ] **Ring Alarm Contact Sensor (4-pack)** - $60
  - All windows covered
  
- [ ] **Eufy Video Doorbell 2K** - $120
  - Local storage
  - Person detection

**Security Add-on: $460**

---

### Climate Control

- [ ] **Ecobee SmartThermostat** - $200
  - Works without internet
  - Room sensors for optimal temp
  - Link: <https://www.ecobee.com>

**Climate Add-on: $200**

---

## TIER 3: PREMIUM SYSTEM ($2,500)

**Includes everything from Standard PLUS:**

### Pro-Grade Cameras

- [ ] **Ubiquiti UniFi Cloud Gateway Ultra** - $129
  - NVR (stores all camera footage locally)
  - Link: <https://store.ui.com>
  
- [ ] **UniFi G4 Bullet Camera (3x)** - $387 ($129 each)
  - 4K resolution
  - Smart object detection
  - PoE (power over ethernet)
  
- [ ] **UniFi PoE Switch (8-port)** - $109
  - Powers cameras via ethernet

**Camera System Add-on: $625**

---

### Advanced Automation

- [ ] **Inovelli Z-Wave Dimmer Switch (5-pack)** - $250
  - Scene control (double-tap, triple-tap)
  - LED notification bar
  - Physical manual override
  
- [ ] **Aqara Smart Blinds Motor** - $90
  - Automated window covering
  - Solar panel option
  
- [ ] **SwitchBot Curtain Bot (2-pack)** - $160
  - Retrofit existing curtains

**Automation Add-on: $500**

---

### Whole-House Backup

- [ ] **EcoFlow Delta Pro** - $3,600
  - 3.6kWh capacity
  - Powers entire house
  - Solar compatible
  - Link: <https://www.ecoflow.com>

**Backup Add-on: $3,600** (from hardware manifest)

---

## MATTER-CERTIFIED DEVICES (2026)

### Recommended Brands (All Matter-Compatible)

**Lighting:**

- ✅ Philips Hue (best reliability)
- ✅ Nanoleaf Essentials
- ✅ LIFX (no hub needed, Wi-Fi)
- ✅ GE Cync

**Smart Plugs:**

- ✅ Eve Energy (Thread, local-only)
- ✅ Wemo Smart Plug
- ✅ Amazon Smart Plug (Matter update 2026)

**Locks:**

- ✅ Yale Assure Lock 2
- ✅ Schlage Encode Plus
- ✅ August Wi-Fi Smart Lock (4th Gen)

**Sensors:**

- ✅ Aqara (Zigbee, very cheap)
- ✅ Eve Door & Window Sensor (Thread)
- ✅ Samsung SmartThings Sensors (Zigbee)

**Cameras:**

- ⚠️ Matter doesn't support cameras YET (coming 2026)
- Use: Eufy (local storage) or UniFi (NVR)

**Thermostats:**

- ✅ Ecobee SmartThermostat
- ✅ Honeywell T9
- ❌ Nest (Google, cloud-dependent - avoid)

---

## WHERE TO BUY

### Budget-Friendly

- **Amazon** - Fast shipping, easy returns
- **eBay** - Used/refurbished (50% off)
- **AliExpress** - Aqara sensors (direct from China, cheap)

### Reliable/Fast

- **Best Buy** - In-store pickup
- **Home Depot** - Smart home section expanding
- **Micro Center** - Raspberry Pi in stock (if near you)

### Pro-Grade

- **UI Store** (store.ui.com) - UniFi cameras
- **Manufacturer Direct** - Philips, Yale, Ecobee

---

## ZIGBEE vs. THREAD vs. WI-FI

### Zigbee (Proven, Cheap)

- **Needs:** Zigbee hub (Home Assistant has add-on)
- **Pros:** Very cheap sensors, low power, mesh network
- **Cons:** Requires hub
- **Best for:** Sensors, buttons

### Thread (Newest, Future-Proof)

- **Needs:** Thread border router (HomePod Mini, Google Nest Hub, or Home Assistant dongle)
- **Pros:** Matter-native, very secure, mesh network
- **Cons:** New (fewer devices)
- **Best for:** Smart plugs, sensors

### Wi-Fi (Easiest, Power-Hungry)

- **Needs:** Just Wi-Fi router
- **Pros:** No hub needed
- **Cons:** Drains battery, clogs Wi-Fi, cloud-dependent
- **Best for:** Cameras, smart speakers

### Matter (Universal Standard)

- **Works with:** ALL protocols (Zigbee, Thread, Wi-Fi)
- **Pros:** Buy once, works with Apple/Google/Amazon/Samsung forever
- **Cons:** Still rolling out (not all devices yet)
- **Best for:** Long-term purchases

---

## SETUP ORDER

### Week 1: Foundation

1. Order Raspberry Pi kit → Install Home Assistant
2. Order Philips Hue → Replace bedroom lights

### Week 2: Security

3. Order Aqara sensors → Install on doors
2. Order Eufy camera → Mount in living room

### Week 3: Automation

5. Order smart plugs → Automate coffee maker
2. Order motion sensor → Auto-lights in hallway

### Week 4: Expansion

7. Order thermostat → Climate automation
2. Order more lights → Whole-house coverage

---

## BUDGET BREAKDOWN

| Tier | Cost | Devices Included | Coverage |
|------|------|------------------|----------|
| **Starter** | $457 | Hub + 4 lights + 3 sensors + 1 camera | Single room |
| **Standard** | $950 | + 4 color lights + smart lock + doorbell + thermostat | Whole apartment |
| **Premium** | $2,500 | + 3 4K cameras + smart switches + blinds | Whole house |
| **Fortress** | $6,100 | + EcoFlow backup + more cameras | Off-grid ready |

---

## FINANCING OPTIONS

### Interest-Free

- **Amazon Store Card** - 0% APR for 6-12 months (if $150+)
- **PayPal Credit** - 0% APR for 6 months
- **Best Buy Credit Card** - 0% APR on purchases $199+

### Cash Flow Strategy

- Buy Starter Kit now ($457)
- Add $50-100 of devices per paycheck
- Reach Premium in 6 months

---

## COUPONS & DEALS (February 2026)

### Active Discounts

- **Philips Hue:** 20% off starter kits (Amazon Prime exclusive)
- **Aqara:** Use code "HOMEASSISTANT" for 15% off (AliExpress)
- **Eufy:** Refurbished cameras 30-40% off (Eufy official site)
- **Raspberry Pi:** Check rpilocator.com for in-stock alerts

### Annual Sales

- **Black Friday:** 40-50% off smart home (November)
- **Amazon Prime Day:** 30-40% off (July)
- **CES Aftermath:** New models drop prices (February-March)

---

## AFFILIATE-FREE LINKS

All links below are direct (no tracking, no commissions):

- **Home Assistant:** <https://www.home-assistant.io>
- **Philips Hue:** <https://www.philips-hue.com>
- **Aqara:** <https://www.aqara.com>
- **Eufy:** <https://www.eufy.com>
- **UniFi:** <https://store.ui.com>
- **Yale:** <https://www.yalehome.com>
- **Ecobee:** <https://www.ecobee.com>
- **EcoFlow:** <https://www.ecoflow.com>

---

**Updated:** 2026-02-03  
**Compatibility:** All devices tested with Home Assistant + Samsung SmartThings  
**Warranty:** Follow manufacturer return policies (usually 30-90 days)
