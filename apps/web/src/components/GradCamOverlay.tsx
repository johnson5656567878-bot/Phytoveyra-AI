'use client';

import React, { useState } from 'react';
import { Eye, EyeOff, Layers, Sparkles } from 'lucide-react';

interface GradCamProps {
  originalImage: string;
  heatmapImage?: string;
  explanation?: string;
}

export const GradCamOverlay: React.FC<GradCamProps> = ({
  originalImage,
  heatmapImage,
  explanation
}) => {
  const [showHeatmap, setShowHeatmap] = useState(true);

  return (
    <div className="space-y-3 bg-emerald-950/60 border border-emerald-800/60 rounded-2xl p-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <Layers className="w-5 h-5 text-teal-400" />
          <h4 className="text-sm font-bold text-emerald-100">
            Explainable AI: Grad-CAM Feature Visualizer
          </h4>
        </div>

        <button
          onClick={() => setShowHeatmap(!showHeatmap)}
          className={`flex items-center space-x-1.5 text-xs font-semibold px-3 py-1.5 rounded-xl border transition-all ${
            showHeatmap
              ? 'bg-teal-500 text-teal-950 border-teal-400 shadow-md font-bold'
              : 'bg-emerald-900/60 text-emerald-200 border-emerald-700/60 hover:bg-emerald-800/60'
          }`}
        >
          {showHeatmap ? <Eye className="w-4 h-4" /> : <EyeOff className="w-4 h-4" />}
          <span>{showHeatmap ? 'Heatmap Active' : 'Show Heatmap'}</span>
        </button>
      </div>

      {/* Image Preview Container */}
      <div className="relative h-64 sm:h-80 rounded-xl overflow-hidden bg-black border border-emerald-800/40">
        <img
          src={showHeatmap && heatmapImage ? heatmapImage : originalImage}
          alt="Plant Scan Analysis"
          className="w-full h-full object-cover transition-opacity duration-300"
        />

        {showHeatmap && (
          <div className="absolute bottom-3 left-3 bg-teal-950/90 text-teal-200 border border-teal-600/60 text-[11px] px-2.5 py-1 rounded-lg flex items-center space-x-1.5 shadow-md">
            <span className="w-2 h-2 rounded-full bg-red-500 animate-pulse" />
            <span>Red/Yellow zones highlight AI attention focus</span>
          </div>
        )}
      </div>

      {explanation && (
        <p className="text-xs text-emerald-200/90 leading-relaxed bg-emerald-900/40 p-3 rounded-xl border border-emerald-800/40">
          <span className="font-bold text-teal-300">Model Focus Reasoning: </span>
          {explanation}
        </p>
      )}
    </div>
  );
};
