"""
🏴 PROJECT MONOLITH: DUAL-STACK CONFIGURATION
This file controls which operational stack is active.
"""

import os
from typing import Literal


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ============================================
# OPERATION MODE
# ============================================
# Set to TRUE to use mock data (safe for testing)
# Set to FALSE to use real money/APIs (PRODUCTION)
USE_SIMULATION_MODE = True

ACTIVE_STACK: Literal["LOCAL", "CLOUD"] = "LOCAL"

# ============================================
# STACK A: FORTRESS (LOCAL)
# ============================================

LOCAL_CONFIG = {
    "mode": "FORTRESS",
    "llm_endpoint": "http://localhost:11434",  # Ollama
    "llm_model": "llama3",
    "image_endpoint": "http://localhost:7860",  # Stable Diffusion Automatic1111
    "image_model": "sdxl",
    "db_uri": "postgresql://monolith:fortress@localhost:5432/monolith",
    "redis_uri": "redis://localhost:6379",
    "vector_db": "chromadb",
    "vector_db_path": os.path.join(BASE_DIR, "Data", "ChromaDB"),
    "observability": "loki",
    "workflow_engine": "n8n-local",
    "rpa_tools": ["moltbot", "autohotkey"],
    "internet_required": False,
    "cost_per_request": 0.0,
    "privacy_level": "MAXIMUM",
}

# ============================================
# STACK B: CLOUD (GOD MODE)
# ============================================

CLOUD_CONFIG = {
    "mode": "GOD_MODE",
    "llm_endpoint": "https://api.openai.com/v1",
    "llm_model": "gpt-4o",  # or gpt-5 when available
    "llm_api_key": os.getenv("OPENAI_API_KEY"),
    "claude_endpoint": "https://api.anthropic.com/v1",
    "claude_model": "claude-4-opus",
    "claude_api_key": os.getenv("ANTHROPIC_API_KEY"),
    "groq_endpoint": "https://api.groq.com/openai/v1",
    "groq_model": "llama3-70b-8192",
    "groq_api_key": os.getenv("GROQ_API_KEY"),
    "image_endpoint": "https://api.midjourney.com",
    "image_api_key": os.getenv("MIDJOURNEY_API_KEY"),
    "db_uri": os.getenv("SUPABASE_URL"),
    "redis_uri": os.getenv("REDIS_CLOUD_URL"),
    "vector_db": "pinecone",
    "vector_db_api_key": os.getenv("PINECONE_API_KEY"),
    "observability": "elk",
    "workflow_engine": "n8n-cloud",
    "rpa_tools": ["moltbot"],
    "payment_stripe_key": os.getenv("STRIPE_API_KEY"),
    "payment_paypal_key": os.getenv("PAYPAL_API_KEY"),
    "crypto_wallet": os.getenv("METAMASK_PRIVATE_KEY"),
    "internet_required": True,
    "cost_per_request": 0.01,  # Estimated
    "privacy_level": "API_DEPENDENT",
}

# ============================================
# ACTIVE CONFIGURATION
# ============================================

if ACTIVE_STACK == "LOCAL":
    CONFIG = LOCAL_CONFIG
    print("🔒 FORTRESS MODE ACTIVATED")
    print("   Privacy: MAXIMUM | Cost: $0 | Internet: NOT REQUIRED")
elif ACTIVE_STACK == "CLOUD":
    CONFIG = CLOUD_CONFIG
    print("☁️ GOD MODE ACTIVATED")
    print("   Intelligence: MAXIMUM | Speed: ULTRA | Internet: REQUIRED")
else:
    raise ValueError(f"Invalid ACTIVE_STACK: {ACTIVE_STACK}. Must be 'LOCAL' or 'CLOUD'")

# ============================================
# CONVENIENCE ACCESSORS
# ============================================

def get_llm_endpoint():
    """Get the active LLM endpoint"""
    return CONFIG["llm_endpoint"]

def get_llm_model():
    """Get the active LLM model"""
    return CONFIG["llm_model"]

def get_image_endpoint():
    """Get the active image generation endpoint"""
    return CONFIG["image_endpoint"]

def get_db_uri():
    """Get the active database URI"""
    return CONFIG["db_uri"]

def is_local_mode():
    """Check if running in local/fortress mode"""
    return ACTIVE_STACK == "LOCAL"

def is_cloud_mode():
    """Check if running in cloud/god mode"""
    return ACTIVE_STACK == "CLOUD"

def get_mode_name():
    """Get the human-readable mode name"""
    return CONFIG["mode"]

# ============================================
# SYSTEM INFO
# ============================================

def print_system_info():
    """Print current system configuration"""
    print("\n" + "="*50)
    print("🏴 PROJECT MONOLITH: SYSTEM CONFIGURATION")
    print("="*50)
    print(f"Active Stack: {ACTIVE_STACK}")
    print(f"Mode: {CONFIG['mode']}")
    print(f"LLM: {CONFIG['llm_model']}")
    print(f"Privacy: {CONFIG['privacy_level']}")
    print(f"Internet Required: {CONFIG['internet_required']}")
    print(f"Cost/Request: ${CONFIG['cost_per_request']}")
    print("="*50 + "\n")

if __name__ == "__main__":
    print_system_info()
