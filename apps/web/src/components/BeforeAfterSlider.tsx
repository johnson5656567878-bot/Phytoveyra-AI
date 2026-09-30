'use client';

import React, { useState } from 'react';
import { Sparkles, Sliders } from 'lucide-react';

interface BeforeAfterProps {
  beforeImage: string;
  afterImage: string;
  beforeLabel?: string;
  afterLabel?: string;
}

export const BeforeAfterSlider: React.FC<BeforeAfterProps> = ({
  beforeImage,
  afterImage,
  beforeLabel = 'Initial Diagnosis (Before)',
  afterLabel = 'Follow-Up Recovery (After)'
}) => {
  const [sliderPosition, setSliderPosition] = useState(50);
  const [isDragging, setIsDragging] = useState(false);

  const handleMove = (clientX: number, rect: DOMRect) => {
    const x = clientX - rect.left;
    let pos = (x / rect.width) * 100;
    if (pos < 0) pos = 0;
    if (pos > 100) pos = 100;
    setSliderPosition(pos);
  };

  const handleTouchMove = (e: React.TouchEvent<HTMLDivElement>) => {
    const rect = e.currentTarget.getBoundingClientRect();
    handleMove(e.touches[0].clientX, rect);
  };

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!isDragging) return;
    const rect = e.currentTarget.getBoundingClientRect();
    handleMove(e.clientX, rect);
  };

  return (
    <div className="w-full space-y-3">
      <div
        className="relative w-full h-[380px] sm:h-[450px] rounded-2xl overflow-hidden shadow-xl border border-emerald-800/40 select-none cursor-ew-resize bg-emerald-950"
        onMouseDown={() => setIsDragging(true)}
        onMouseUp={() => setIsDragging(false)}
        onMouseLeave={() => setIsDragging(false)}
        onMouseMove={handleMouseMove}
        onTouchMove={handleTouchMove}
      >
        {/* After Image (Background layer) */}
        <img
          src={afterImage}
          alt="After Recovery"
          className="absolute inset-0 w-full h-full object-cover"
        />

        {/* Before Image (Clipped overlay layer) */}
        <div
          className="absolute inset-y-0 left-0 overflow-hidden"
          style={{ width: `${sliderPosition}%` }}
        >
          <img
            src={beforeImage}
            alt="Before Treatment"
            className="absolute top-0 left-0 w-full h-full object-cover max-w-none"
            style={{ width: '100%', height: '100%' }}
          />
        </div>

        {/* Labels Overlay */}
        <div className="absolute top-3 left-3 bg-red-950/80 backdrop-blur-md text-red-200 border border-red-700/50 text-xs font-semibold px-3 py-1 rounded-full shadow-md">
          {beforeLabel}
        </div>
        <div className="absolute top-3 right-3 bg-emerald-950/80 backdrop-blur-md text-emerald-200 border border-emerald-700/50 text-xs font-semibold px-3 py-1 rounded-full shadow-md">
          {afterLabel}
        </div>

        {/* Divider Slider Handle */}
        <div
          className="absolute top-0 bottom-0 w-1 bg-white shadow-2xl z-20 flex items-center justify-center"
          style={{ left: `${sliderPosition}%` }}
        >
          <div className="w-9 h-9 rounded-full bg-emerald-500 text-emerald-950 flex items-center justify-center shadow-lg border-2 border-white transform hover:scale-110 transition-transform">
            <Sliders className="w-4 h-4 stroke-[3]" />
          </div>
        </div>
      </div>

      <div className="flex items-center justify-between text-xs text-emerald-300/80 px-2 font-medium">
        <span>👈 Drag slider left/right to compare plant foliage recovery</span>
        <span>{Math.round(sliderPosition)}% View Split</span>
      </div>
    </div>
  );
};
