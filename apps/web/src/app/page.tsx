'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { useTranslation } from '@/lib/i18n';
import { api } from '@/lib/api';
import { Crop, WeatherData, RiskAlert, TreatmentSchedule, PlantScan } from '@/lib/types';
import { VoiceAssistantBar } from '@/components/VoiceAssistantBar';
import { 
  Sprout, Camera, AlertTriangle, CloudRain, Calendar, Activity, 
  TrendingUp, ArrowRight, ShieldCheck, CheckCircle2, Clock, Sparkles, Stethoscope, ChevronRight 
} from 'lucide-react';

function processRecentScans(rawScans: PlantScan[]): PlantScan[] {
  if (!Array.isArray(rawScans)) return [];

  // Deduplicate strictly by stable unique scan.id
  const seenIds = new Set<string>();
  const uniqueScans: PlantScan[] = [];

  for (const scan of rawScans) {
    if (!scan || !scan.id) continue;
    if (!seenIds.has(scan.id)) {
      seenIds.add(scan.id);
      uniqueScans.push(scan);
    }
  }

  // Sort by scan date/time in descending order (newest first)
  uniqueScans.sort((a, b) => {
    const timeA = a.created_at ? new Date(a.created_at).getTime() : 0;
    const timeB = b.created_at ? new Date(b.created_at).getTime() : 0;
    return timeB - timeA;
  });

  // Limit to ONLY the latest 10
  return uniqueScans.slice(0, 10);
}

export default function DashboardPage() {
  const { t } = useTranslation();
  const [crops, setCrops] = useState<Crop[]>([]);
  const [weather, setWeather] = useState<WeatherData | null>(null);
  const [alerts, setAlerts] = useState<RiskAlert[]>([]);
  const [schedules, setSchedules] = useState<TreatmentSchedule[]>([]);
  const [scans, setScans] = useState<PlantScan[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadDashboardData() {
      try {
        const [cData, wData, aData, sData, scData] = await Promise.all([
          api.getCrops(),
          api.getWeather(),
          api.getRiskAlerts(),
          api.getSchedules(),
          api.getScans()
        ]);
        setCrops(cData);
        setWeather(wData);
        setAlerts(aData);
        setSchedules(sData);
        setScans(processRecentScans(scData));
      } catch (err) {
        console.error("Dashboard data load error", err);
      } finally {
        setLoading(false);
      }
    }
    loadDashboardData();
  }, []);

  const healthyCropsCount = crops.filter(c => c.health_status === 'Healthy').length;
  const healthPct = crops.length > 0 ? Math.round((healthyCropsCount / crops.length) * 100) : 0;

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      
      {/* Top Banner Header */}
      <div className="glass-panel p-6 sm:p-8 rounded-3xl border border-emerald-800/60 relative overflow-hidden bg-gradient-to-r from-emerald-950 via-emerald-900 to-teal-950 shadow-2xl">
        <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-6 relative z-10">
          <div>
            <div className="inline-flex items-center space-x-2 bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 px-3 py-1 rounded-full text-xs font-semibold mb-3">
              <Sparkles className="w-3.5 h-3.5" />
              <span>Data-Driven Plant Health Platform</span>
            </div>
            <h1 className="text-2xl sm:text-4xl font-extrabold text-white tracking-tight">
              {t('dashboard.title')}
            </h1>
            <p className="text-sm text-emerald-200/90 mt-1 max-w-2xl">
              Closed-Loop AI Healthcare: Upload actual plant photos → Get real AI diagnosis → Follow source-backed treatment → Track recovery.
            </p>
          </div>

          <div className="flex items-center space-x-3 w-full sm:w-auto">
            <Link
              href="/scan"
              className="flex-1 sm:flex-initial flex items-center justify-center space-x-2 bg-gradient-to-r from-emerald-500 to-teal-400 text-emerald-950 font-extrabold px-5 py-3 rounded-2xl shadow-xl hover:scale-105 transition-transform text-sm"
            >
              <Camera className="w-5 h-5 stroke-[2.5]" />
              <span>{t('dashboard.quickScan')}</span>
            </Link>
            
            <Link
              href="/assistant"
              className="flex-1 sm:flex-initial flex items-center justify-center space-x-2 bg-emerald-900/80 border border-emerald-700 text-emerald-200 font-semibold px-4 py-3 rounded-2xl hover:bg-emerald-800/80 transition-colors text-sm"
            >
              <Stethoscope className="w-5 h-5 text-teal-400" />
              <span>Ask AI Chat</span>
            </Link>
          </div>
        </div>
      </div>

      {/* Voice Assistant Quick Microphone Bar */}
      <VoiceAssistantBar />

      {/* 6 Key Dashboard Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
        
        {/* 1. Crop Health */}
        <div className="glass-card p-4 rounded-2xl border border-emerald-700/50 space-y-2">
          <div className="flex items-center justify-between text-emerald-300">
            <span className="text-xs font-semibold">{t('dashboard.cropHealthStatus')}</span>
            <Sprout className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-black text-white">
            {crops.length > 0 ? `${healthPct}%` : "No data"}
          </div>
          {crops.length > 0 ? (
            <div className="w-full bg-emerald-950 h-2 rounded-full overflow-hidden border border-emerald-800">
              <div className="bg-emerald-400 h-full rounded-full transition-all" style={{ width: `${healthPct}%` }} />
            </div>
          ) : null}
          <p className="text-[11px] text-emerald-300/80">
            {crops.length > 0 ? `${healthyCropsCount} of ${crops.length} crops healthy` : "No crops added yet"}
          </p>
        </div>

        {/* 2. Active Treatments */}
        <div className="glass-card p-4 rounded-2xl border border-emerald-700/50 space-y-2">
          <div className="flex items-center justify-between text-emerald-300">
            <span className="text-xs font-semibold">{t('dashboard.activeTreatments')}</span>
            <Activity className="w-4 h-4 text-teal-400" />
          </div>
          <div className="text-2xl font-black text-white">{schedules.length}</div>
          <p className="text-[11px] text-teal-300">
            {schedules.length > 0 ? `${schedules.length} Active Plan(s)` : "No active plans"}
          </p>
        </div>

        {/* 3. Upcoming Tasks */}
        <div className="glass-card p-4 rounded-2xl border border-emerald-700/50 space-y-2">
          <div className="flex items-center justify-between text-emerald-300">
            <span className="text-xs font-semibold">{t('dashboard.upcomingTasks')}</span>
            <Calendar className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-black text-white">{schedules.filter(s => s.status === 'Pending').length}</div>
          <p className="text-[11px] text-amber-300">
            {schedules.length > 0 ? "Scheduled Tasks" : "No upcoming tasks"}
          </p>
        </div>

        {/* 4. Weather */}
        <div className="glass-card p-4 rounded-2xl border border-emerald-700/50 space-y-2">
          <div className="flex items-center justify-between text-emerald-300">
            <span className="text-xs font-semibold">{t('dashboard.weatherWidget')}</span>
            <CloudRain className="w-4 h-4 text-sky-400" />
          </div>
          <div className="text-2xl font-black text-white">
            {weather ? `${weather.temperature_c}°C` : "--°C"}
          </div>
          <p className="text-[11px] text-sky-300">
            {weather ? `${weather.humidity_percent}% Humidity` : "Loading weather..."}
          </p>
        </div>

        {/* 5. Disease Alerts */}
        <div className="glass-card p-4 rounded-2xl border border-emerald-700/50 space-y-2">
          <div className="flex items-center justify-between text-emerald-300">
            <span className="text-xs font-semibold">{t('dashboard.diseaseAlerts')}</span>
            <AlertTriangle className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-2xl font-black text-amber-300">{alerts.length}</div>
          <p className="text-[11px] text-amber-200/80">
            {alerts.length > 0 ? `${alerts.length} Active Alert(s)` : "No active alerts"}
          </p>
        </div>

        {/* 6. Recovery Progress */}
        <div className="glass-card p-4 rounded-2xl border border-emerald-700/50 space-y-2">
          <div className="flex items-center justify-between text-emerald-300">
            <span className="text-xs font-semibold">{t('dashboard.recoveryProgress')}</span>
            <TrendingUp className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-black text-emerald-300">
            {scans.length > 0 ? "Tracking" : "0"}
          </div>
          <p className="text-[11px] text-emerald-300">
            {scans.length > 0 ? `${scans.length} Scan(s) Logged` : "No recovery scans yet"}
          </p>
        </div>

      </div>

      {/* Main Grid: Scans + Weather & Risk Alerts */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Left Column (2 Cols): Scans & Treatment Schedule */}
        <div className="lg:col-span-2 space-y-6">
          
          {/* Recent Plant Scans */}
          <div className="glass-panel p-6 rounded-2xl border border-emerald-800/60 space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-base font-bold text-emerald-100 flex items-center gap-2">
                <Camera className="w-5 h-5 text-emerald-400" />
                {t('dashboard.recentScans')}
              </h3>
              <Link href="/scan" className="text-xs font-bold text-emerald-400 hover:underline flex items-center gap-1">
                <span>New Scan</span>
                <ChevronRight className="w-3.5 h-3.5" />
              </Link>
            </div>

            {scans.length === 0 ? (
              <div className="bg-emerald-950/40 border border-emerald-800/50 p-8 rounded-xl text-center space-y-3">
                <Camera className="w-10 h-10 text-emerald-500/50 mx-auto" />
                <p className="text-sm font-bold text-white">No plant scans yet.</p>
                <p className="text-xs text-emerald-300/70">Upload a plant photo to begin real AI diagnosis.</p>
                <Link
                  href="/scan"
                  className="inline-flex items-center space-x-2 bg-emerald-500 text-emerald-950 font-bold px-4 py-2 rounded-xl text-xs mt-2"
                >
                  <Camera className="w-4 h-4" />
                  <span>Scan Crop Now</span>
                </Link>
              </div>
            ) : (
              <div className="space-y-3">
                {scans.map((scan) => (
                  <div key={scan.id} className="bg-emerald-950/70 border border-emerald-800/60 rounded-xl p-4 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 hover:border-emerald-700 transition-colors">
                    <div className="flex items-center space-x-4">
                      {scan.image_url ? (
                        <img
                          src={scan.image_url}
                          alt="User Plant Scan"
                          className="w-16 h-16 rounded-xl object-cover border border-emerald-700/60"
                        />
                      ) : (
                        <div className="w-16 h-16 rounded-xl bg-emerald-900 flex items-center justify-center text-emerald-400">
                          <Camera className="w-6 h-6" />
                        </div>
                      )}
                      <div>
                        <div className="flex items-center space-x-2">
                          <span className="text-sm font-bold text-white">
                            {scan.crop_name}: {scan.diagnosis?.title || "AI Scan Result"}
                          </span>
                          {scan.diagnosis?.severity && (
                            <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${
                              scan.diagnosis.severity === 'Healthy' 
                                ? 'bg-emerald-950 text-emerald-300 border-emerald-700'
                                : 'bg-red-950 text-red-300 border-red-700/60'
                            }`}>
                              {scan.diagnosis.severity}
                            </span>
                          )}
                        </div>
                        <p className="text-xs text-emerald-300/80 mt-0.5">
                          AI Confidence: <strong className="text-teal-300">{Math.round((scan.diagnosis?.confidence || 0) * 100)}%</strong>
                        </p>
                        <p className="text-[11px] text-emerald-400/60 mt-1">
                          Scanned on {new Date(scan.created_at).toLocaleDateString()}
                        </p>
                      </div>
                    </div>

                    <div className="flex items-center space-x-2 w-full sm:w-auto justify-end">
                      <Link
                        href={`/treatment?scanId=${scan.id}`}
                        className="bg-emerald-800/80 hover:bg-emerald-700 text-emerald-100 text-xs font-bold px-3.5 py-2 rounded-xl transition-colors"
                      >
                        View Treatment
                      </Link>
                      <Link
                        href={`/recovery?scanId=${scan.id}`}
                        className="bg-gradient-to-r from-emerald-500 to-teal-400 text-emerald-950 text-xs font-bold px-3.5 py-2 rounded-xl shadow-md hover:scale-105 transition-transform"
                      >
                        Track Recovery
                      </Link>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Treatment Tasks & Reminders */}
          <div className="glass-panel p-6 rounded-2xl border border-emerald-800/60 space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-base font-bold text-emerald-100 flex items-center gap-2">
                <Clock className="w-5 h-5 text-teal-400" />
                {t('dashboard.upcomingTasks')}
              </h3>
            </div>

            {schedules.length === 0 ? (
              <div className="bg-emerald-950/40 border border-emerald-800/50 p-6 rounded-xl text-center text-xs text-emerald-300/70">
                No upcoming tasks. Schedule treatment tasks from your scan diagnosis.
              </div>
            ) : (
              <div className="space-y-3">
                {schedules.map((sched) => (
                  <div key={sched.id} className="bg-emerald-950/60 border border-emerald-800/50 rounded-xl p-4 flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <div className="w-9 h-9 rounded-xl bg-teal-500/20 text-teal-300 border border-teal-500/30 flex items-center justify-center">
                        <CheckCircle2 className="w-5 h-5" />
                      </div>
                      <div>
                        <h4 className="text-xs font-bold text-white">{sched.action_item}</h4>
                        <p className="text-[11px] text-emerald-300/70">Scheduled: {sched.scheduled_date} | Notes: {sched.notes || 'Routine task'}</p>
                      </div>
                    </div>
                    <span className="text-[10px] font-bold bg-amber-950 text-amber-300 border border-amber-700/60 px-2.5 py-1 rounded-full">
                      {sched.status}
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>

        </div>

        {/* Right Column (1 Col): Weather & Risk Alerts */}
        <div className="space-y-6">
          
          {/* Weather Widget */}
          <div className="glass-panel p-6 rounded-2xl border border-emerald-800/60 space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-base font-bold text-emerald-100 flex items-center gap-2">
                <CloudRain className="w-5 h-5 text-sky-400" />
                {t('dashboard.weatherWidget')}
              </h3>
              <span className="text-xs text-sky-300">{weather?.location_name || 'Coimbatore'}</span>
            </div>

            <div className="bg-sky-950/40 border border-sky-800/50 rounded-xl p-4 space-y-3">
              <div className="flex items-center justify-between">
                <div>
                  <span className="text-3xl font-black text-white">{weather?.temperature_c || '--'}°C</span>
                  <p className="text-xs text-sky-200/80">{weather?.forecast_text || 'Loading forecast...'}</p>
                </div>
                <div className="text-right text-xs text-sky-300 space-y-1">
                  <div>Humidity: <strong>{weather?.humidity_percent || '--'}%</strong></div>
                  <div>Rainfall: <strong>{weather?.rainfall_mm || '--'} mm</strong></div>
                  <div>Wind: <strong>{weather?.wind_speed_kmh || '--'} km/h</strong></div>
                </div>
              </div>

              {weather?.warning && (
                <div className="bg-amber-950/80 border border-amber-700/60 p-2.5 rounded-lg text-xs text-amber-200 flex items-start space-x-2">
                  <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
                  <span>{weather.warning}</span>
                </div>
              )}
            </div>
          </div>

          {/* Disease Risk Alerts */}
          <div className="glass-panel p-6 rounded-2xl border border-emerald-800/60 space-y-4">
            <h3 className="text-base font-bold text-emerald-100 flex items-center gap-2">
              <AlertTriangle className="w-5 h-5 text-amber-400" />
              {t('dashboard.diseaseAlerts')}
            </h3>

            {alerts.length === 0 ? (
              <div className="bg-emerald-950/40 border border-emerald-800/50 p-6 rounded-xl text-center text-xs text-emerald-300/70">
                No active crop health alerts. Add or scan crops to see crop-specific risk alerts.
              </div>
            ) : (
              <div className="space-y-3">
                {alerts.map((alert) => (
                  <div key={alert.id} className="bg-amber-950/40 border border-amber-800/60 rounded-xl p-4 space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-bold text-amber-200">{alert.crop_name}: {alert.disease_pest_name}</span>
                      <span className="bg-red-900 text-red-200 text-[10px] font-bold px-2 py-0.5 rounded-full border border-red-700">
                        {alert.risk_level}
                      </span>
                    </div>
                    <p className="text-xs text-emerald-200/90 leading-relaxed">
                      {alert.reason}
                    </p>
                    <p className="text-xs text-amber-300/90 font-semibold bg-amber-900/30 p-2 rounded-lg border border-amber-800/40">
                      💡 Action: {alert.preventive_action}
                    </p>
                  </div>
                ))}
              </div>
            )}
          </div>

        </div>

      </div>
    </div>
  );
}
