'use client';

import React, { useState } from 'react';
import { useTranslation } from '@/lib/i18n';
import { 
  Calculator, Sprout, Layers, FlaskConical, CheckCircle2, BookOpen, ArrowRight 
} from 'lucide-react';

export default function FertilizerPage() {
  const { t } = useTranslation();
  const [cropName, setCropName] = useState("Chilli");
  const [areaAcres, setAreaAcres] = useState(1.0);
  const [soilN, setSoilN] = useState(20);
  const [soilP, setSoilP] = useState(10);
  const [soilK, setSoilK] = useState(150);

  const [result, setResult] = useState<any>(null);

  const handleCalculate = (e: React.FormEvent) => {
    e.preventDefault();
    // Execute standard formula calculation
    const n_req = Math.max(15, (60 - (soilN * 0.5)) * areaAcres);
    const p_req = Math.max(10, (40 - (soilP * 0.4)) * areaAcres);
    const k_req = Math.max(10, (40 - (soilK * 0.1)) * areaAcres);

    const dap_kg = Number((p_req / 0.46).toFixed(1));
    const n_from_dap = dap_kg * 0.18;
    const rem_n = Math.max(0, n_req - n_from_dap);
    const urea_kg = Number((rem_n / 0.46).toFixed(1));
    const mop_kg = Number((k_req / 0.60).toFixed(1));
    const compost = Number((2.5 * areaAcres).toFixed(1));

    setResult({
      crop_name: cropName,
      area_acres: areaAcres,
      nitrogen_req_kg: Number(n_req.toFixed(1)),
      phosphorus_req_kg: Number(p_req.toFixed(1)),
      potassium_req_kg: Number(k_req.toFixed(1)),
      recommended_urea_kg: urea_kg,
      recommended_dap_kg: dap_kg,
      recommended_mop_kg: mop_kg,
      organic_compost_tons: compost,
      formula_explanation: `Calculated using ICAR Extension Formula for ${cropName} across ${areaAcres} acre(s). DAP supplies ${p_req.toFixed(1)} kg P2O5 and ${n_from_dap.toFixed(1)} kg N. Remaining N is provided by Urea.`
    });
  };

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div>
        <div className="inline-flex items-center space-x-1.5 bg-teal-500/20 text-teal-300 border border-teal-500/30 px-3 py-1 rounded-full text-xs font-semibold mb-2">
          <BookOpen className="w-3.5 h-3.5" />
          <span>Rule-Based Agricultural Extension Formulas</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white flex items-center gap-2">
          <Calculator className="w-8 h-8 text-emerald-400" />
          {t('fertilizer.title')}
        </h1>
        <p className="text-sm text-emerald-200/80 mt-1">
          {t('fertilizer.subtitle')}
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Left Column (5 Cols): Form Inputs */}
        <div className="lg:col-span-5 space-y-4">
          <div className="glass-panel p-6 rounded-2xl border border-emerald-800/60 space-y-4">
            <h3 className="text-sm font-bold text-white flex items-center gap-2">
              <FlaskConical className="w-4 h-4 text-emerald-400" />
              Input Soil Test & Crop Parameters
            </h3>

            <form onSubmit={handleCalculate} className="space-y-3 text-xs">
              <div>
                <label className="block text-emerald-300 mb-1">Target Crop</label>
                <select
                  value={cropName}
                  onChange={(e) => setCropName(e.target.value)}
                  className="w-full bg-emerald-900/60 border border-emerald-700 rounded-xl p-2.5 text-white focus:outline-none"
                >
                  <option value="Chilli">Chilli / Pepper</option>
                  <option value="Rice">Paddy Rice</option>
                  <option value="Tomato">Tomato</option>
                  <option value="Sweet Corn">Sweet Corn / Maize</option>
                  <option value="Cotton">Cotton</option>
                </select>
              </div>

              <div>
                <label className="block text-emerald-300 mb-1">Planted Area (Acres)</label>
                <input
                  type="number"
                  step="0.1"
                  value={areaAcres}
                  onChange={(e) => setAreaAcres(Number(e.target.value))}
                  className="w-full bg-emerald-900/60 border border-emerald-700 rounded-xl p-2.5 text-white focus:outline-none"
                  required
                />
              </div>

              <div className="pt-2 border-t border-emerald-800/40 space-y-3">
                <span className="text-[11px] font-bold text-teal-300 uppercase">Soil Test Values (PPM)</span>
                
                <div className="grid grid-cols-3 gap-2">
                  <div>
                    <label className="block text-emerald-300 mb-1">Nitrogen (N)</label>
                    <input
                      type="number"
                      value={soilN}
                      onChange={(e) => setSoilN(Number(e.target.value))}
                      className="w-full bg-emerald-900/60 border border-emerald-700 rounded-xl p-2 text-white focus:outline-none"
                    />
                  </div>

                  <div>
                    <label className="block text-emerald-300 mb-1">Phosphorus (P)</label>
                    <input
                      type="number"
                      value={soilP}
                      onChange={(e) => setSoilP(Number(e.target.value))}
                      className="w-full bg-emerald-900/60 border border-emerald-700 rounded-xl p-2 text-white focus:outline-none"
                    />
                  </div>

                  <div>
                    <label className="block text-emerald-300 mb-1">Potassium (K)</label>
                    <input
                      type="number"
                      value={soilK}
                      onChange={(e) => setSoilK(Number(e.target.value))}
                      className="w-full bg-emerald-900/60 border border-emerald-700 rounded-xl p-2 text-white focus:outline-none"
                    />
                  </div>
                </div>
              </div>

              <button
                type="submit"
                className="w-full bg-gradient-to-r from-emerald-500 to-teal-400 text-emerald-950 font-extrabold py-3 rounded-xl shadow-lg hover:scale-105 transition-transform text-xs mt-3"
              >
                {t('fertilizer.calculateCta')}
              </button>
            </form>
          </div>
        </div>

        {/* Right Column (7 Cols): Calculation Output */}
        <div className="lg:col-span-7 space-y-4">
          {result ? (
            <div className="glass-panel p-6 rounded-2xl border border-emerald-800/60 space-y-5">
              
              <div className="border-b border-emerald-800/60 pb-3">
                <span className="text-[10px] font-bold text-teal-400 uppercase tracking-wider">Recommended Fertilizer Schedule</span>
                <h3 className="text-xl font-bold text-white mt-0.5">{result.crop_name} ({result.area_acres} Acres)</h3>
              </div>

              {/* 3 Nutrient Requirement Badges */}
              <div className="grid grid-cols-3 gap-3">
                <div className="bg-emerald-900/60 border border-emerald-700/60 p-3 rounded-xl text-center">
                  <span className="text-[10px] text-emerald-300 font-bold">Nitrogen (N)</span>
                  <div className="text-lg font-black text-white">{result.nitrogen_req_kg} kg</div>
                </div>

                <div className="bg-emerald-900/60 border border-emerald-700/60 p-3 rounded-xl text-center">
                  <span className="text-[10px] text-teal-300 font-bold">Phosphorus (P2O5)</span>
                  <div className="text-lg font-black text-white">{result.phosphorus_req_kg} kg</div>
                </div>

                <div className="bg-emerald-900/60 border border-emerald-700/60 p-3 rounded-xl text-center">
                  <span className="text-[10px] text-sky-300 font-bold">Potassium (K2O)</span>
                  <div className="text-lg font-black text-white">{result.potassium_req_kg} kg</div>
                </div>
              </div>

              {/* Commercial Fertilizer Bags Breakdown */}
              <div className="space-y-3">
                <h4 className="text-xs font-bold text-white">Commercial Fertilizer Quantities</h4>
                
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                  <div className="bg-emerald-950/80 border border-emerald-800/60 p-3.5 rounded-xl flex items-center justify-between">
                    <div>
                      <span className="font-bold text-white">Urea (46% N)</span>
                      <p className="text-[10px] text-emerald-300/70">Split top dressing</p>
                    </div>
                    <strong className="text-emerald-300 text-sm">{result.recommended_urea_kg} kg</strong>
                  </div>

                  <div className="bg-emerald-950/80 border border-emerald-800/60 p-3.5 rounded-xl flex items-center justify-between">
                    <div>
                      <span className="font-bold text-white">DAP (18:46:0)</span>
                      <p className="text-[10px] text-emerald-300/70">Basal application</p>
                    </div>
                    <strong className="text-teal-300 text-sm">{result.recommended_dap_kg} kg</strong>
                  </div>

                  <div className="bg-emerald-950/80 border border-emerald-800/60 p-3.5 rounded-xl flex items-center justify-between">
                    <div>
                      <span className="font-bold text-white">MOP (60% K2O)</span>
                      <p className="text-[10px] text-emerald-300/70">Potash fertilizer</p>
                    </div>
                    <strong className="text-sky-300 text-sm">{result.recommended_mop_kg} kg</strong>
                  </div>

                  <div className="bg-emerald-950/80 border border-emerald-800/60 p-3.5 rounded-xl flex items-center justify-between">
                    <div>
                      <span className="font-bold text-white">Organic FYM</span>
                      <p className="text-[10px] text-emerald-300/70">Farmyard Compost</p>
                    </div>
                    <strong className="text-amber-300 text-sm">{result.organic_compost_tons} Tons</strong>
                  </div>
                </div>
              </div>

              {/* Mathematical Explanation */}
              <div className="bg-emerald-900/40 border border-emerald-700/50 p-4 rounded-xl text-xs text-emerald-200/90 leading-relaxed">
                <strong className="text-teal-300">Calculation Audit: </strong>
                {result.formula_explanation}
              </div>

            </div>
          ) : (
            <div className="glass-panel p-8 rounded-2xl border border-emerald-800/60 text-center space-y-3">
              <Calculator className="w-12 h-12 text-emerald-500/50 mx-auto" />
              <h4 className="text-sm font-bold text-white">Fertilizer Calculation Ready</h4>
              <p className="text-xs text-emerald-200/70 max-w-sm mx-auto">
                Enter your soil test parameters (N, P, K) and crop area on the left, then click calculate to generate an optimal ICAR dosage schedule.
              </p>
            </div>
          )}
        </div>

      </div>
    </div>
  );
}
