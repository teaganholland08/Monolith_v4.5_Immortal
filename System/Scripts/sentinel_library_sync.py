import os
import time

def sync_library_of_alexandria():
    """
    SENTINEL PROTOCOL: LIBRARY OF ALEXANDRIA
    Downloads (Generates) critical survival knowledge for Offline Vault Storage.
    Ensures continuity of species and system in Grid-Down scenarios.
    """
    print("🏰 SENTINEL: SECURING HUMAN KNOWLEDGE ARCHIVE...")
    
    # Define the Vault Path
    library_path = os.path.join(os.path.dirname(__file__), "..", "..", "Brain", "Library")
    if not os.path.exists(library_path):
        os.makedirs(library_path)
        print(f"   -> EXTENDING VAULT: {library_path}")

    # Define the Books (Survival Wikis)
    books = [
        {
            "filename": "GRID_DOWN_OPERATIONS.md",
            "title": "PROTOCOL OMEGA: TOTAL POWER FAILURE",
            "content": """# GRID DOWN OPERTIONS MANUAL
**STATUS:** OFFLINE ACCESS ONLY
**PRIORITY:** CRITICAL

## 1. IMMEDIATE ACTIONS (0-4 HOURS)
*   [ ] Sever connection to Utility Grid (Main Breaker OFF).
*   [ ] Activate EnerVenue Battery Banks (Island Mode).
*   [ ] Deploy Faraday Blankets over sensitive electronics (Laptops, Radios).
*   [ ] Lock Down Perimeter (Mag-Locks to Fail-Secure).

## 2. WATER SECURITY
*   [ ] Enable Atmospheric Water Generator (Watergen).
*   [ ] If Power < 20%, switch to Gravity Feed Filtration (Berkey).
*   [ ] Ration: 4L per person/day.

## 3. ENERGY MANAGEMENT
*   [ ] Solar Input Only.
*   [ ] DISABLE: AC, Electric Oven, Washer/Dryer.
*   [ ] ENABLE: Server Core (Low Power), Security Cameras, Fridge.
"""
        },
        {
            "filename": "TACTICAL_MEDICINE_ATLAS.md",
            "title": "TACTICAL MEDICINE & SURGERY",
            "content": """# FIELD MEDICINE DATABASE
**WARNING:** FOR EMERGENCY USE ONLY.

## 1. TRAUMA (BLEEDING)
*   **Tourniquet:** Apply High & Tight. Twist until bleeding STOPS.
*   **Wound Packing:** Use Hemostatic Gauze (Celox/QuikClot). Pack bone-deep.

## 2. INFECTION CONTROL
*   **Antibiotics:**
    *   Amoxicillin 500mg: General infection.
    *   Doxycycline 100mg: Tick/Bio-agents.
*   **Sanitation:** Boil water 3 mins rolling boil.
"""
        },
        {
            "filename": "COMMS_MESH_FREQUENCIES.md",
            "title": "COMMUNICATION RELAY PLAN",
            "content": """# APOCALYPSE COMMUNICATIONS
**HARDWARE:** MESHTASTIC + HAM RADIO + SATELLITE

## 1. FREQUENCIES (MONITORING)
*   **National Calling:** 146.520 MHz
*   **Prepper Net:** 14.242 MHz (USB)
*   **Local Mesh:** Channel 0 (LongFast)

## 2. STARLINK BACKUP
*   Deploy Starlink Dish in 'Stow' position inside Faraday Cage when not in use.
*   Burst Transmit: Only power on for 5 mins to download intelligence, then OFF.
"""
        }
    ]

    # "Download" Books
    for book in books:
        filepath = os.path.join(library_path, book['filename'])
        print(f"   📚 ARCHIVING: {book['title']}...")
        time.sleep(1.0) # Simulate write/download speed
        with open(filepath, "w") as f:
            f.write(book['content'])
        print(f"      -> SAVED to /Brain/Library/{book['filename']}")

    print("\n✅ LIBRARY OF ALEXANDRIA: SYNCHRONIZED.")
    print("   The System (and You) can now survive 100 years offline.")

if __name__ == "__main__":
    sync_library_of_alexandria()
