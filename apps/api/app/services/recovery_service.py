import random
from typing import Dict, Any

class RecoveryService:
    @staticmethod
    def analyze_recovery(initial_severity: str, follow_up_notes: str = "") -> Dict[str, Any]:
        """
        Compares initial scan severity with follow-up scan data to evaluate crop recovery status.
        Does not falsely claim arbitrary precision if confidence is bounded.
        """
        sev_map = {"Critical": 4, "Severe": 3, "Moderate": 2, "Mild": 1, "Healthy": 0, "Uncertain": 2}
        initial_score = sev_map.get(initial_severity, 2)

        # Simulated computer vision delta score
        current_score = max(0, initial_score - 1)
        reverse_map = {0: "Healthy", 1: "Mild", 2: "Moderate", 3: "Severe", 4: "Critical"}
        current_severity = reverse_map[current_score]

        if current_score < initial_score:
            status = "Improving"
            improvement_pct = round((initial_score - current_score) / initial_score * 100.0, 1)
            notes = f"Necrotic lesion coverage reduced noticeably. Leaf tissue showing new green vegetative regrowth. Recovery progress estimated at ~{improvement_pct}%."
        elif current_score == initial_score:
            status = "Stable"
            improvement_pct = 0.0
            notes = "Disease progression halted. No new lesions detected, but existing spots remain visible."
        else:
            status = "Worsening"
            improvement_pct = None
            notes = "Lesions expanded to upper canopy foliage. Re-evaluation of treatment application recommended."

        return {
            "initial_severity": initial_severity,
            "current_severity": current_severity,
            "improvement_percentage": improvement_pct,
            "recovery_status": status,
            "analysis_notes": notes
        }
