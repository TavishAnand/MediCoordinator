"""
Orchestrator Agent - The Decision Maker
Uses Perplexity API for intelligent coordination
"""

import os
from dotenv import load_dotenv
from openai import OpenAI
from typing import Dict, List, Any

load_dotenv()

class OrchestratorAgent:
    """
    Main coordinator using Perplexity API
    """
    
    def __init__(self):
        """Initialize with Perplexity API"""
        api_key = os.getenv('PERPLEXITY_API_KEY')
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.perplexity.ai"
        )
        
    def analyze_request(self, request: str) -> Dict[str, Any]:
        """
        Analyze incoming request and determine which agents to activate
        
        Args:
            request: User request string
            
        Returns:
            Dictionary with analysis and agent routing decisions
        """
        
        messages = [
            {
                "role": "system",
                "content": """You are a hospital coordination system orchestrator.
Analyze requests and determine which agents should be activated:

Available agents:
1. supply_chain_agent - Handles inventory, supplies, equipment
2. clinical_agent - Handles patient safety, drug interactions, protocols
3. discharge_agent - Handles patient discharge planning

Respond in this exact format:
AGENTS_NEEDED: [comma-separated list]
PRIORITY: [HIGH/MEDIUM/LOW]
REASONING: [brief explanation]"""
            },
            {
                "role": "user",
                "content": f"Request: {request}"
            }
        ]
        
        try:
            response = self.client.chat.completions.create(
                model="sonar-pro",
                messages=messages,
                max_tokens=500
            )
            
            analysis = response.choices[0].message.content
            
            # Parse response
            agents_needed = []
            if "supply_chain" in analysis.lower():
                agents_needed.append("supply_chain_agent")
            if "clinical" in analysis.lower():
                agents_needed.append("clinical_agent")
            if "discharge" in analysis.lower():
                agents_needed.append("discharge_agent")
                
            priority = "HIGH" if "HIGH" in analysis else "MEDIUM"
            
            return {
                "agents_needed": agents_needed,
                "priority": priority,
                "analysis": analysis,
                "original_request": request
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "agents_needed": [],
                "priority": "UNKNOWN"
            }
    
    def coordinate(self, request: str) -> Dict[str, Any]:
        """
        Main coordination method
        """
        print(f"\n🎯 ORCHESTRATOR: Analyzing request...")
        print(f"Request: {request}\n")
        
        # Analyze request
        analysis = self.analyze_request(request)
        
        if "error" in analysis:
            print(f"❌ Error: {analysis['error']}")
            return analysis
        
        # Display analysis
        print(f"✅ Analysis complete!")
        print(f"Priority: {analysis['priority']}")
        print(f"Agents needed: {', '.join(analysis['agents_needed'])}")
        print(f"\nReasoning:\n{analysis['analysis']}\n")
        
        return analysis


# Test function
def test_orchestrator():
    """Test the orchestrator"""
    
    orchestrator = OrchestratorAgent()
    
    print("="*60)
    print("TEST 1: Emergency Surgery Request")
    print("="*60)
    
    result1 = orchestrator.coordinate(
        "Emergency C-section needed in OR-3. Check supplies and verify patient safety."
    )
    
    print("\n" + "="*60)
    print("TEST 2: Patient Discharge")
    print("="*60)
    
    result2 = orchestrator.coordinate(
        "Patient in room 302 ready for discharge tomorrow. Arrange home care."
    )
    
    return result1, result2


if __name__ == "__main__":
    print("🏥 MediCoordinator - Orchestrator Agent (Perplexity API)\n")
    test_orchestrator()
