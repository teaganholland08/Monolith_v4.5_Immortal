# MONOLITH MESHTASTIC INTEGRATION GUIDE

**Purpose:** Off-grid communication layer using LoRa radio  
**Range:** 5-10 km urban, 200+ km ideal conditions  
**Encryption:** AES-256 by default  
**Cost:** $20-$80 per device

---

## WHAT IS MESHTASTIC?

Meshtastic creates a **mesh network** of radios that relay messages to each other, eliminating need for:

- Cellular networks
- Wi-Fi/Internet
- Satellite service (except for long-range bridges)

**Use Cases for Monolith:**

- Emergency communication if internet/cell dies
- Off-grid coordination between home base and remote location
- Secure local messaging (not visible to ISP/government)
- Dead drop messaging (leave device at location, retrieve later)

---

## HARDWARE OPTIONS (2026)

### Budget: LilyGo T-Beam ($25)

- ESP32 processor
- 915MHz LoRa radio (US frequency)
- GPS built-in
- Battery powered (18650 cell)
- Range: 5-10 km
- **Best for:** Testing, basic messaging

### Standard: Heltec V3 ($35)

- OLED display
- Longer battery life
- Better antenna
- Range: 10-15 km
- **Best for:** Daily use, hiking

### Premium: LilyGo T-Deck Plus ($80)

- Full QWERTY keyboard
- 2.4" touchscreen
- SD card slot
- LoRa + WiFi + Bluetooth
- Range: 15-20 km
- **Best for:** Command center node, base station

### Custom: RAK Meshtastic Build ($150+)

- Weatherproof enclosure
- Solar panel
- High-gain antenna
- Range: 50+ km
- **Best for:** Permanent outdoor relay nodes

---

## SETUP (30 Minutes)

### 1. Flash Firmware

```bash
# Install Meshtastic CLI
python -m pip install meshtastic

# Flash device (connects via USB)
meshtastic --flash

# Or use web flasher: https://flasher.meshtastic.org
```

### 2. Configure Device

```bash
# Set node name
meshtastic --set-owner "MonolithNode1"

# Set channel encryption key (use same key for all your devices)
meshtastic --ch-set psk base64:<YOUR_KEY_HERE>

# Set region (915MHz for North America)
meshtastic --set lora.region US

# Disable telemetry broadcasting (save bandwidth)
meshtastic --set telemetry.device_update_interval 0
```

### 3. Test Communication

- Open Meshtastic app (iOS/Android)
- Pair via Bluetooth
- Send test message to another node
- Verify delivery

---

## INTEGRATION WITH MONOLITH

### Option 1: Serial API (Python)

```python
import meshtastic
import meshtastic.serial_interface

# Connect to device via USB
interface = meshtastic.serial_interface.SerialInterface()

# Send message
interface.sendText("MONOLITH: System online", 
                   destinationId="!XXXXXXXX")  # Node ID

# Receive messages
def on_receive(packet, interface):
    if packet['decoded']['portnum'] == 'TEXT_MESSAGE_APP':
        msg = packet['decoded']['payload'].decode('utf-8')
        print(f"Received: {msg}")

interface.onReceive = on_receive
```

### Option 2: MQTT Bridge (Network)

Meshtastic can bridge to MQTT for integration with Home Assistant or Monolith dashboard:

```yaml
# In Meshtastic settings
mqtt:
  enabled: true
  address: "mqtt.meshtastic.local"
  username: "monolith"
  password: "your_password"
  encryption_enabled: true
```

Then in Monolith:

```python
import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("mqtt.meshtastic.local", 1883)

def on_message(client, userdata, message):
    print(f"Mesh message: {message.payload.decode()}")

client.subscribe("msh/2/json/#")
client.on_message = on_message
client.loop_forever()
```

---

## CHANNEL CONFIGURATION

### Default Channel (Public)

- **Name:** LongFast
- **Encryption:** Base64 default key (everyone can decode)
- **Use:** General testing only

### Private Channel (Monolith Secure)

```bash
# Generate secure key
meshtastic --ch-add MonolithSecure

# Set encryption (32-byte key)
meshtastic --ch-set psk random --ch-index 1

# Only devices with this key can see messages
```

### Emergency Channel (No Encryption)

```bash
# For emergencies when you need to reach ANYONE
meshtastic --ch-set psk none --ch-index 2
```

---

## DEPLOYMENT STRATEGIES

### Strategy 1: Personal Network (2-3 Nodes)

**Setup:**

- 1x Base station (home, powered by AC or solar)
- 1x Mobile node (on person, battery)
- 1x Vehicle node (in car, powered by 12V)

**Use:** Off-grid communication when traveling within 20km of home.

### Strategy 2: Relay Network (5+ Nodes)

**Setup:**

- 1x Base station (home)
- 3x Relay nodes (high points: rooftops, hills, trees)
- 2x Mobile nodes (person, vehicle)

**Use:** Extend range to 100+ km by hopping between relays.

### Strategy 3: Dead Drop Messaging

**Setup:**

- Hide weatherproof Meshtastic node at predetermined location
- Pre-program message schedule (e.g., check every 6 hours)
- Leave messages by driving/walking close enough to transmit

**Use:** Covert communication without direct contact.

---

## SECURITY CONSIDERATIONS

### Encryption

✅ **Enabled by default:** AES-256 with PSK (Pre-Shared Key)  
✅ **PKI mode:** Public-key infrastructure for better security (firmware 2.7.15+)  
⚠️ **Radio silence:** Your device DOES transmit metadata (node ID, GPS if enabled)

### Anonymity

- Do NOT use real name as node name
- Disable GPS if location privacy is critical
- Use burner device (not linked to real identity)

### Range = Exposure

- Longer range = easier to detect with directional antenna
- Keep transmit power LOW if stealth is needed
- Use store-and-forward mode (message hops, no direct link)

---

## INTEGRATION WITH VANISHING PROTOCOL

### Pre-Configured Nodes

Add Meshtastic nodes to your Go-Bag:

| Node | Purpose | Config |
|------|---------|--------|
| **Primary** | Your personal device | Full keyboard, display |
| **Backup** | Redundant node (if primary fails) | Minimal, long battery |
| **Relay** | Extend range from base | Solar, weatherproof |

### Emergency Messaging Commands

Pre-program macros for quick messages:

```bash
# "I'm safe, no need for extraction"
meshtastic --sendtext "SAFE" --ch-index 1

# "Need immediate assistance at last GPS"
meshtastic --sendtext "HELP-GPS" --ch-index 1

# "Going dark, do not attempt contact"
meshtastic --sendtext "DARK" --ch-index 1
```

---

## MESH + STARLINK HYBRID

**Best of Both Worlds:**

- Use Meshtastic for local off-grid comms (0-50km)
- Use Starlink for long-range internet (anywhere on Earth)

**Setup:**

1. Starlink connects to internet
2. Starlink runs MQTT broker
3. Meshtastic bridges to MQTT
4. Remote Meshtastic node also bridges to MQTT (via different Starlink)
5. Messages relay through internet but encrypted end-to-end

**Result:** Global off-grid messaging network.

---

## LEGAL NOTES

### Allowed (ISM Band - 915MHz US, 868MHz EU)

✅ Unlicensed radio use  
✅ Encrypted messaging  
✅ Personal/recreational use  
✅ Emergency communication  

### Restricted

⚠️ Commercial use (requires business license)  
⚠️ High power transmitters (>1W typically)  

### Prohibited

❌ Interfering with emergency services  
❌ Transmitting on restricted frequencies  
❌ Using for illegal activities  

---

## COST BREAKDOWN

| Component | Qty | Cost | Purpose |
|-----------|-----|------|---------|
| LilyGo T-Beam | 2 | $50 | Base + Mobile |
| LilyGo T-Deck | 1 | $80 | Command Center |
| Solar Panel | 2 | $40 | Relay power |
| Antennas (upgrade) | 3 | $45 | Better range |
| Cases (weatherproof) | 2 | $30 | Outdoor nodes |
| **TOTAL** | | **$245** | Full mesh network |

---

## RECOMMENDED FIRST PURCHASE

**Start Simple:** LilyGo T-Beam (2-pack) - $50

- Test range in your area
- Learn firmware configuration
- Verify encryption works
- Decide if you need more nodes

**Upgrade Later:** Add relays and solar once you know it works.

---

## RESOURCES

- **Official Site:** <https://meshtastic.org>
- **Firmware Releases:** <https://github.com/meshtastic/firmware/releases>
- **Web Flasher:** <https://flasher.meshtastic.org>
- **Community Forum:** <https://meshtastic.discourse.group>
- **Range Calculator:** <https://meshtastic.org/docs/overview/range-tests>

---

**Status:** Meshtastic integration documented. Ready to add to Go-Bag and Shadow Net protocol.
