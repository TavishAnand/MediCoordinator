"""
Discharge Agent - Patient Discharge Planning & Coordination
Plans discharge, arranges home care, coordinates follow-ups
"""

import os
from dotenv import load_dotenv
from openai import OpenAI
from typing import Dict, Any

load_dotenv()

class DischargeAgent:
    """
    Manages patient discharge planning
    """
    
    def __init__(self):
        """Initialize with Perplexity API"""
        api_key = os.getenv('PERPLEXITY_API_KEY')
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.perplexity.ai"
        )
    
    def create_discharge_plan(self, patient_id: str, condition: str) -> Dict[str, Any]:
        """Create comprehensive discharge plan"""
        
        messages = [
            {
                "role": "system",
                "content": """You are a discharge planning coordinator.
Create a comprehensive discharge plan including:
1. Home care arrangements
2. Medication instructions
3. Follow-up appointments
4. Warning signs to watch for

Respond in format:
HOME_CARE: [arrangements needed]
MEDICATIONS: [instructions]
FOLLOW_UP: [appointment schedule]
WARNING_SIGNS: [what to watch for]
TIMELINE: [discharge readiness]"""
            },
            {
                "role": "user",
                "content": f"Patient: {patient_id}\nCondition: {condition}\nCreate discharge plan."
            }
        ]
        
        try:
            response = self.client.chat.completions.create(
                model="sonar-pro",
                messages=messages,
                max_tokens=500
            )
            
            return {
                "status": "plan_created",
                "patient_id": patient_id,
                "plan": response.choices[0].message.content
            }
            
        except Exception as e:
            return {"error": str(e), "status": "error"}
    
    def execute(self, patient_id: str, task: str) -> Dict[str, Any]:
        """Main execution method"""
        print(f"\n🏠 DISCHARGE AGENT: Creating discharge plan...")
        print(f"Task: {task}\n")
        
        result = self.create_discharge_plan(patient_id, task)
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
            return result
        
        print(f"✅ Discharge plan created!")
        print(f"\nPlan:\n{result['plan']}\n")
        
        return result


def test_discharge_agent():
    """Test the discharge agent"""
    agent = DischargeAgent()
    
    print("="*60)
    print("TEST: Post-Surgery Discharge Planning")
    print("="*60)
    
    result = agent.execute(
        "patient_302",
        "Post C-section recovery, ready for discharge"
    )
    
    return result


if __name__ == "__main__":
    print("🏥 MediCoordinator - Discharge Agent\n")
    test_discharge_agent()
