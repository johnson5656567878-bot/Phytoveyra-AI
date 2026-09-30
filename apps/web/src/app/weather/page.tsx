'use client';

import React, { useEffect, useState } from 'react';
import { useTranslation } from '@/lib/i18n';
import { api } from '@/lib/api';
import { WeatherData, RiskAlert } from '@/lib/types';
import { 
  CloudRain, Sun, Wind, Droplets, AlertTriangle, MapPin, ShieldCheck, Layers, Activity 
} from 'lucide-react';

export default function WeatherPage() {
  const { t } = useTranslation();
  const [weather, setWeather] = useState<WeatherData | null>(null);
  const [alerts, setAlerts] = useState<RiskAlert[]>([]);

  useEffect(() => {
    api.getWeather().then(setWeather);
    api.getRiskAlerts().then(setAlerts);
  }, []);

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white flex items-center gap-2">
          <CloudRain className="w-8 h-8 text-sky-400" />
          {t('weather.title')} & Disease Risk Map
        </h1>
        <p className="text-sm text-emerald-200/80 mt-1">
          Real-time agricultural weather conditions and localized predictive disease vulnerability alerts.
        </p>
      </div>

      {/* Main Weather Metrics */}
      <div className="glass-panel p-6 rounded-2xl border border-emerald-800/60 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 bg-gradient-to-r from-emerald-950 via-emerald-900 to-teal-950">
        
        <div className="bg-sky-950/50 border border-sky-800/50 p-4 rounded-xl space-y-1">
          <div className="flex items-center justify-between text-xs text-sky-300">
            <span>Air Temperature</span>
            <Sun className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-3xl font-black text-white">{weather?.temperature_c || 28.5}°C</div>
          <p className="text-[11px] text-sky-200/80">Optimal crop growth range</p>
        </div>

        <div className="bg-sky-950/50 border border-sky-800/50 p-4 rounded-xl space-y-1">
          <div className="flex items-center justify-between text-xs text-sky-300">
            <span>Relative Humidity</span>
            <Droplets className="w-4 h-4 text-sky-400" />
          </div>
          <div className="text-3xl font-black text-white">{weather?.humidity_percent || 84}%</div>
          <p className="text-[11px] text-amber-300 font-semibold">High Fungal Incubation</p>
        </div>

        <div className="bg-sky-950/50 border border-sky-800/50 p-4 rounded-xl space-y-1">
          <div className="flex items-center justify-between text-xs text-sky-300">
            <span>24h Rainfall</span>
            <CloudRain className="w-4 h-4 text-sky-400" />
          </div>
          <div className="text-3xl font-black text-white">{weather?.rainfall_mm || 12.4} mm</div>
          <p className="text-[11px] text-sky-200/80">Scattered showers</p>
        </div>

        <div className="bg-sky-950/50 border border-sky-800/50 p-4 rounded-xl space-y-1">
          <div className="flex items-center justify-between text-xs text-sky-300">
            <span>Wind Velocity</span>
            <Wind className="w-4 h-4 text-teal-400" />
          </div>
          <div className="text-3xl font-black text-white">{weather?.wind_speed_kmh || 14.2} km/h</div>
          <p className="text-[11px] text-teal-300">Spore dispersals likely</p>
        </div>

      </div>

      {/* Localized Disease Risk Alerts */}
      <div className="glass-panel p-6 rounded-2xl border border-emerald-800/60 space-y-4">
        <h3 className="text-base font-bold text-white flex items-center gap-2">
          <AlertTriangle className="w-5 h-5 text-amber-400" />
          Predictive Disease & Pest Risk Engine
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {alerts.map((alert) => (
            <div key={alert.id} className="bg-amber-950/40 border border-amber-800/60 p-5 rounded-2xl space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-amber-200">{alert.crop_name}: {alert.disease_pest_name}</span>
                <span className="bg-red-900 text-red-200 text-[10px] font-bold px-2.5 py-0.5 rounded-full border border-red-700">
                  {alert.risk_level}
                </span>
              </div>
              <p className="text-xs text-emerald-200/90 leading-relaxed">
                {alert.reason}
              </p>
              <div className="bg-amber-900/30 p-3 rounded-xl border border-amber-800/40 text-xs text-amber-200 font-semibold">
                🛡️ Recommended Preventive Action: {alert.preventive_action}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Privacy-Preserving Regional Map Widget */}
      <div className="glass-panel p-6 rounded-2xl border border-emerald-800/60 space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <MapPin className="w-5 h-5 text-emerald-400" />
            Regional Aggregated Outbreak Map (Privacy-Preserved)
          </h3>
          <span className="text-xs text-emerald-300">Coimbatore Region</span>
        </div>

        <div className="relative h-64 sm:h-80 rounded-2xl overflow-hidden border border-emerald-700/60 bg-emerald-950 flex items-center justify-center p-4">
          {/* Simulated Geographic Activity Grid */}
          <div className="absolute inset-0 opacity-20 bg-[radial-gradient(#10b981_1px,transparent_1px)] [background-size:16px_16px]" />
          
          <div className="relative z-10 text-center space-y-2">
            <div className="w-12 h-12 rounded-full bg-red-500/20 text-red-400 border border-red-500/40 flex items-center justify-center mx-auto animate-ping">
              <Activity className="w-6 h-6" />
            </div>
            <h4 className="text-sm font-bold text-white">High Fungal Risk Cluster Detected in District Zone 4</h4>
            <p className="text-xs text-emerald-300/80 max-w-md">
              Aggregated statistics show 14 late blight reports within 5km radius. Individual farmer locations remain strictly private.
            </p>
          </div>
        </div>
      </div>

    </div>
  );
}
