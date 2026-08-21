from typing import Dict, List


def recommend_fertilizer(crop: str, N: float, P: float, K: float, ph: float) -> Dict[str, List[str]]:
    """Return recommended fertilizers and a short explanation based on soil values."""
    crop = crop.lower().strip()
    fertilizers: List[str] = []
    reasons: List[str] = []

    if N < 40:
        fertilizers.append("Urea")
        reasons.append("Low nitrogen suggests a nitrogen-rich fertilizer.")
    if P < 40:
        fertilizers.append("DAP")
        reasons.append("Low phosphorus benefits from DAP or superphosphate.")
    if K < 40:
        fertilizers.append("Muriate of Potash (MOP)")
        reasons.append("Low potassium is improved with potash.")
    if ph < 6.0:
        fertilizers.append("Dolomite Lime")
        reasons.append("Acidic soil will benefit from lime to raise pH.")
    if ph > 7.8:
        fertilizers.append("Elemental Sulfur")
        reasons.append("Alkaline soil may improve with sulfur treatment.")

    crop_specific = {
        "rice": "NPK 16-16-8",
        "maize": "NPK 20-10-10",
        "wheat": "NPK 19-19-19",
        "cotton": "NPK 10-26-26",
        "sugarcane": "NPK 20-10-10",
    }

    if crop in crop_specific:
        fertilizers.insert(0, crop_specific[crop])
        reasons.insert(0, f"Crop-specific blend for {crop.title()}.")

    if not fertilizers:
        fertilizers = ["Balanced NPK blend", "Organic compost"]
        reasons.append("Soil nutrients are balanced, so a maintenance blend is best.")

    fertilizers = list(dict.fromkeys(fertilizers))
    return {"fertilizers": fertilizers, "reasons": reasons}


def analyze_soil(n: float, p: float, k: float, ph: float) -> dict:
    """Categorize N, P, K values as 'low', 'medium', or 'high', and pH as 'acidic', 'neutral', or 'alkaline'."""
    # Nitrogen (N) heuristics
    if n < 50:
        n_status = "low"
    elif n <= 100:
        n_status = "medium"
    else:
        n_status = "high"

    # Phosphorus (P) heuristics
    if p < 40:
        p_status = "low"
    elif p <= 80:
        p_status = "medium"
    else:
        p_status = "high"

    # Potassium (K) heuristics
    if k < 40:
        k_status = "low"
    elif k <= 80:
        k_status = "medium"
    else:
        k_status = "high"

    # pH heuristics
    if ph < 6.0:
        ph_status = "acidic"
    elif ph <= 7.5:
        ph_status = "neutral"
    else:
        ph_status = "alkaline"

    return {
        "nitrogen": n_status,
        "phosphorus": p_status,
        "potassium": k_status,
        "ph": ph_status
    }


def get_fertilizer_suggestion(soil_analysis: dict) -> dict:
    """Generate general fertilizer suggestions based on soil nutrient categorization and pH."""
    suggestions: List[str] = []
    
    n_status = soil_analysis.get("nitrogen")
    p_status = soil_analysis.get("phosphorus")
    k_status = soil_analysis.get("potassium")
    ph_status = soil_analysis.get("ph")

    if n_status == "low":
        suggestions.append("Consider adding nitrogen-rich organic matter or nitrogen-based fertilizers to improve soil vigor.")
    elif n_status == "high":
        suggestions.append("Nitrogen levels are high. Avoid excess nitrogen application to prevent leggy growth or run-off.")

    if p_status == "low":
        suggestions.append("Apply a phosphorus supplement or bone meal to support strong root establishment and flowering.")

    if k_status == "low":
        suggestions.append("Consider applying potassium-based inputs (like potash) to boost overall plant disease resistance and water regulation.")

    if ph_status == "acidic":
        suggestions.append("Soil is acidic. Liming (dolomite or agricultural lime) may be used to raise the pH if the target crop requires neutral conditions.")
    elif ph_status == "alkaline":
        suggestions.append("Soil is alkaline. Adding organic matter or sulfur-based amendments can help gradually lower the pH.")

    if not suggestions:
        suggestions.append("Nutrient levels appear balanced. Maintain soil quality with routine compost or balanced organic maintenance blends.")

    return {
        "suggestions": suggestions,
        "disclaimer": "These are general heuristics. Please consult a local agricultural expert before applying fertilizers."
    }
