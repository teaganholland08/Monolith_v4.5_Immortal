"""
MONOLITH REVENUE BRIDGE - Gumroad Integration
Automatically publishes Genesis Engine output to Gumroad marketplace

Revenue Flow:
1. Genesis creates Python script/guide
2. System uploads to Gumroad
3. Product listed at $X.XX
4. Sales deposit to YOUR bank account (2-5 days)
5. Track revenue in ledger.db

Setup:
1. Create Gumroad account at gumroad.com
2. Go to Settings > Advanced > Create Application
3. Get Access Token
4. Set environment variable: GUMROAD_ACCESS_TOKEN
"""

import requests
import os
from pathlib import Path
from datetime import datetime

class GumroadBridge:
    def __init__(self):
        self.access_token = os.getenv("GUMROAD_ACCESS_TOKEN", "")
        self.base_url = "https://api.gumroad.com/v2"
        
    def is_configured(self):
        """Check if API credentials are set"""
        return bool(self.access_token)
    
    def create_product(self, file_path, name, description, price=9.99):
        """
        Upload file to Gumroad as digital product
        
        Args:
            file_path: Absolute path to file
            name: Product name (shown to buyers)
            description: Product description
            price: Price in USD (min $0.99)
        
        Returns:
            dict with product_id, url, status
        """
        if not self.is_configured():
            return {
                "status": "ERROR",
                "message": "GUMROAD_ACCESS_TOKEN not set in environment"
            }
        
        try:
            # Step 1: Create product listing
            product_data = {
                "name": name,
                "description": description,
                "price": int(price * 100),  # Gumroad uses cents
                "published": True
            }
            
            headers = {
                "Authorization": f"Bearer {self.access_token}"
            }
            
            response = requests.post(
                f"{self.base_url}/products",
                headers=headers,
                data=product_data,
                timeout=30
            )
            
            if response.status_code != 200:
                return {
                    "status": "ERROR",
                    "message": f"Gumroad API error: {response.text}"
                }
            
            product = response.json().get("product", {})
            product_id = product.get("id")
            product_url = product.get("short_url")
            
            # Step 2: Upload file to product
            with open(file_path, 'rb') as f:
                files = {'file': f}
                upload_response = requests.post(
                    f"{self.base_url}/products/{product_id}/upload",
                    headers=headers,
                    files=files,
                    timeout=60
                )
            
            return {
                "status": "SUCCESS",
                "product_id": product_id,
                "url": product_url,
                "price": price,
                "message": f"Product live at {product_url}"
            }
            
        except Exception as e:
            return {
                "status": "ERROR",
                "message": str(e)
            }
    
    def list_products(self):
        """Get all your Gumroad products"""
        if not self.is_configured():
            return []
        
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = requests.get(
                f"{self.base_url}/products",
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json().get("products", [])
            return []
        except:
            return []
    
    def get_sales(self):
        """Fetch recent sales data"""
        if not self.is_configured():
            return []
        
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = requests.get(
                f"{self.base_url}/sales",
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json().get("sales", [])
            return []
        except:
            return []
    
    def auto_publish_genesis_output(self, genesis_file_path):
        """
        Automatically publish Genesis Engine output
        
        Naming convention:
        - agent_bitcoin_tracker.py -> "Bitcoin Tracker Agent" ($14.99)
        - guide_tax_optimization.md -> "Tax Optimization Guide" ($9.99)
        """
        file_path = Path(genesis_file_path)
        
        if not file_path.exists():
            return {"status": "ERROR", "message": "File not found"}
        
        # Generate product name from filename
        base_name = file_path.stem.replace("_", " ").title()
        
        # Determine price based on file type
        if file_path.suffix == ".py":
            price = 14.99
            description = f"Automated Python script: {base_name}. Professionally generated code ready to use."
        elif file_path.suffix == ".md":
            price = 9.99
            description = f"Comprehensive guide: {base_name}. Expert-level information and strategies."
        else:
            price = 4.99
            description = f"Digital asset: {base_name}"
        
        # Create product
        result = self.create_product(
            file_path=str(file_path),
            name=base_name,
            description=description,
            price=price
        )
        
        # Log to ledger if successful
        if result.get("status") == "SUCCESS":
            self._log_product(base_name, price, result.get("url"))
        
        return result
    
    def _log_product(self, name, price, url):
        """Log product creation to ledger"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "product": name,
            "price": price,
            "url": url,
            "status": "LISTED"
        }
        
        # Append to products log
        log_file = Path(__file__).parent.parent / "Logs" / "gumroad_products.log"
        log_file.parent.mkdir(exist_ok=True)
        
        with open(log_file, 'a') as f:
            f.write(f"{log_entry}\n")
    
    def calculate_revenue(self):
        """Calculate total revenue from Gumroad sales"""
        sales = self.get_sales()
        
        total = sum(float(sale.get("price", 0)) / 100 for sale in sales)
        count = len(sales)
        
        return {
            "total_revenue": total,
            "sales_count": count,
            "avg_sale": total / count if count > 0 else 0
        }

if __name__ == "__main__":
    bridge = GumroadBridge()
    
    if not bridge.is_configured():
        print("⚠️ GUMROAD SETUP REQUIRED")
        print("\n1. Go to: https://gumroad.com/settings/advanced")
        print("2. Create Application > Get Access Token")
        print("3. Set environment variable:")
        print('   setx GUMROAD_ACCESS_TOKEN "your_token_here"')
        print("\nThen restart terminal and run again.")
    else:
        print("✓ Gumroad configured")
        
        # Show stats
        products = bridge.list_products()
        revenue = bridge.calculate_revenue()
        
        print(f"\nProducts listed: {len(products)}")
        print(f"Total sales: {revenue['sales_count']}")
        print(f"Revenue: ${revenue['total_revenue']:.2f}")
