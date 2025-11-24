"""
Real-time Metrics Tracker & Cost Calculator
Tracks performance and calculates ROI
"""

import time
from datetime import datetime
from typing import Dict, List, Any
import json

class MetricsTracker:
    """
    Tracks all system metrics and calculates cost savings
    """
    
    def __init__(self):
        self.requests = []
        self.start_time = time.time()
        
        # Cost assumptions (industry averages)
        self.MANUAL_SURGERY_PREP_TIME = 35  # minutes
        self.MANUAL_SAFETY_CHECK_TIME = 12  # minutes
        self.MANUAL_DISCHARGE_PLAN_TIME = 120  # minutes
        self.CLINICAL_STAFF_COST_PER_HOUR = 85  # USD
        self.ADMIN_STAFF_COST_PER_HOUR = 45  # USD
        
    def log_request(self, request_type: str, agents_used: List[str], 
                    response_time: float, status: str):
        """Log a request with all metrics"""
        
        request_data = {
            "timestamp": datetime.now().isoformat(),
            "request_type": request_type,
            "agents_used": agents_used,
            "response_time": response_time,
            "status": status,
            "time_saved": self._calculate_time_saved(agents_used),
            "cost_saved": self._calculate_cost_saved(agents_used)
        }
        
        self.requests.append(request_data)
        return request_data
    
    def _calculate_time_saved(self, agents_used: List[str]) -> float:
        """Calculate time saved in minutes"""
        
        time_saved = 0
        
        if "supply_chain_agent" in agents_used:
            time_saved += self.MANUAL_SURGERY_PREP_TIME
        
        if "clinical_agent" in agents_used:
            time_saved += self.MANUAL_SAFETY_CHECK_TIME
        
        if "discharge_agent" in agents_used:
            time_saved += self.MANUAL_DISCHARGE_PLAN_TIME
        
        return time_saved
    
    def _calculate_cost_saved(self, agents_used: List[str]) -> float:
        """Calculate cost saved in USD"""
        
        time_saved_hours = self._calculate_time_saved(agents_used) / 60
        
        # Mix of clinical and admin staff costs
        avg_cost = (self.CLINICAL_STAFF_COST_PER_HOUR + 
                   self.ADMIN_STAFF_COST_PER_HOUR) / 2
        
        return time_saved_hours * avg_cost
    
    def get_summary_stats(self) -> Dict[str, Any]:
        """Get summary statistics"""
        
        if not self.requests:
            return {
                "total_requests": 0,
                "avg_response_time": 0,
                "total_time_saved_hours": 0,
                "total_cost_saved": 0,
                "uptime_hours": 0
            }
        
        total_time_saved = sum(r["time_saved"] for r in self.requests)
        total_cost_saved = sum(r["cost_saved"] for r in self.requests)
        avg_response_time = sum(r["response_time"] for r in self.requests) / len(self.requests)
        
        uptime = (time.time() - self.start_time) / 3600  # hours
        
        return {
            "total_requests": len(self.requests),
            "avg_response_time": round(avg_response_time, 2),
            "total_time_saved_hours": round(total_time_saved / 60, 2),
            "total_cost_saved": round(total_cost_saved, 2),
            "daily_cost_saved": round(total_cost_saved * (24 / uptime) if uptime > 0 else 0, 2),
            "annual_projection": round(total_cost_saved * (8760 / uptime) if uptime > 0 else 0, 2),
            "uptime_hours": round(uptime, 2)
        }
    
    def get_recent_requests(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get most recent requests"""
        return self.requests[-limit:]


# Global tracker instance
tracker = MetricsTracker()
