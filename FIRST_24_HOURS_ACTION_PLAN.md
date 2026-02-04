# 🏁 THE "FIRST 24 HOURS" ACTION PLAN

**Objective:** Establish system dominance and verify all 4 layers of the Monolith.

---

## ⏰ HOUR 0-2: THE NEURAL HANDSHAKE

### Actions

- [ ] Execute `REPAIR_MONOLITH.bat` to initialize the system
- [ ] Run `python -m streamlit run System\UI\monolith_ui.py`
- [ ] Open dashboard at <http://localhost:8501>

### Verification

- [ ] Confirm Hydra Deck shows "HUNTING"
- [ ] Verify Shadow Net reads "DEFCON 5"
- [ ] Check all 4 metrics display correctly

### Safety

- [ ] Register two YubiKey hardware tokens
- [ ] Set up local and cloud access authentication
- [ ] Test emergency kill-switch hotkey

---

## ⏰ HOUR 2-6: THE FINANCIAL GENESIS

### Bootstrap Actions

- [ ] In Command Line, type: **"Alfred, initiate Phase 0 Bootstrap."**
- [ ] Monitor Operations Account for first transaction

### Bootstrap Task

The AI will begin scanning for Attention Gaps on Medium and X to generate your first $1.00 seed capital.

### Observation

- [ ] Watch for first incoming transaction
- [ ] Verify Hydra is actively hunting
- [ ] Check revenue streams table

---

## ⏰ HOUR 6-12: PHYSICAL & IOT CALIBRATION

### IoT Setup Actions

- [ ] Connect SmartThings Token to `concierge_main.py`
- [ ] Set environment variables:

  ```powershell
  setx HOME_ASSISTANT_TOKEN "your-token"
  setx HOME_ASSISTANT_URL "http://your-ha-instance:8123"
  ```

### Voice Test

- [ ] Issue command: **"Alfred, lock the fortress and set night-cycle lighting."**

### Verification

- [ ] Ensure Home Assistant confirms physical state changes
- [ ] Test all smart locks respond
- [ ] Verify lighting controls work

---

## ⏰ HOUR 12-24: THE SHADOW ALIGNMENT

### Shadow Setup Actions

- [ ] Verify Offline Ark is indexing correctly
- [ ] Check system downloaded local Powell River map
- [ ] Confirm Medical/Apothecary guides are accessible

### The Transition

At **21:00**, the system will enter **"Cave Mode"**:

- Silences all non-DEFCON 1 notifications
- Protects sleep cycle
- Maintains background monitoring

---

## 📦 THE DIGITAL "GO-BAG" (ENCRYPTED USB)

### Go-Bag Contents to Prepare

- [ ] Copy of `PROJECT_MONOLITH_OMEGA_FINAL.md`
- [ ] `requirements.txt` file
- [ ] `config.py` configuration
- [ ] All Python scripts from `System\Scripts\`
- [ ] Emergency access credentials

### Usage

For rapid redeployment if primary PC is physically destroyed.

---

## 🔄 THE MAINTENANCE ROUTINE (WEEKLY)

### Every Sunday

- [ ] Ask: **"Alfred, what is the ROI on our current compute usage?"**
- [ ] Review revenue vs. expenses
- [ ] Check system health metrics

### Monthly Red-Team Test

- [ ] Flip main breaker
- [ ] Run "Lights Out" Simulation
- [ ] Test battery and gasifier backup

---

## 📊 THE SCALING GOVERNOR

### Rules

- [ ] System forbidden from spending >30% monthly profit on hardware
- [ ] If profit = $0.00 for 48 hours → auto-kill current niche
- [ ] Rotate to next "Hydra Head" automatically

---

## ✅ DAY 1 COMPLETION CHECKLIST

By end of first 24 hours, verify:

- [ ] Dashboard is live and accessible
- [ ] At least one revenue stream is active
- [ ] Smart home controls respond to commands
- [ ] Shadow is monitoring global threats
- [ ] Cave Mode activates at 21:00
- [ ] Emergency protocols are tested
- [ ] Backup USB is prepared and secured

---

## 🚨 TROUBLESHOOTING

### Dashboard Won't Load

```powershell
# Kill existing processes
Get-Process | Where-Object {$_.ProcessName -eq "streamlit"} | Stop-Process -Force

# Restart
cd C:\Monolith
python -m streamlit run System\UI\monolith_ui.py
```

### Voice Commands Not Working

- Check microphone permissions
- Install: `pip install SpeechRecognition pyaudio`
- Fallback to text input

### Smart Home Not Responding

- Verify Home Assistant is running
- Check token is set correctly
- Test connection manually

---

**SYSTEM:** Project Monolith Omega  
**STATUS:** Day Zero Protocol  
**UPDATED:** February 3, 2026
