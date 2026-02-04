# Implementation Plan - Monolith Global Agentic Factory Upgrade

Transform Project Monolith into a recursive, five-pillar agentic system with a specialized Tax Accountant agent.

## User Review Required

> [!IMPORTANT]
> The "Accountant Agent" will simulate bank scraping and CRA integration for the 2026 landscape. Please confirm if you want the "Slip-Scraper" to be a separate script or integrated into the Accountant Agent.

## Proposed Changes

### Core Orchestration

#### [System/Agents/master_assistant.py]

- Organize agents into Five Strategic Vertical Pillars:
  - **Wealth Factory**: Treasurer, Accountant, Arbitrage Sentinel, Tax-Shield.
  - **Security Factory**: Cipher Agent, Metadata Scrambler, Physical Sentinel.
  - **Labor Factory**: Robotic Fleet Manager, Inventory Ghost, Scheduler.
  - **Health Factory**: Longevity Scout, Circadian Master, Stress Guardian.
  - **Development Factory**: Architect, Code-Gen, Hardware Auditor.
- Upgrade `spawn_worker` to use a more sophisticated template engine.

### Specialized Agents

#### [System/Agents/accountant_agent.py] (NEW)

- Implement Canadian (CRA/BC) tax logic.
- Simulated "Slip-Scraper" for T4/T5/T1135 pulls.
- Wealthsimple Tax AI integration stubs.

#### [System/Agents/tax_shield_agent.py] (NEW)

- Continuous monitoring of 2026 tax loopholes.

#### [System/Agents/cipher_agent.py] (NEW)

- Logic for PQC (Post-Quantum Cryptography) patterns (Kyber-1024).

### Maintenance & Discovery

#### [System/Agents/gap_scanner.py]

- Update the "required" list to match the 2026 Factory Blueprint.

## Verification Plan

### Automated Tests

- Run `master_assistant.py` to verify it spawns missing pillar agents.
- Run `accountant_agent.py` to verify tax deduction calculations and slip scraping simulation.

### Manual Verification

- Check `System/Sentinels/*.done` files to ensure all pillar agents are reporting status correctly.
- Launch the dashboard and verify the new vertical pillars are displayed.
