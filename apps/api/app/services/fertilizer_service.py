from typing import Dict, Any

class FertilizerService:
    @staticmethod
    def calculate(crop_name: str, area_acres: float, soil_n_ppm: float = 20.0, soil_p_ppm: float = 10.0, soil_k_ppm: float = 150.0) -> Dict[str, Any]:
        """
        Rule-based N-P-K fertilizer requirement calculator based on standardized agricultural extension formulas.
        Recommended dose of fertilizer (RDF) per acre:
        - Rice: N:P:K = 50:20:20 kg/acre
        - Tomato: N:P:K = 60:40:40 kg/acre
        - Maize/Corn: N:P:K = 50:25:25 kg/acre
        - Default: N:P:K = 40:20:20 kg/acre
        """
        crop_lower = crop_name.lower()
        if "rice" in crop_lower or "paddy" in crop_lower:
            target_n, target_p, target_k = 50.0, 20.0, 20.0
        elif "tomato" in crop_lower or "chilli" in crop_lower:
            target_n, target_p, target_k = 60.0, 40.0, 40.0
        elif "corn" in crop_lower or "maize" in crop_lower:
            target_n, target_p, target_k = 50.0, 25.0, 25.0
        else:
            target_n, target_p, target_k = 40.0, 20.0, 20.0

        # Adjust based on soil test values (standard soil credit algorithm)
        n_req = max(10.0, (target_n - (soil_n_ppm * 0.5)) * area_acres)
        p_req = max(5.0, (target_p - (soil_p_ppm * 0.4)) * area_acres)
        k_req = max(5.0, (target_k - (soil_k_ppm * 0.1)) * area_acres)

        # Convert nutrient requirements to standard commercial fertilizer bags/weight
        # Urea = 46% N
        # DAP (Di-ammonium Phosphate) = 18% N, 46% P2O5
        # MOP (Muriate of Potash) = 60% K2O
        dap_kg = round(p_req / 0.46, 1)
        n_from_dap = dap_kg * 0.18
        remaining_n = max(0.0, n_req - n_from_dap)
        urea_kg = round(remaining_n / 0.46, 1)
        mop_kg = round(k_req / 0.60, 1)
        compost_tons = round(2.5 * area_acres, 1)

        explanation = (
            f"Calculated using standard ICAR Nutrient Management Formula for {crop_name} across {area_acres} acre(s). "
            f"DAP provides the primary Phosphorus ({round(p_req,1)} kg P2O5) along with {round(n_from_dap,1)} kg elemental N. "
            f"The remaining N requirement ({round(remaining_n,1)} kg N) is fulfilled via Urea. "
            f"Potassium ({round(k_req,1)} kg K2O) is fulfilled via MOP."
        )

        return {
            "crop_name": crop_name,
            "area_acres": area_acres,
            "nitrogen_req_kg": round(n_req, 1),
            "phosphorus_req_kg": round(p_req, 1),
            "potassium_req_kg": round(k_req, 1),
            "recommended_urea_kg": urea_kg,
            "recommended_dap_kg": dap_kg,
            "recommended_mop_kg": mop_kg,
            "organic_compost_tons": compost_tons,
            "formula_explanation": explanation
        }
