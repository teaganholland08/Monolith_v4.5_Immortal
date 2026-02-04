# 🦅 PROJECT MONOLITH: OPERATOR MANUAL (v4.5 IMMORTAL)

**Status:** ACTIVE
**Architecture:** Python Kernel (`monolith_omega.py`) + Streamlit UI (`monolith_ui.py`)

---

## 🚀 1. LAUNCH PROTOCOLS

### A. The Core (Omega Kernel)

This runs the autonomous revenue engine (Hydra) and security layers.

1. Open Terminal (PowerShell/CMD).
2. Navigate to the Fortress:

    ```powershell
    cd "C:\Users\Teagan Holland\Desktop\Monolith_v4.5_Immortal"
    ```

3. Ignite the Kernel:

    ```powershell
    python monolith_omega.py
    ```

    *You will see the "IMMORTAL" command prompt when ready.*

### B. The Interface (Command Deck)

This launches the visual dashboard for monitoring and manual override.

1. Open a **New** Terminal.
2. Navigate to the Fortress:

    ```powershell
    cd "C:\Users\Teagan Holland\Desktop\Monolith_v4.5_Immortal"
    ```

3. Launch the Dashboard:

    ```powershell
    streamlit run System/UI/monolith_ui.py
    ```

    *Browser will auto-launch at <http://localhost:8501>*

---

## 🛠️ 2. DEPENDENCIES & SETUP

If you are moving to a new machine, run this once:

```powershell
pip install -r requirements.txt
```

**Key Libraries:**

* `streamlit`: The Dashboard UI.
* `selenium` / `playwright`: The Hands (Web Automation).
* `web3`: Crypto interactions.
* `feedparser`: Intelligence gathering.

---

## ⚙️ 3. CONFIGURATION (Simulation vs. Production)

 The system handles "Real Money" capability via `config.py`.

* **Simulation Mode:** (`USE_SIMULATION_MODE = True`)
  * Safe. Mocks all purchases and trades.
  * Use this for testing new logic.
* **Production Mode:** (`USE_SIMULATION_MODE = False`)
  * **DANGER:** Real money will be spent provided API keys are set.
  * Ensure `config.py` keys (OpenAI, Stripe, Wallet PKs) are loaded via Environment Variables.

---

## 🚨 4. EMERGENCY OVERRIDES

**Situation: Runaway Spending / AI Hallucination**

* **Action:** Immediate Hard Kill.
* **Command:** Close the Terminal running `monolith_omega.py`.
* **Backup:** Task Manager -> End Process `python.exe`.

**Situation: Dashboard Glitch**

* **Action:** Soft Reset.
* **Command:** Press `Ctrl+C` in the Streamlit terminal, then re-run the launch command.

---

## 📝 5. DAILY RITUAL

1. **09:00:** Verify `logs/monolith.log` for overnight errors.
2. **09:05:** Check Revenue vs. Spending in Dashboard.
3. **09:10:** Clear alerts.

*SYSTEM IS YOURS. HUNT. BUILD. SURVIVE.*
