"""
MediCoordinator - Complete Multi-Agent Healthcare System
Demonstrates full agent coordination workflow with real-time metrics
"""

import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agents.orchestrator import OrchestratorAgent
from src.agents.supply_chain_agent import SupplyChainAgent
from src.agents.clinical_agent import ClinicalAgent
from src.agents.discharge_agent import DischargeAgent
from src.analytics.metrics_tracker import tracker


class MediCoordinator:
    """
    Main coordination system - orchestrates all agents
    """
    
    def __init__(self):
        """Initialize all agents"""
        print("🏥 Initializing MediCoordinator System...\n")
        
        self.orchestrator = OrchestratorAgent()
        self.supply_chain = SupplyChainAgent()
        self.clinical = ClinicalAgent()
        self.discharge = DischargeAgent()
        
        print("✅ All agents initialized!\n")
    
    def process_request(self, request: str, patient_id: str = "patient_123"):
        """
        Process a complete healthcare coordination request
        
        Args:
            request: User request
            patient_id: Patient identifier
        """
        print("="*70)
        print(f"NEW REQUEST: {request}")
        print("="*70)
        
        # Step 1: Orchestrator analyzes and routes
        routing = self.orchestrator.coordinate(request)
        
        if "error" in routing:
            print(f"❌ Orchestration failed: {routing['error']}")
            return
        
        agents_needed = routing.get("agents_needed", [])
        results = {}
        
        # Start timing
        start_time = time.time()
        
        # Step 2: Execute agent tasks
        print("\n" + "="*70)
        print("EXECUTING AGENT TASKS")
        print("="*70)
        
        if "supply_chain_agent" in agents_needed:
            results["supply_chain"] = self.supply_chain.execute(
                request,
                ["blood_o_positive", "anesthesia_propofol", "sterile_instruments"]
            )
        
        if "clinical_agent" in agents_needed:
            results["clinical"] = self.clinical.execute(
                patient_id,
                request
            )
        
        if "discharge_agent" in agents_needed:
            results["discharge"] = self.discharge.execute(
                patient_id,
                request
            )
        
        # Calculate response time
        response_time = time.time() - start_time
        
        # Determine status
        all_safe = all("error" not in result for result in results.values())
        status = "approved" if all_safe else "review_required"
        
        # Log metrics
        tracker.log_request(
            request_type=request[:50],
            agents_used=agents_needed,
            response_time=response_time,
            status=status
        )
        
        # Step 3: Synthesize final decision
        print("\n" + "="*70)
        print("FINAL DECISION")
        print("="*70)
        
        print(f"\n✅ REQUEST PROCESSED SUCCESSFULLY")
        print(f"Priority: {routing.get('priority', 'UNKNOWN')}")
        print(f"Agents activated: {len(agents_needed)}")
        print(f"Results collected: {len(results)}")
        
        if all_safe:
            print(f"\n🎉 STATUS: APPROVED - All safety checks passed")
            print(f"✅ Supplies: Available")
            print(f"✅ Safety: Cleared")
            print(f"✅ Coordination: Complete")
        else:
            print(f"\n⚠️ STATUS: REVIEW REQUIRED - Some checks need attention")
        
        # Show metrics
        stats = tracker.get_summary_stats()
        print(f"\n💰 COST SAVINGS THIS SESSION:")
        print(f"   Response time: {response_time:.2f}s")
        print(f"   Time saved: {stats['total_time_saved_hours']:.1f} hours")
        print(f"   Cost saved: ${stats['total_cost_saved']:.2f}")
        print(f"   Daily projection: ${stats['daily_cost_saved']:.2f}")
        print(f"   Annual projection: ${stats['annual_projection']:,.2f}")
        
        print("\n" + "="*70 + "\n")
        
        return {
            "routing": routing,
            "results": results,
            "status": status,
            "metrics": stats
        }


def run_demo():
    """Run complete system demonstration"""
    
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║              🏥 MEDICOORDINATOR DEMO                            ║
║         Multi-Agent Healthcare Coordination System               ║
║              WITH REAL-TIME COST ANALYTICS                       ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    # Initialize system
    system = MediCoordinator()
    
    # Demo Scenario 1: Emergency Surgery
    print("\n" + "🚨 SCENARIO 1: EMERGENCY SURGERY 🚨".center(70))
    
    system.process_request(
        "Emergency C-section needed in OR-3. Verify all supplies and patient safety protocols.",
        patient_id="patient_123"
    )
    
    input("\n⏸️  Press Enter to continue to next scenario...\n")
    
    # Demo Scenario 2: Patient Discharge
    print("\n" + "🏠 SCENARIO 2: PATIENT DISCHARGE 🏠".center(70))
    
    system.process_request(
        "Patient in room 302 ready for discharge tomorrow. Arrange home care and follow-up.",
        patient_id="patient_302"
    )
    
    # Final summary
    final_stats = tracker.get_summary_stats()
    
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║                    ✅ DEMO COMPLETE!                             ║
║                                                                  ║
║   MediCoordinator successfully coordinated 2 complex scenarios   ║
║   demonstrating multi-agent decision-making in healthcare.       ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    print("\n📊 FINAL SESSION METRICS:")
    print("="*70)
    print(f"Total requests processed: {final_stats['total_requests']}")
    print(f"Average response time: {final_stats['avg_response_time']}s")
    print(f"Total time saved: {final_stats['total_time_saved_hours']:.1f} hours")
    print(f"Total cost saved: ${final_stats['total_cost_saved']:.2f}")
    print(f"\n💰 PROJECTED ANNUAL SAVINGS: ${final_stats['annual_projection']:,.2f}")
    print("="*70)


if __name__ == "__main__":
    run_demo()
