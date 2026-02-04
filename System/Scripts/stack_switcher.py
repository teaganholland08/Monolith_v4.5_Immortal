"""
🏴 PROJECT MONOLITH: STACK SWITCHER
Interactive utility to switch between Fortress (Local) and God Mode (Cloud)
"""

import os
import sys

def display_banner():
    print("\n" + "="*60)
    print("🏴 PROJECT MONOLITH: STACK SWITCHER")
    print("="*60)

def display_stacks():
    print("\nAVAILABLE STACKS:\n")
    
    print("🔒 [A] FORTRESS MODE (Local)")
    print("   ├─ Privacy: MAXIMUM")
    print("   ├─ Cost: $0 (No API fees)")
    print("   ├─ Internet: NOT REQUIRED")
    print("   ├─ AI: Llama 3 (Local)")
    print("   ├─ Images: Stable Diffusion XL")
    print("   └─ Use Case: Privacy, Offline, Learning\n")
    
    print("☁️  [B] GOD MODE (Cloud)")
    print("   ├─ Intelligence: MAXIMUM")
    print("   ├─ Cost: ~$0.01/request")
    print("   ├─ Internet: REQUIRED")
    print("   ├─ AI: GPT-5, Claude 4, Groq")
    print("   ├─ Images: Midjourney, DALL-E")
    print("   ├─ Payments: Stripe, PayPal, Crypto")
    print("   └─ Use Case: Max Performance, Revenue Generation\n")

def get_current_stack():
    """Read current stack from config.py"""
    config_path = "C:/Monolith/config.py"
    
    if not os.path.exists(config_path):
        return "UNKNOWN"
    
    with open(config_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if 'ACTIVE_STACK: Literal["LOCAL", "CLOUD"] = "LOCAL"' in content:
        return "LOCAL"
    elif 'ACTIVE_STACK: Literal["LOCAL", "CLOUD"] = "CLOUD"' in content:
        return "CLOUD"
    else:
        return "UNKNOWN"

def switch_stack(new_stack):
    """Switch to the specified stack"""
    config_path = "C:/Monolith/config.py"
    
    if not os.path.exists(config_path):
        print("❌ Error: config.py not found!")
        return False
    
    with open(config_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the ACTIVE_STACK line
    if new_stack == "LOCAL":
        new_content = content.replace(
            'ACTIVE_STACK: Literal["LOCAL", "CLOUD"] = "CLOUD"',
            'ACTIVE_STACK: Literal["LOCAL", "CLOUD"] = "LOCAL"'
        )
    else:
        new_content = content.replace(
            'ACTIVE_STACK: Literal["LOCAL", "CLOUD"] = "LOCAL"',
            'ACTIVE_STACK: Literal["LOCAL", "CLOUD"] = "CLOUD"'
        )
    
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

def main():
    display_banner()
    
    current = get_current_stack()
    
    if current == "LOCAL":
        print(f"\n📍 Current Stack: 🔒 FORTRESS MODE (Local)")
    elif current == "CLOUD":
        print(f"\n📍 Current Stack: ☁️ GOD MODE (Cloud)")
    else:
        print(f"\n📍 Current Stack: UNKNOWN")
    
    display_stacks()
    
    choice = input(">> SELECT STACK (A/B) or Q to quit: ").strip().upper()
    
    if choice == 'Q':
        print("\n👋 Exiting...")
        return
    
    if choice == 'A':
        new_stack = "LOCAL"
        mode_name = "🔒 FORTRESS MODE"
    elif choice == 'B':
        new_stack = "CLOUD"
        mode_name = "☁️ GOD MODE"
    else:
        print("\n❌ Invalid choice!")
        return
    
    if new_stack == current:
        print(f"\n✓ Already running {mode_name}")
        return
    
    print(f"\n⚙️  Switching to {mode_name}...")
    
    if switch_stack(new_stack):
        print(f"✅ SUCCESS! Stack switched to {mode_name}")
        print("\n⚠️  IMPORTANT: Restart any running Monolith services for changes to take effect.")
        print("   Run: python -m streamlit run System\\UI\\monolith_ui.py")
    else:
        print("❌ Failed to switch stack!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Exiting...")
        sys.exit(0)
