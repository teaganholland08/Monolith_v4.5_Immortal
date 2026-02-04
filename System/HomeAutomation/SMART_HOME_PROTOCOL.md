# MONOLITH SMART HOME PROTOCOL

**Strategy:** Local Fallback Architecture  
**Principle:** Convenience today, resilience tomorrow  
**Status:** Hybrid (Cloud + Local)

---

## CORE PHILOSOPHY

### Normal Mode (90% of time)

- Use cloud features (voice assistants, phone apps, automation)
- Full Samsung SmartThings integration
- Alexa/Google Assistant voice control
- Remote access from anywhere

### Stealth Mode (IF needed)

- Cut internet connection
- Everything still works locally
- No data leaving house
- Full manual override available

**Rule:** Every device must have a local fallback. If it requires cloud to function, don't buy it.

---

## THE HUB: HOME ASSISTANT

### Why Home Assistant?

- **Connects to everything:** Samsung SmartThings, Alexa, Google, Apple, Zigbee, Z-Wave, Matter
- **Local processing:** Runs on hardware in your house (not Amazon's servers)
- **Survives internet outage:** Automations keep running
- **Open source:** No company can shut it down
- **Free:** No subscription fees ever

### Hardware Options

| Device | Cost | Performance | Complexity |
|--------|------|-------------|------------|
| Raspberry Pi 4 (4GB) | $55 | Good | Easy |
| Raspberry Pi 5 (8GB) | $80 | Excellent | Easy |
| Home Assistant Yellow | $140 | Excellent | Easiest |
| Old PC/Laptop | $0 | Great | Medium |

**Recommendation:** Raspberry Pi 4 (4GB) - Best value for Monolith.

### Setup (30 minutes)

1. Download: <https://www.home-assistant.io/installation/raspberrypi>
2. Flash to MicroSD using Raspberry Pi Imager
3. Insert card, connect ethernet, power on
4. Visit: <http://homeassistant.local:8123>
5. Create account (stays 100% local)

---

## SAMSUNG SMARTTHINGS BRIDGE

### Current Setup (You Already Have)

- **SmartThings Hub:** Built into Samsung phone/TV
- **Works with:** Samsung appliances, most smart home brands
- **Cloud:** Yes (Samsung servers)
- **Local:** Partial (lighting automations run local)

### Integration Strategy

**Use SmartThings AS IS, but connect to Home Assistant:**

1. In Home Assistant: Settings > Devices & Services > Add Integration > "SmartThings"
2. Link your Samsung account
3. Now all SmartThings devices appear in Home Assistant
4. Create automations in Home Assistant (more powerful)
5. If internet fails, Home Assistant keeps running

**Result:** You get Samsung's easy app + Home Assistant's resilience.

---

## DEVICE RECOMMENDATIONS

### Tier 1: Matter/Thread (2026 Standard)

**What is Matter?**

- Universal smart home language (Apple + Google + Amazon + Samsung agreed)
- Devices work with ALL assistants simultaneously
- Local control by design
- No vendor lock-in

**Matter-Certified Shopping List:**

#### Lighting

- **Philips Hue (White & Color Starter Kit)** - $130
  - Local control via Hue Bridge
  - Works with: Everything
  - Fallback: Physical switches still work
  
- **Nanoleaf Essentials (Thread)** - $20/bulb
  - No hub needed (uses iPhone/HomePod as Thread border router)
  - Works with Matter
  
#### Smart Plugs

- **Eve Energy (Thread)** - $40
  - Power monitoring
  - Local only (no cloud)

#### Door Locks

- **Yale Assure Lock 2 (Matter)** - $280
  - Z-Wave + Matter
  - Physical key backup
  - Local control

### Tier 2: Zigbee/Z-Wave (Private Mesh)

**Why Zigbee/Z-Wave?**

- Doesn't use Wi-Fi (creates own mesh network)
- Very hard to hack (invisible to router)
- Low power (sensors last 2+ years on battery)
- 100% local

**Shopping List:**

#### Motion Sensors

- **Aqara Motion Sensor (Zigbee)** - $17
  - 2-year battery
  - Works with Home Assistant

#### Door/Window Sensors

- **Aqara Door Sensor (Zigbee)** - $15
  - Know when doors open
  - Trigger automations

#### Smart Switches

- **Inovelli Z-Wave Switches** - $50
  - Physical manual override
  - Scene control (double-tap, triple-tap)

### Tier 3: Cameras (NVR = Local Storage)

**Avoid:** Ring, Nest, Arlo (all cloud-dependent)  
**Use:** Cameras with local storage

#### Best Options

**Budget: Eufy Indoor Cam 2K** - $40

- Local storage (no cloud required)
- Works without internet
- Optional cloud backup

**Pro: Ubiquiti UniFi Protect**

- UniFi Cloud Gateway Ultra - $129
- G4 Bullet Camera - $129/each
- **Local NVR** (stores 30+ days of video)
- Professional-grade
- View from anywhere (but video stays home)

**DIY: Frigate NVR** - $0 (software)

- Runs on Raspberry Pi
- Works with cheap IP cameras ($30 each)
- AI object detection (person, car, animal)
- Integrates with Home Assistant

---

## VOICE CONTROL INTEGRATION

### Option 1: Keep Existing (Alexa/Google)

**How it works:**

1. Home Assistant exposes devices to Alexa/Google
2. Say: "Alexa, turn off all lights"
3. Alexa → Home Assistant → Devices (locally)

**Trade-off:** Voice goes to cloud, but execution is local.

### Option 2: Home Assistant "Assist" (100% Local)

**How it works:**

1. Install "Assist" on Home Assistant
2. Use old smartphone as voice terminal
3. Say: "Turn on bedroom lights"
4. **Nothing** leaves your house

**Trade-off:** Not as good as Alexa (yet), but improving rapidly.

### Option 3: Hybrid (Best of Both)

- Use Alexa/Google 99% of time (convenient)
- Enable Home Assistant Assist as backup
- If internet dies, local voice still works

---

## MONOLITH DASHBOARD INTEGRATION

### 3-Tab Layout

#### Tab 1: The World (Monolith AI)

- Market data (BTC, ETH, SPY)
- News scanner signals
- Revenue tracking (Gumroad, Medium)
- Tax optimizer recommendations

#### Tab 2: The House (Smart Home)

**Embedded Home Assistant iframe:**

```html
<iframe src="http://homeassistant.local:8123" 
        width="100%" height="800px"></iframe>
```

**Or custom widgets:**

- Live camera feeds (4-camera view)
- Light controls (quick toggles)
- Power usage graph
- Security status (all doors locked/unlocked)

#### Tab 3: The System (Diagnostics)

- CPU/RAM usage
- VPN status
- Hygiene engine reports
- Security logs

---

## POWER FAILURE PROTOCOL

### What Happens if Internet Dies?

| Device Type | Cloud Mode | Local Fallback |
|-------------|------------|----------------|
| Philips Hue | App control fails | Physical switches work |
| Zigbee Sensors | ✅ Keep working | Home Assistant automations run |
| Yale Lock | App control fails | Physical keypad works |
| Eufy Camera | Remote view fails | ✅ Local storage continues |
| Home Assistant | ✅ 100% operational | All automations run |

### What Happens if Power Dies?

**Battery Backup (UPS):**

- **APC Back-UPS 600VA** - $75
- Powers: Raspberry Pi + Router + 1 camera
- Runtime: 2-4 hours

**Full House Backup:**

- **EcoFlow Delta Pro** - $3,600 (from your hardware manifest)
- Powers entire house for days
- Solar recharging capability

---

## AUTOMATION EXAMPLES

### Morning Routine

**Trigger:** 7:00 AM weekdays  
**Actions:**

1. Gradually brighten bedroom lights (sunrise simulation)
2. Start coffee maker (smart plug)
3. Read morning news summary via speaker
4. Unlock front door (if armed security system is disarmed)

### Security Lockdown

**Trigger:** Say "Lockdown mode" OR Monolith detects threat  
**Actions:**

1. Lock all doors
2. Turn off all lights
3. Start recording all cameras
4. Send alert to phone
5. Activate alarm siren (if intruder detected)

### Energy Optimization

**Trigger:** Electricity price spike (via API)  
**Actions:**

1. Turn off non-essential devices
2. Set thermostat to eco mode
3. Delay EV charging until off-peak

### Presence Simulation (Vacation)

**Trigger:** Away mode enabled  
**Actions:**

1. Random light patterns (8PM-11PM)
2. Open/close blinds on schedule
3. Play TV audio occasionally
4. Make it look like you're home

---

## SHOPPING LIST (Complete Starter Kit)

### Core Hub

- [ ] Raspberry Pi 4 (4GB) - $55
- [ ] MicroSD card (64GB) - $12
- [ ] Power supply - $8
- [ ] Ethernet cable - $5

### Lighting (Start Small)

- [ ] Philips Hue Bridge - $60
- [ ] Philips Hue White Starter (4 bulbs) - $100

### Security

- [ ] 2x Aqara Door Sensors - $30
- [ ] 1x Aqara Motion Sensor - $17
- [ ] Eufy Indoor Cam 2K - $40

### Power/Control

- [ ] Eve Energy Smart Plug (Matter) - $40
- [ ] Aqara Temperature Sensor - $15

### Backup Power

- [ ] APC Back-UPS 600VA - $75

**Total:** ~$457 for full smart home foundation

---

## SETUP TIMELINE

### Week 1: Hub Setup (2 hours)

- Set up Raspberry Pi with Home Assistant
- Connect to network
- Link Samsung SmartThings account
- Add all existing devices

### Week 2: Add Lighting (1 hour)

- Install Philips Hue Bridge
- Replace 4 most-used bulbs
- Create first automation (bedtime routine)

### Week 3: Add Security (1 hour)

- Install door sensors on front/back door
- Set up motion sensor in hallway
- Create "Lockdown" scene

### Week 4: Add Camera (1 hour)

- Mount Eufy camera
- Configure motion detection
- Test recording playback

### Month 2: Expand

- Add more lights
- Add temperature sensors
- Create advanced automations
- Integrate with Monolith dashboard

---

## SECURITY CONSIDERATIONS

### Network Segmentation

**Create 3 Networks:**

1. **Main Network:** Computer, phone (192.168.1.x)
2. **IoT Network:** Smart home devices (192.168.2.x)
3. **Guest Network:** Visitors (192.168.3.x)

**Why:** If a smart bulb gets hacked, it can't reach your computer.

### Firewall Rules

- Smart home devices can talk to Home Assistant
- Smart home devices CANNOT access internet (unless needed)
- Home Assistant can access internet (for updates only)

### Camera Privacy

- Cameras NEVER point at private areas (bedroom, bathroom)
- Use privacy shutters when home
- Disable audio recording (unless security camera)

---

## MIGRATION PATH TO STEALTH

### IF You Need to Go Off-Grid

#### Phase 1: Disable Cloud (10 minutes)

1. Turn off router Wi-Fi
2. Home Assistant still works (ethernet)
3. All Zigbee/Z-Wave devices work
4. Cameras record locally

#### Phase 2: Air-Gap (30 minutes)

1. Disconnect internet completely
2. Set up local DNS (Pi-hole on Raspberry Pi)
3. All devices communicate via LAN only

#### Phase 3: Maximum Stealth (IF paranoid)

1. Replace Philips Hue with Zigbee bulbs (no cloud option)
2. Replace Eufy with Frigate NVR (open source)
3. Use Home Assistant voice (no Alexa/Google)

**Result:** Fully functional smart home with ZERO internet dependency.

---

## MONOLITH VOICE COMMANDS

### Current Home Assistant Integration

**In `monolith_omega.py` conversational mode:**

```
User: "Lock the house"
Monolith: → Calls Home Assistant API → Locks all smart locks

User: "Lights off"
Monolith: → Turns off all lights

User: "Security status"
Monolith: → Reports all door sensors, camera status
```

### Future: Full Voice Pipeline

1. User speaks to microphone
2. Monolith processes command
3. If home control → Route to Home Assistant
4. If market question → Route to Oracle
5. If system command → Route to OS Core

---

## FAQ

**Q: If I buy Matter devices, do I still need Home Assistant?**  
A: Technically no, but Home Assistant gives you WAY more automation power and privacy.

**Q: Can I use my Samsung TV as a hub?**  
A: Yes, newer Samsung TVs have SmartThings built-in. But add Home Assistant for local backup.

**Q: What if I move?**  
A: Unplug Raspberry Pi, take it to new house, plug in. Everything works immediately (devices reconnect automatically).

**Q: Is this expensive?**  
A: Starter kit is ~$450. But you can start with just Home Assistant ($80) and add devices slowly.

**Q: Will this work with my existing Samsung smart stuff?**  
A: Yes, 100%. SmartThings integration means all your existing devices work with Home Assistant.

---

## NEXT STEPS

1. **Order Raspberry Pi 4 kit** (or use old laptop)
2. **Install Home Assistant** (30 min)
3. **Connect SmartThings** (5 min)
4. **Add existing devices** to Home Assistant
5. **Create first automation** (bedtime lights)
6. **Integrate into Monolith dashboard** (iframe or API)

**Full guide:** <https://www.home-assistant.io/getting-started>

---

**Status:** You now have the blueprint for a smart home that works TODAY and survives TOMORROW.
