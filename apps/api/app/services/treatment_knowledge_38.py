"""
Complete 38-Class Treatment & Guidance Knowledge Base for PlantVillage.
Provides grounded agricultural guidance for all 38 specific crop-condition classes.
Healthy classes receive "Plant appears healthy" with preventive/monitoring guidance.
"""

from typing import Dict, Any, Optional

TREATMENT_KNOWLEDGE_38: Dict[str, Dict[str, Any]] = {
    # 0. Apple Scab
    "Apple___Apple_scab": {
        "problem_title": "Apple Scab (Venturia inaequalis)",
        "why_happening": "Fungal infection caused by Venturia inaequalis. Primary infection occurs during spring rains when mature ascospores are released from overwintered leaf litter.",
        "immediate_action": "Rake and destroy infected fallen leaves. Prune infected twigs and foliage to improve sunlight penetration and air movement.",
        "cultural_control": "Plant scab-resistant apple cultivars (e.g., Liberty, Enterprise). Maintain wide tree canopy spacing and prune lower scaffold branches.",
        "biological_organic": "Foliar application of Liquid Sulfur spray @ 3-5g/L water or Neem Oil extract @ 5ml/L at green tip stage.",
        "approved_chemical": "Active Ingredient: Captan 50% WP @ 2.5g/L water OR Difenoconazole 25% EC @ 0.5ml/L water applied from pink bud stage. Pre-Harvest Interval (PHI): 14 days.",
        "safety_warning": "Observe 14-day Pre-Harvest Interval (PHI). Wear protective eye goggles, face mask, and gloves during spraying.",
        "follow_up_days": 7,
        "source_reference": "ICAR-CITH & TNAU Fruit Crop Protection Advisory"
    },
    # 1. Apple Black Rot
    "Apple___Black_rot": {
        "problem_title": "Apple Black Rot & Frog-Eye Leaf Spot (Botryosphaeria obtusa)",
        "why_happening": "Fungal disease caused by Botryosphaeria obtusa, entering through bark wounds, mummified fruit, or damaged leaf margins during humid weather.",
        "immediate_action": "Remove mummified fruits and dead/cankered wood immediately. Burn or deeply bury pruned orchard debris.",
        "cultural_control": "Avoid mechanical trunk injury during pruning. Keep canopy foliage dry by maintaining open orchard structure.",
        "biological_organic": "Apply Trichoderma harzianum bio-fungicide @ 5g/L or Bio-Copper foliar spray.",
        "approved_chemical": "Active Ingredient: Mancozeb 75% WP @ 2.0g/L water OR Thiophanate-Methyl 70% WP @ 1.0g/L water. Pre-Harvest Interval (PHI): 21 days.",
        "safety_warning": "Do not apply chemical sprays during bloom stage to protect honeybee pollinators.",
        "follow_up_days": 10,
        "source_reference": "University Agricultural Extension & ICAR Fruit Pathology Guidelines"
    },
    # 2. Apple Cedar Apple Rust
    "Apple___Cedar_apple_rust": {
        "problem_title": "Cedar Apple Rust (Gymnosporangium juniperi-virginianae)",
        "why_happening": "Heteroecious fungal rust requiring both apple trees and Eastern Red Cedar / Juniper hosts to complete its life cycle.",
        "immediate_action": "Inspect surrounding area for alternate cedar hosts and prune galls from nearby juniper trees within 500 meters if feasible.",
        "cultural_control": "Plant rust-resistant apple varieties (e.g., Freedom, Pristine). Maintain good orchard spacing.",
        "biological_organic": "Foliar application of Sulfur WP @ 3.0g/L water at early leaf expansion.",
        "approved_chemical": "Active Ingredient: Myclobutanil 10% WP @ 0.4g/L water OR Propiconazole 25% EC @ 1.0ml/L water. Pre-Harvest Interval (PHI): 14 days.",
        "safety_warning": "Adhere strictly to Pre-Harvest Interval (PHI) of 14 days before fruit harvesting.",
        "follow_up_days": 7,
        "source_reference": "Orchard Health Extension Bulletin"
    },
    # 3. Apple Healthy
    "Apple___healthy": {
        "problem_title": "Plant appears healthy",
        "why_happening": "Apple foliage shows excellent chlorophyll density, uniform green leaf blades, and no signs of fungal lesions or insect feeding.",
        "immediate_action": "Plant appears healthy. No curative disease treatment required.",
        "cultural_control": "Maintain balanced seasonal pruning, orchard floor weeding, and root-zone soil aeration.",
        "biological_organic": "Apply organic compost mulching around tree dripline to nourish beneficial soil microbes.",
        "approved_chemical": "No chemical pesticide treatment needed for healthy crop foliage.",
        "safety_warning": "Avoid unnecessary chemical applications to protect natural predator insects in the orchard.",
        "follow_up_days": 14,
        "source_reference": "ICAR Good Agricultural Practices (GAP) for Apple"
    },

    # 4. Blueberry Healthy
    "Blueberry___healthy": {
        "problem_title": "Plant appears healthy",
        "why_happening": "Blueberry foliage exhibits dark green color, healthy shoot tip growth, and no signs of chlorosis or leaf spot pathogens.",
        "immediate_action": "Plant appears healthy. No curative disease treatment required.",
        "cultural_control": "Maintain acidic soil pH (4.5 to 5.5) using elemental sulfur. Maintain pine bark mulch bed.",
        "biological_organic": "Apply mycorrhizal root inoculants and organic compost tea.",
        "approved_chemical": "No chemical pesticide treatment needed for healthy crop foliage.",
        "safety_warning": "Avoid alkaline irrigation water to maintain proper soil acidity.",
        "follow_up_days": 14,
        "source_reference": "Small Fruit Extension Management Guidelines"
    },

    # 5. Cherry Powdery Mildew
    "Cherry___Powdery_mildew": {
        "problem_title": "Cherry Powdery Mildew (Podosphaera clandestina)",
        "why_happening": "Fungal pathogen Podosphaera clandestina forming white powdery mycelial patches on young foliage under warm dry days and humid nights.",
        "immediate_action": "Prune overcrowded sucker shoots and dense interior canopy branches to lower micro-humidity.",
        "cultural_control": "Ensure adequate sunlight penetration throughout the orchard canopy. Avoid excessive nitrogen fertilizer.",
        "biological_organic": "Foliar spray of Potassium Bicarbonate @ 4g/L water OR Neem Oil (Azadirachtin 10,000 ppm) @ 3ml/L water.",
        "approved_chemical": "Active Ingredient: Tebuconazole 25.9% EC @ 0.75ml/L water OR Myclobutanil 10% WP @ 0.4g/L water. Pre-Harvest Interval (PHI): 7 days.",
        "safety_warning": "Re-entry interval is 24 hours. Wear gloves and protective mask during foliar application.",
        "follow_up_days": 7,
        "source_reference": "TNAU & ICAR Horticultural Disease Management"
    },
    # 6. Cherry Healthy
    "Cherry___healthy": {
        "problem_title": "Plant appears healthy",
        "why_happening": "Cherry leaves show robust leaf blade expansion, deep chlorophyll greening, and clean margins.",
        "immediate_action": "Plant appears healthy. No curative disease treatment required.",
        "cultural_control": "Maintain orchard canopy pruning, drip irrigation, and balanced annual fertilization.",
        "biological_organic": "Apply seaweed extract foliar spray for enhanced stress tolerance.",
        "approved_chemical": "No chemical pesticide treatment needed for healthy crop foliage.",
        "safety_warning": "Inspect leaves bi-weekly for early detection of pests.",
        "follow_up_days": 14,
        "source_reference": "Horticultural Extension Service"
    },

    # 7. Corn Cercospora Leaf Spot Gray Leaf Spot
    "Corn___Cercospora_leaf_spot_Gray_leaf_spot": {
        "problem_title": "Corn Gray Leaf Spot (Cercospora zeae-maydis)",
        "why_happening": "Fungal pathogen causing rectangular necrotic leaf lesions restricted by leaf veins during warm, humid conditions.",
        "immediate_action": "Incorporate infected field stubble deep into soil after harvest to accelerate residue decomposition.",
        "cultural_control": "Practice 2-year crop rotation with non-host crops (e.g., soybeans). Plant tolerant corn hybrids.",
        "biological_organic": "Apply Trichoderma viride bio-fungicide @ 5g/L water at early tasseling stage.",
        "approved_chemical": "Active Ingredient: Azoxystrobin 18.2% + Difenoconazole 11.4% SC @ 1.0ml/L water OR Pyraclostrobin 20% WG @ 0.5g/L water. Pre-Harvest Interval (PHI): 14 days.",
        "safety_warning": "Do not apply fungicides near aquatic habitats or open water sources.",
        "follow_up_days": 7,
        "source_reference": "ICAR-IIMR Maize Pathology Advisory"
    },
    # 8. Corn Common Rust
    "Corn___Common_rust": {
        "problem_title": "Corn Common Rust (Puccinia sorghi)",
        "why_happening": "Airborne urediniospores of Puccinia sorghi germinating on corn leaf foliage under cool, humid weather (16-23°C).",
        "immediate_action": "Scout lower leaves weekly. If rust pustules cover >5% leaf area prior to silking, initiate protective treatment.",
        "cultural_control": "Plant rust-resistant corn hybrids. Plant early in the season to avoid peak spore flights.",
        "biological_organic": "Foliar application of Pseudomonas fluorescens @ 10g/L water at 10-day intervals.",
        "approved_chemical": "Active Ingredient: Propiconazole 25% EC @ 1.0ml/L water OR Mancozeb 75% WP @ 2.0g/L water. Pre-Harvest Interval (PHI): 14 days.",
        "safety_warning": "Adhere strictly to 14-day Pre-Harvest Interval (PHI).",
        "follow_up_days": 7,
        "source_reference": "National Maize Research Advisory"
    },
    # 9. Corn Northern Leaf Blight
    "Corn___Northern_Leaf_Blight": {
        "problem_title": "Corn Northern Leaf Blight (Exserohilum turcicum)",
        "why_happening": "Fungal infection producing long cigar-shaped greyish-green lesions on leaves during warm moist conditions.",
        "immediate_action": "Collect and destroy severely blighted lower leaves to reduce inoculum load.",
        "cultural_control": "Rotate corn fields with legumes or sunflowers. Till crop residues post-harvest.",
        "biological_organic": "Spray Bacillus subtilis bio-fungicide @ 5g/L water.",
        "approved_chemical": "Active Ingredient: Mancozeb 75% WP @ 2.0g/L water OR Azoxystrobin 23% SC @ 1.0ml/L water. Pre-Harvest Interval (PHI): 14 days.",
        "safety_warning": "Wear protective clothing and mask during spraying.",
        "follow_up_days": 7,
        "source_reference": "ICAR-IIMR Disease Management Guide"
    },
    # 10. Corn Healthy
    "Corn___healthy": {
        "problem_title": "Plant appears healthy",
        "why_happening": "Corn leaves display healthy dark green coloration, strong leaf midribs, and no disease lesions or pest feeding.",
        "immediate_action": "Plant appears healthy. No curative disease treatment required.",
        "cultural_control": "Maintain balanced N-P-K soil fertilization (split urea application) and adequate irrigation during silking.",
        "biological_organic": "Incorporate Azospirillum / Azotobacter bio-fertilizers in root zone.",
        "approved_chemical": "No chemical pesticide treatment needed for healthy crop foliage.",
        "safety_warning": "Scout field regularly for early signs of fall armyworm or stem borers.",
        "follow_up_days": 14,
        "source_reference": "ICAR Good Agricultural Practices for Maize"
    },

    # 11. Grape Black Rot
    "Grape___Black_rot": {
        "problem_title": "Grape Black Rot (Guignardia bidwellii)",
        "why_happening": "Fungal infection causing brown circular leaf spots and black shriveled mummified berries during warm wet spring weather.",
        "immediate_action": "Prune and destroy all mummified berries and infected canes during dormant season.",
        "cultural_control": "Train grapevines on open trellis systems to promote rapid canopy leaf drying.",
        "biological_organic": "Foliar application of Copper Hydroxide @ 2.0g/L water at early bud burst.",
        "approved_chemical": "Active Ingredient: Myclobutanil 10% WP @ 0.4g/L water OR Mancozeb 75% WP @ 2.0g/L water. Pre-Harvest Interval (PHI): 14 days.",
        "safety_warning": "Observe 14-day PHI. Wash harvested grapes thoroughly before processing.",
        "follow_up_days": 7,
        "source_reference": "National Research Centre for Grapes (NRCG) Advisory"
    },
    # 12. Grape Esca Black Measles
    "Grape___Esca_Black_Measles": {
        "problem_title": "Grape Esca & Black Measles Trunk Disease",
        "why_happening": "Complex fungal trunk infection (Phaeoacremonium / Phaeomoniella) causing interveinal leaf striping ('tiger-stripes') and berry spotting.",
        "immediate_action": "Mark infected vines for dormant pruning. Disinfect pruning shears between cuts using 70% ethanol.",
        "cultural_control": "Apply wound sealant paste over large pruning cuts immediately to prevent spore entry.",
        "biological_organic": "Apply Trichoderma spp. biocontrol paste on fresh pruning wounds.",
        "approved_chemical": "No effective systemic chemical cure exists for internal wood rot; focus on trunk sanitation and wound protection.",
        "safety_warning": "Avoid pruning during rainy weather when fungal spores are airborne.",
        "follow_up_days": 14,
        "source_reference": "Viticulture Trunk Disease Extension Manual"
    },
    # 13. Grape Leaf Blight Isariopsis Leaf Spot
    "Grape___Leaf_blight_Isariopsis_Leaf_Spot": {
        "problem_title": "Grape Isariopsis Leaf Blight (Pseudocercospora vitis)",
        "why_happening": "Fungal leaf spot causing irregular brown lesions on leaves and premature defoliation under high humidity.",
        "immediate_action": "Prune lower shaded foliage to improve air movement under the grapevine canopy.",
        "cultural_control": "Remove fallen vineyard leaf litter post-harvest to minimize overwintering spores.",
        "biological_organic": "Foliar application of Pseudomonas fluorescens @ 10g/L water.",
        "approved_chemical": "Active Ingredient: Copper Oxychloride 50% WP @ 2.5g/L water OR Carbendazim 50% WP @ 1.0g/L water. Pre-Harvest Interval (PHI): 14 days.",
        "safety_warning": "Wear protective mask and long sleeves during chemical application.",
        "follow_up_days": 7,
        "source_reference": "NRCG Grape Pathology Bulletin"
    },
    # 14. Grape Healthy
    "Grape___healthy": {
        "problem_title": "Plant appears healthy",
        "why_happening": "Grapevine foliage shows vibrant green leaves, strong cane growth, and clear fruit clusters.",
        "immediate_action": "Plant appears healthy. No curative disease treatment required.",
        "cultural_control": "Maintain canopy leaf thinning, drip fertigation, and trellis wire management.",
        "biological_organic": "Spray bio-stimulants (amino acid / kelp extract) for cluster development.",
        "approved_chemical": "No chemical pesticide treatment needed for healthy crop foliage.",
        "safety_warning": "Monitor undersides of leaves weekly for downy mildew or mites.",
        "follow_up_days": 14,
        "source_reference": "Good Viticultural Practices Advisory"
    },

    # 15. Orange Haunglongbing Citrus Greening
    "Orange___Haunglongbing_Citrus_greening": {
        "problem_title": "Citrus Greening / Huanglongbing (Candidatus Liberibacter asiaticus)",
        "why_happening": "Bacterial phloem disease transmitted by Asian Citrus Psyllid (Diaphorina citri), causing asymmetric blotchy leaf mottle and small lopsided bitter fruit.",
        "immediate_action": "Rogue out severely decline-stage trees. Prune infected branches and control psyllid vector populations immediately.",
        "cultural_control": "Plant certified disease-free tissue-cultured citrus saplings. Install yellow sticky traps for psyllid monitoring.",
        "biological_organic": "Foliar application of Neem Seed Kernel Extract (NSKE 5%) or Entomopathogenic fungi (Beauveria bassiana @ 5g/L) for vector control.",
        "approved_chemical": "Active Ingredient: Imidacloprid 17.8% SL @ 0.4ml/L water OR Thiamethoxam 25% WG @ 0.3g/L water targeting Asian Citrus Psyllid vector. Pre-Harvest Interval (PHI): 15 days.",
        "safety_warning": "Apply systemic insecticides after bloom to protect honeybees.",
        "follow_up_days": 10,
        "source_reference": "ICAR-CCRI Citrus Advisory Bulletin"
    },

    # 16. Peach Bacterial Spot
    "Peach___Bacterial_spot": {
        "problem_title": "Peach Bacterial Spot (Xanthomonas arboricola pv. pruni)",
        "why_happening": "Bacterial infection causing small angular water-soaked leaf spots that drop out, creating a 'shot-hole' appearance.",
        "immediate_action": "Prune diseased twigs during winter dormant period and destroy infected orchard prunings.",
        "cultural_control": "Plant resistant peach cultivars. Maintain orchard windbreaks to minimize wind-driven rain bacterial spread.",
        "biological_organic": "Copper Hydroxide organic protective spray @ 1.5g/L at delayed dormant stage.",
        "approved_chemical": "Active Ingredient: Copper Oxychloride 50% WP @ 2.0g/L water OR Oxytetracycline bactericide @ 0.5g/L water (where approved). Pre-Harvest Interval (PHI): 21 days.",
        "safety_warning": "Avoid copper sprays during warm humid weather to prevent copper phytotoxicity on foliage.",
        "follow_up_days": 7,
        "source_reference": "ICAR Stone Fruit Pathology Advisory"
    },
    # 17. Peach Healthy
    "Peach___healthy": {
        "problem_title": "Plant appears healthy",
        "why_happening": "Peach foliage displays lush green leaves, healthy twig extension, and clean bark.",
        "immediate_action": "Plant appears healthy. No curative disease treatment required.",
        "cultural_control": "Maintain open-center tree pruning, root zone mulching, and thinning of overset fruits.",
        "biological_organic": "Apply organic neem cake around root zone for nematode suppression.",
        "approved_chemical": "No chemical pesticide treatment needed for healthy crop foliage.",
        "safety_warning": "Perform seasonal trunk inspection for peach tree borer larvae.",
        "follow_up_days": 14,
        "source_reference": "Horticultural Extension Service"
    },

    # 18. Pepper Bell Bacterial Spot
    "Pepper_bell___Bacterial_spot": {
        "problem_title": "Bell Pepper Bacterial Spot (Xanthomonas euvesicatoria)",
        "why_happening": "Bacterial pathogen entering leaf stomata and wounds during warm, rainy weather (>24°C), causing dark blister-like spots.",
        "immediate_action": "Remove heavily spotted lower leaves immediately. Avoid working in pepper fields when foliage is wet.",
        "cultural_control": "Use certified disease-free seeds. Practice 2-year rotation away from solanaceous crops. Use drip irrigation.",
        "biological_organic": "Foliar spray of Copper Hydroxide (1%) + Bacillus subtilis bio-bactericide @ 5g/L water.",
        "approved_chemical": "Active Ingredient: Copper Oxychloride 50% WP @ 2.5g/L water mixed with Streptomycin sulphate (100 ppm). Pre-Harvest Interval (PHI): 7 days.",
        "safety_warning": "Wear protective gear. Observe 7-day PHI before pepper harvest.",
        "follow_up_days": 7,
        "source_reference": "IIHR Vegetable Crop Advisory"
    },
    # 19. Pepper Bell Healthy
    "Pepper_bell___healthy": {
        "problem_title": "Plant appears healthy",
        "why_happening": "Bell pepper foliage is deep green, erect, with healthy flowering nodes and firm fruit set.",
        "immediate_action": "Plant appears healthy. No curative disease treatment required.",
        "cultural_control": "Maintain steady soil moisture using drip irrigation. Apply calcium nitrate to prevent blossom-end rot.",
        "biological_organic": "Apply Panchagavya or seaweed liquid fertilizer foliar spray.",
        "approved_chemical": "No chemical pesticide treatment needed for healthy crop foliage.",
        "safety_warning": "Scout undersides of leaves weekly for aphids or thrips.",
        "follow_up_days": 14,
        "source_reference": "ICAR Vegetable Production Guide"
    },

    # 20. Potato Early Blight
    "Potato___Early_blight": {
        "problem_title": "Potato Early Blight (Alternaria solani)",
        "why_happening": "Fungal infection causing dark brown concentric target-board ring spots on older lower leaves during warm, humid conditions.",
        "immediate_action": "Prune and destroy infected lower leaves. Ensure adequate nitrogen and potassium plant nutrition.",
        "cultural_control": "Rotate potato fields with non-solanaceous crops (maize, beans). Space rows for foliage drying.",
        "biological_organic": "Foliar application of Trichoderma viride @ 5g/L or Bio-Copper spray.",
        "approved_chemical": "Active Ingredient: Mancozeb 75% WP @ 2.0g/L water OR Chlorothalonil 75% WP @ 2.0g/L water. Pre-Harvest Interval (PHI): 14 days.",
        "safety_warning": "Re-entry interval is 24 hours. Wear protective mask and gloves.",
        "follow_up_days": 7,
        "source_reference": "ICAR-CPRI Potato Pathology Advisory"
    },
    # 21. Potato Late Blight
    "Potato___Late_blight": {
        "problem_title": "Potato Late Blight (Phytophthora infestans)",
        "why_happening": "Destructive oomycete pathogen Phytophthora infestans causing rapid dark water-soaked leaf lesions with white mold on undersides during cool, foggy, rainy weather.",
        "immediate_action": "Destroy severely infected plants immediately. Stop sprinkler irrigation.",
        "cultural_control": "Plant certified disease-free seed tubers. Hill soil high over potato rows to protect tubers from spore wash.",
        "biological_organic": "Foliar spray of Copper Hydroxide @ 2.5g/L water at first weather warning.",
        "approved_chemical": "Active Ingredient: Metalaxyl 8% + Mancozeb 64% WP @ 2.5g/L water OR Cymoxanil 8% + Mancozeb 64% WP @ 2.0g/L water. Pre-Harvest Interval (PHI): 14 days.",
        "safety_warning": "Late blight can destroy crops within days; initiate protective sprays promptly upon weather alerts.",
        "follow_up_days": 5,
        "source_reference": "Central Potato Research Institute (CPRI) Emergency Advisory"
    },
    # 22. Potato Healthy
    "Potato___healthy": {
        "problem_title": "Plant appears healthy",
        "why_happening": "Potato foliage shows full green canopy coverage, robust stem vigor, and no leaf spots.",
        "immediate_action": "Plant appears healthy. No curative disease treatment required.",
        "cultural_control": "Maintain row hilling, balanced potassium soil fertility, and regulated irrigation.",
        "biological_organic": "Apply bio-fertilizer inoculants (PSB / Azotobacter) into soil.",
        "approved_chemical": "No chemical pesticide treatment needed for healthy crop foliage.",
        "safety_warning": "Inspect potato canopy twice weekly during humid weather spells.",
        "follow_up_days": 14,
        "source_reference": "CPRI Good Potato Farming Practices"
    },

    # 23. Raspberry Healthy
    "Raspberry___healthy": {
        "problem_title": "Plant appears healthy",
        "why_happening": "Raspberry canes display vibrant green foliage, healthy spur development, and no leaf rust or cane blight lesions.",
        "immediate_action": "Plant appears healthy. No curative disease treatment required.",
        "cultural_control": "Trellis primocanes and floricanes cleanly. Prune spent floricanes after fruit harvest.",
        "biological_organic": "Mulch base with organic compost and straw.",
        "approved_chemical": "No chemical pesticide treatment needed for healthy crop foliage.",
        "safety_warning": "Ensure adequate row spacing for ventilation.",
        "follow_up_days": 14,
        "source_reference": "Small Fruit Extension Guidelines"
    },

    # 24. Soybean Healthy
    "Soybean___healthy": {
        "problem_title": "Plant appears healthy",
        "why_happening": "Soybean trifoliate leaves display dark green color, healthy nodulation on roots, and clean leaf blades.",
        "immediate_action": "Plant appears healthy. No curative disease treatment required.",
        "cultural_control": "Maintain crop rotation, field weed control, and proper seed spacing.",
        "biological_organic": "Inoculate seeds with Bradyrhizobium japonicum before planting.",
        "approved_chemical": "No chemical pesticide treatment needed for healthy crop foliage.",
        "safety_warning": "Scout field for defoliating caterpillars or girdle beetles.",
        "follow_up_days": 14,
        "source_reference": "ICAR-IISR Soybean Advisory"
    },

    # 25. Squash Powdery Mildew
    "Squash___Powdery_mildew": {
        "problem_title": "Squash Powdery Mildew (Erysiphe cichoracearum / Podosphaera xanthii)",
        "why_happening": "White powdery fungal coating covering upper and lower leaf surfaces, causing leaf yellowing and premature drying under dry days and humid nights.",
        "immediate_action": "Prune old, heavily infected shaded leaves from base of squash vines.",
        "cultural_control": "Plant resistant squash varieties. Space plants 90cm apart for canopy ventilation.",
        "biological_organic": "Foliar application of Potassium Bicarbonate @ 4g/L water OR Neem Oil (Azadirachtin 10,000 ppm) @ 3ml/L water.",
        "approved_chemical": "Active Ingredient: Myclobutanil 10% WP @ 0.4g/L water OR Difenoconazole 25% EC @ 0.5ml/L water. Pre-Harvest Interval (PHI): 3 days.",
        "safety_warning": "Observe 3-day Pre-Harvest Interval (PHI). Do not apply sulfur during high heat (>32°C).",
        "follow_up_days": 7,
        "source_reference": "IIHR Vegetable Pathology Advisory"
    },

    # 26. Strawberry Leaf Scorch
    "Strawberry___Leaf_scorch": {
        "problem_title": "Strawberry Leaf Scorch (Diplocarpon earlianum)",
        "why_happening": "Fungal pathogen causing small purplish spots on upper leaf surfaces that enlarge and coalesce, giving foliage a scorched, dried appearance.",
        "immediate_action": "Remove severely scorched leaves immediately. Avoid overhead sprinkler watering.",
        "cultural_control": "Renovate strawberry beds post-harvest by mowing old foliage. Use clean straw mulch under berries.",
        "biological_organic": "Spray Bio-Copper Hydroxide @ 2g/L or Trichoderma harzianum @ 5g/L water.",
        "approved_chemical": "Active Ingredient: Captan 50% WP @ 2.5g/L water OR Difenoconazole 25% EC @ 0.5ml/L water. Pre-Harvest Interval (PHI): 7 days.",
        "safety_warning": "Adhere to 7-day PHI. Wash harvested berries thoroughly.",
        "follow_up_days": 7,
        "source_reference": "TNAU Small Fruit Protection Advisory"
    },
    # 27. Strawberry Healthy
    "Strawberry___healthy": {
        "problem_title": "Plant appears healthy",
        "why_happening": "Strawberry plants feature lush green crowns, erect petioles, vibrant white flowers, and clean leaves.",
        "immediate_action": "Plant appears healthy. No curative disease treatment required.",
        "cultural_control": "Maintain drip irrigation under straw mulching bed to keep fruits clean.",
        "biological_organic": "Foliar application of bio-stimulants for berry sizing.",
        "approved_chemical": "No chemical pesticide treatment needed for healthy crop foliage.",
        "safety_warning": "Inspect fruit clusters regularly for grey mold (Botrytis).",
        "follow_up_days": 14,
        "source_reference": "Strawberry Extension Management Guide"
    },

    # 28. Tomato Bacterial Spot
    "Tomato___Bacterial_spot": {
        "problem_title": "Tomato Bacterial Spot (Xanthomonas perforans)",
        "why_happening": "Bacterial pathogen entering foliage through stomata and wounds under warm, rainy conditions, producing small water-soaked dark spots with yellow halos.",
        "immediate_action": "Prune infected lower foliage immediately. Avoid handling plants when wet.",
        "cultural_control": "Stake tomato plants, space 60cm apart, use drip irrigation, and rotate away from solanaceous crops.",
        "biological_organic": "Foliar spray of Copper Hydroxide (1%) + Bacillus subtilis bio-bactericide @ 5g/L water.",
        "approved_chemical": "Active Ingredient: Copper Oxychloride 50% WP @ 2.5g/L water mixed with Streptomycin sulphate (100 ppm). Pre-Harvest Interval (PHI): 7 days.",
        "safety_warning": "Wear protective gloves and mask. Observe 7-day PHI before fruit harvest.",
        "follow_up_days": 7,
        "source_reference": "TNAU & ICAR Vegetable Pathology Guidelines"
    },
    # 29. Tomato Early Blight
    "Tomato___Early_blight": {
        "problem_title": "Tomato Early Blight (Alternaria solani)",
        "why_happening": "Fungal infection causing brown target-board spots with concentric rings starting on older lower leaves during warm humid weather.",
        "immediate_action": "Prune off infected lower leaves up to the first fruit cluster and destroy them.",
        "cultural_control": "Mulch plant base with straw/plastic to prevent soil splash. Stake tomato vines for airflow.",
        "biological_organic": "Spray Trichoderma viride @ 5g/L water or Copper Hydroxide @ 2g/L water.",
        "approved_chemical": "Active Ingredient: Mancozeb 75% WP @ 2.0g/L water OR Difenoconazole 25% EC @ 0.5ml/L water. Pre-Harvest Interval (PHI): 7 days.",
        "safety_warning": "Observe 7-day Pre-Harvest Interval (PHI). Wear protective equipment during spraying.",
        "follow_up_days": 7,
        "source_reference": "IIHR Tomato Disease Advisory"
    },
    # 30. Tomato Late Blight
    "Tomato___Late_blight": {
        "problem_title": "Tomato Late Blight (Phytophthora infestans)",
        "why_happening": "Aggressive oomycete pathogen producing large dark water-soaked leaf lesions with white cottony spore mold on leaf undersides during cool, wet weather.",
        "immediate_action": "Remove and destroy severely affected foliage immediately. Stop overhead watering.",
        "cultural_control": "Ensure wide plant spacing, clear weed hosts, and destroy infected crop residues post-harvest.",
        "biological_organic": "Foliar application of Copper Hydroxide @ 2.5g/L water at disease onset.",
        "approved_chemical": "Active Ingredient: Metalaxyl 8% + Mancozeb 64% WP @ 2.5g/L water OR Famoxadone 16.6% + Cymoxanil 22.1% SC @ 1.0ml/L water. Pre-Harvest Interval (PHI): 7 days.",
        "safety_warning": "Late blight spreads rapidly; apply protective spray promptly upon symptom detection.",
        "follow_up_days": 5,
        "source_reference": "ICAR-IIHR Emergency Tomato Advisory"
    },
    # 31. Tomato Leaf Mold
    "Tomato___Leaf_Mold": {
        "problem_title": "Tomato Leaf Mold (Passalora fulva / Fulvia fulva)",
        "why_happening": "Fungal pathogen causing pale green/yellow spots on upper leaf surfaces and dense olivaceous velvety mold patches on undersides under high relative humidity (>85%).",
        "immediate_action": "Vigorously increase greenhouse/field ventilation. Prune lower crowded leaves.",
        "cultural_control": "Reduce relative humidity below 85% using exhaust fans or wide plant spacing. Avoid evening canopy watering.",
        "biological_organic": "Spray Bio-Copper Hydroxide @ 2.0g/L or Trichoderma harzianum @ 5g/L water.",
        "approved_chemical": "Active Ingredient: Difenoconazole 25% EC @ 0.5ml/L water OR Mancozeb 75% WP @ 2.0g/L water. Pre-Harvest Interval (PHI): 7 days.",
        "safety_warning": "Adhere to 7-day Pre-Harvest Interval (PHI). Wear mask during spraying.",
        "follow_up_days": 7,
        "source_reference": "Vegetable Pathology Extension Bulletin"
    },
    # 32. Tomato Septoria Leaf Spot
    "Tomato___Septoria_leaf_spot": {
        "problem_title": "Tomato Septoria Leaf Spot (Septoria lycopersici)",
        "why_happening": "Fungal infection creating numerous small circular spots with dark brown margins and grey centers containing tiny black specks (pycnidia).",
        "immediate_action": "Prune affected lower leaves immediately. Mulch soil around plant stems.",
        "cultural_control": "Rotate out of tomatoes for 2 years. Stake vines off wet soil and use drip irrigation.",
        "biological_organic": "Foliar application of Copper Hydroxide @ 2.0g/L water.",
        "approved_chemical": "Active Ingredient: Chlorothalonil 75% WP @ 2.0g/L water OR Mancozeb 75% WP @ 2.0g/L water. Pre-Harvest Interval (PHI): 7 days.",
        "safety_warning": "Re-entry interval is 24 hours. Wash harvested tomatoes thoroughly.",
        "follow_up_days": 7,
        "source_reference": "ICAR-IIHR Tomato Protection Advisory"
    },
    # 33. Tomato Spider Mites Two-Spotted Spider Mite
    "Tomato___Spider_mites_Two-spotted_spider_mite": {
        "problem_title": "Tomato Two-Spotted Spider Mite (Tetranychus urticae)",
        "why_happening": "Sap-sucking mite infestation causing fine yellow stippling, bronzing, and delicate silk webbing on leaf undersides under hot dry conditions.",
        "immediate_action": "Spray plant undersides with strong water jet to knock down mite colonies.",
        "cultural_control": "Maintain field border weed control. Overhead misting during peak heat can suppress mite buildup.",
        "biological_organic": "Release predatory mites (Phytoseiulus persimilis) OR spray Neem Oil (Azadirachtin 10,000 ppm) @ 3ml/L water.",
        "approved_chemical": "Active Ingredient: Abamectin 1.9% EC @ 0.5ml/L water OR Spiromesifen 22.9% SC @ 0.8ml/L water. Pre-Harvest Interval (PHI): 3 days.",
        "safety_warning": "Do not re-use chemical miticides continuously to prevent mite resistance development.",
        "follow_up_days": 5,
        "source_reference": "ICAR-NBAIR Acarology Advisory"
    },
    # 34. Tomato Target Spot
    "Tomato___Target_Spot": {
        "problem_title": "Tomato Target Spot (Corynespora cassiicola)",
        "why_happening": "Fungal infection causing pinpoint brown leaf spots that enlarge into circular lesions with light brown centers and dark target-like borders.",
        "immediate_action": "Prune severely affected lower leaves. Avoid overhead sprinkler irrigation.",
        "cultural_control": "Improve canopy airflow, clear plant debris post-harvest, and practice crop rotation.",
        "biological_organic": "Foliar spray of Bacillus subtilis bio-fungicide @ 5g/L water.",
        "approved_chemical": "Active Ingredient: Azoxystrobin 23% SC @ 1.0ml/L water OR Chlorothalonil 75% WP @ 2.0g/L water. Pre-Harvest Interval (PHI): 7 days.",
        "safety_warning": "Observe 7-day PHI. Wear protective clothing during spraying.",
        "follow_up_days": 7,
        "source_reference": "Vegetable Crop Advisory"
    },
    # 35. Tomato Tomato Mosaic Virus
    "Tomato___Tomato_mosaic_virus": {
        "problem_title": "Tomato Mosaic Virus (ToMV)",
        "why_happening": "Mechanically transmitted Tobamovirus causing leaf mosaic mottling, fern-like leaf distortion, and stunted growth.",
        "immediate_action": "Rogue out (pull up and burn) virus-infected tomato plants immediately to prevent mechanical transmission to adjacent crop.",
        "cultural_control": "Wash hands with soap and disinfect pruning shears with 10% trisodium phosphate (TSP) or non-fat milk solution before handling plants. Do not smoke around tomato plants.",
        "biological_organic": "No biological cure for plant viruses; focus on strict sanitation and viral vector control.",
        "approved_chemical": "No chemical pesticide cures plant viral infections once established.",
        "safety_warning": "ToMV is extremely stable and easily spread by hands, clothing, and tools.",
        "follow_up_days": 5,
        "source_reference": "ICAR Plant Virology Advisory"
    },
    # 36. Tomato Tomato Yellow Leaf Curl Virus
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "problem_title": "Tomato Yellow Leaf Curl Virus (TYLCV)",
        "why_happening": "Begomovirus transmitted by Whitefly vector (Bemisia tabaci), causing severe upward leaf curling, yellowing leaf margins, and plant stunting.",
        "immediate_action": "Rogue out infected plants immediately. Install yellow sticky traps @ 15/acre to suppress whitefly vectors.",
        "cultural_control": "Use fine mesh insect netting (50-mesh) in seedbeds. Plant TYLCV-resistant tomato cultivars.",
        "biological_organic": "Foliar application of Neem Seed Kernel Extract (NSKE 5%) or Lecanicillium lecanii bio-insecticide @ 5g/L water.",
        "approved_chemical": "Active Ingredient: Imidacloprid 17.8% SL @ 0.3ml/L water OR Acetamiprid 20% SP @ 0.2g/L water targeting whitefly vector populations. Pre-Harvest Interval (PHI): 7 days.",
        "safety_warning": "Apply insecticides adhering to PHI. Wear protective gear.",
        "follow_up_days": 7,
        "source_reference": "ICAR-IIHR Whitefly & Virus Vector Advisory"
    },
    # 37. Tomato Healthy
    "Tomato___healthy": {
        "problem_title": "Plant appears healthy",
        "why_happening": "Tomato foliage shows lush green compound leaves, strong vine growth, clean flower clusters, and healthy root development.",
        "immediate_action": "Plant appears healthy. No curative disease treatment required.",
        "cultural_control": "Maintain vine staking, prune non-fruiting sucker shoots, and apply balanced organic compost.",
        "biological_organic": "Spray Panchagavya or humic acid foliar spray for vine vigor.",
        "approved_chemical": "No chemical pesticide treatment needed for healthy crop foliage.",
        "safety_warning": "Inspect leaf undersides weekly for early signs of whiteflies or blight.",
        "follow_up_days": 14,
        "source_reference": "ICAR Good Agricultural Practices for Tomato"
    }
}

def get_treatment_for_class(class_name: str) -> Dict[str, Any]:
    """
    Retrieves the exact grounded treatment knowledge entry for any of the 38 PlantVillage classes.
    """
    if class_name in TREATMENT_KNOWLEDGE_38:
        return dict(TREATMENT_KNOWLEDGE_38[class_name])

    # Fallback if class string is unknown
    return {
        "problem_title": f"Condition ({class_name})",
        "why_happening": "Observed foliage condition requiring field verification.",
        "immediate_action": "Scout crop field for symptom spread and isolate heavily affected plant foliage.",
        "cultural_control": "Maintain field sanitation, proper crop spacing, and balanced irrigation.",
        "biological_organic": "Consult local agricultural extension professional for verified biological recommendations.",
        "approved_chemical": "Consult local agricultural extension professional for approved chemical treatments.",
        "safety_warning": "Follow local pesticide safety regulations and wear protective equipment.",
        "follow_up_days": 7,
        "source_reference": "Agricultural Extension Service Knowledge Base"
    }
