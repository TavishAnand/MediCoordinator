"""
Clinical Agent - Patient Safety & Drug Interaction Checker
Validates treatments, checks drug interactions, ensures protocols
"""

import os
from dotenv import load_dotenv
from openai import OpenAI
from typing import Dict, List, Any

load_dotenv()

class ClinicalAgent:
    """
    Ensures patient safety and clinical protocols
    """
    
    def __init__(self):
        """Initialize with Perplexity API"""
        api_key = os.getenv('PERPLEXITY_API_KEY')
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.perplexity.ai"
        )
        
        # Mock patient database
        self.patients = {
            "patient_123": {
                "name": "Jane Doe",
                "age": 32,
                "allergies": [],
                "current_medications": [],
                "conditions": ["pregnancy"]
            }
        }
    
    def check_safety(self, patient_id: str, proposed_treatment: str) -> Dict[str, Any]:
        """
        Check patient safety for proposed treatment
        
        Args:
            patient_id: Patient identifier
            proposed_treatment: Treatment to validate
            
        Returns:
            Safety analysis and recommendations
        """
        
        patient = self.patients.get(patient_id, {})
        
        messages = [
            {
                "role": "system",
                "content": """You are a clinical safety officer.
Analyze proposed treatments for safety issues:
1. Drug interactions
2. Contraindications
3. Allergy risks
4. Protocol compliance

Respond in format:
SAFETY_STATUS: [SAFE/CAUTION/UNSAFE]
INTERACTIONS: [any drug interactions]
CONTRAINDICATIONS: [any issues]
RECOMMENDATIONS: [clinical guidance]"""
            },
            {
                "role": "user",
                "content": f"""Patient: {patient.get('name', 'Unknown')}
Age: {patient.get('age', 'Unknown')}
Allergies: {', '.join(patient.get('allergies', ['None']))}
Current medications: {', '.join(patient.get('current_medications', ['None']))}
Conditions: {', '.join(patient.get('conditions', ['None']))}

Proposed treatment: {proposed_treatment}"""
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
                "patient_id": patient_id,
                "treatment": proposed_treatment,
                "analysis": analysis
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "status": "error"
            }
    
    def execute(self, patient_id: str, task: str) -> Dict[str, Any]:
        """
        Main execution method
        """
        print(f"\n🏥 CLINICAL AGENT: Checking patient safety...")
        print(f"Task: {task}\n")
        
        result = self.check_safety(patient_id, task)
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
            return result
        
        print(f"✅ Safety check complete!")
        print(f"\nAnalysis:\n{result['analysis']}\n")
        
        return result


# Test function
def test_clinical_agent():
    """Test the clinical agent"""
    
    agent = ClinicalAgent()
    
    print("="*60)
    print("TEST: Emergency C-Section Safety Check")
    print("="*60)
    
    result = agent.execute(
        "patient_123",
        "Emergency C-section with general anesthesia (Propofol)"
    )
    
    return result


if __name__ == "__main__":
    print("🏥 MediCoordinator - Clinical Agent\n")
    test_clinical_agent()
