# 🛒 AUTOMATED PROCUREMENT SYSTEM (v4.5)

**Status:** ACTIVE
**Organ:** THE HANDS (Moltbot + Purchasing Agent)
**Objective:** Autonomous biological and technological upgrades.

---

## ⚙️ THE PROTOCOL

This system autonomously converts digital fiat (Revenue) into physical sovereignty (Hardware/Assets).

### 1. The Trigger Logic

Purchasing is NOT time-based. It is **Revenue-Based**.

* **IF** `Treasury_Float` > $5,000 (Safety Buffer)
* **AND** `Revenue_This_Month` > `Next_Item_Cost`
* **THEN** Initiate Purchase Protocol.

### 2. The Shopping List (Priority Queue)

*Derived from `MANDATORY_HARDWARE_MANIFEST.md`*

1. **EnerVenue ESV (x3)** - $45,000 [CRITICAL]
2. **Source Hydropanels (x2)** - $6,000 [CRITICAL]
3. **Castellex Air 550** - $2,800 [DEFENSE]
4. **NVIDIA RTX 6090 (Reserved)** - $3,500 [INTELLIGENCE]
5. **Freeze Dryer (Harvest Right)** - $2,600 [SUSTENANCE]

---

## 🤖 AUTOMATION WORKFLOW

### Phase 1: The Scout (Moltbot)

The `Hands/moltbot.py` agent scrapes key vendors daily for global inventory and pricing.

* **Targets:** Amazon Business, eBay (Refurb Enterprise Tech), Direct Manufacturer Portals.
* **Condition:** Finds "In Stock" status + Price <= Target Price.

### Phase 2: The Cart (Staging)

Items are added to the cart.

* **Verification:** check URL against verified vendor list (in `config.py`).
* **Shipping:** Always to "The Drop" (Secure PO Box or secondary address), never home address directly if possible.

### Phase 3: The Purchase (Execution)

* **Micro-Purchases (<$100):** Auto-approve (e.g., cables, filters).
* **Macro-Purchases (>$100):** Request Commander Authorization via Dashboard.
  * *Action:* Notification sent to `monolith_ui.py`.
  * *Commander:* Clicks "APPROVE" button.
  * *Agent:* Cycles Virtual Credit Card (Privacy.com) -> Executes ONE-TIME transaction.

---

## 🛡️ SECURITY & FAILSAFES

1. **Burner Cards:** NEVER use main bank debit card. Use Privacy.com API to generate exact-limit merchant-locked cards.
2. **Price Logic:** If price is >10% over historical average, HOLD.
3. **Duplicate Check:** Query `InventoryDB` to ensure item isn't already owned.

---

## 📝 LOGGING

All purchases are logged to `Logs/procurement_log.json`:

* Timestamp
* Item Name
* Vendor
* Cost
* Privacy.com Card Last 4
* Tracking Number (Auto-scraped 24h later)
