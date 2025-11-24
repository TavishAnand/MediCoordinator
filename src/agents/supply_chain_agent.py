"""
Supply Chain Agent - Inventory & Equipment Manager
Monitors supplies, predicts shortages, manages orders
"""

import os
from dotenv import load_dotenv
from openai import OpenAI
from typing import Dict, List, Any

load_dotenv()

class SupplyChainAgent:
    """
    Manages hospital inventory and supply chain
    """
    
    def __init__(self):
        """Initialize with Perplexity API"""
        api_key = os.getenv('PERPLEXITY_API_KEY')
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.perplexity.ai"
        )
        
        # Mock inventory database
        self.inventory = {
            "blood_o_positive": 50,
            "blood_ab_negative": 12,
            "surgical_gloves": 1000,
            "anesthesia_propofol": 100,
            "sterile_instruments": 50,
            "iv_fluids": 200
        }
    
    def check_supplies(self, required_items: List[str]) -> Dict[str, Any]:
        """
        Check if required supplies are available
        
        Args:
            required_items: List of items needed
            
        Returns:
            Availability status and recommendations
        """
        
        messages = [
            {
                "role": "system",
                "content": """You are a hospital supply chain analyst.
Given a list of required items and current inventory, determine:
1. If supplies are sufficient
2. What's missing or low
3. Recommendations for ordering

Respond in format:
STATUS: [SUFFICIENT/INSUFFICIENT/CRITICAL]
AVAILABLE: [list items with OK stock]
LOW_STOCK: [list items running low]
MISSING: [list unavailable items]
RECOMMENDATIONS: [brief action items]"""
            },
            {
                "role": "user",
                "content": f"""Required items: {', '.join(required_items)}
                
Current inventory:
{self._format_inventory()}"""
            }
        ]
        
        try:
            response = self.client.chat.completions.create(
                model="sonar-pro",
                messages=messages,
                max_tokens=400
            )
            
            analysis = response.choices[0].message.content
            
            return {
                "status": "analyzed",
                "required_items": required_items,
                "current_inventory": self.inventory,
                "analysis": analysis
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "status": "error"
            }
    
    def _format_inventory(self) -> str:
        """Format inventory for display"""
        return "\n".join([f"- {item}: {qty} units" 
                         for item, qty in self.inventory.items()])
    
    def execute(self, task: str, required_items: List[str] = None) -> Dict[str, Any]:
        """
        Main execution method
        """
        print(f"\n📦 SUPPLY CHAIN AGENT: Checking supplies...")
        print(f"Task: {task}\n")
        
        if required_items is None:
            required_items = ["blood_o_positive", "surgical_gloves", "anesthesia_propofol"]
        
        result = self.check_supplies(required_items)
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
            return result
        
        print(f"✅ Supply check complete!")
        print(f"\nAnalysis:\n{result['analysis']}\n")
        
        return result


# Test function
def test_supply_chain_agent():
    """Test the supply chain agent"""
    
    agent = SupplyChainAgent()
    
    print("="*60)
    print("TEST: Emergency Surgery Supply Check")
    print("="*60)
    
    result = agent.execute(
        "Emergency C-section - check critical supplies",
        required_items=["blood_o_positive", "anesthesia_propofol", "sterile_instruments"]
    )
    
    return result


if __name__ == "__main__":
    print("🏥 MediCoordinator - Supply Chain Agent\n")
    test_supply_chain_agent()
