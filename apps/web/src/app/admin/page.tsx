'use client';

import React, { useState } from 'react';
import { useTranslation } from '@/lib/i18n';
import { 
  Users, Sprout, Camera, Activity, ShieldCheck, Database, BarChart3, Settings, FileText 
} from 'lucide-react';

export default function AdminPage() {
  const { t } = useTranslation();
  const [stats, setStats] = useState({
    total_users: 1284,
    total_farmers: 1210,
    total_experts: 54,
    total_farms: 1420,
    total_scans: 4890,
    ai_model_version: "AgriDoctor-Vision-v2.4",
    avg_ai_confidence: "89.4%",
    low_confidence_rate: "4.2%",
    disease_distribution: [
      { disease: "Fungal Leaf Spots", count: 1420 },
      { disease: "Bacterial Blight", count: 980 },
      { disease: "Pest Infestations", count: 810 },
      { disease: "Nutrient Deficiencies", count: 750 },
      { disease: "Healthy Crops", count: 930 }
    ]
  });

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white flex items-center gap-2">
          <ShieldCheck className="w-8 h-8 text-emerald-400" />
          {t('nav.admin')} Management & AI Telemetry
        </h1>
        <p className="text-sm text-emerald-200/80 mt-1">
          System health monitoring, AI model confidence metrics, and knowledge base management.
        </p>
      </div>

      {/* 4 Metric Overview Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        
        <div className="glass-card p-5 rounded-2xl border border-emerald-700/50 space-y-2">
          <div className="flex items-center justify-between text-xs text-emerald-300">
            <span>Total Farmers</span>
            <Users className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-3xl font-black text-white">{stats.total_farmers}</div>
          <p className="text-[11px] text-emerald-300/80">Active Platform Accounts</p>
        </div>

        <div className="glass-card p-5 rounded-2xl border border-emerald-700/50 space-y-2">
          <div className="flex items-center justify-between text-xs text-emerald-300">
            <span>Total Plant Scans</span>
            <Camera className="w-4 h-4 text-teal-400" />
          </div>
          <div className="text-3xl font-black text-white">{stats.total_scans}</div>
          <p className="text-[11px] text-teal-300">Diagnoses Executed</p>
        </div>

        <div className="glass-card p-5 rounded-2xl border border-emerald-700/50 space-y-2">
          <div className="flex items-center justify-between text-xs text-emerald-300">
            <span>Avg AI Confidence</span>
            <Activity className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-3xl font-black text-emerald-300">{stats.avg_ai_confidence}</div>
          <p className="text-[11px] text-emerald-300/80">Model Calibration Score</p>
        </div>

        <div className="glass-card p-5 rounded-2xl border border-emerald-700/50 space-y-2">
          <div className="flex items-center justify-between text-xs text-emerald-300">
            <span>Model Release</span>
            <Database className="w-4 h-4 text-sky-400" />
          </div>
          <div className="text-lg font-bold text-sky-300">{stats.ai_model_version}</div>
          <p className="text-[11px] text-sky-200/80">Active Production Inference</p>
        </div>

      </div>

      {/* Disease Distribution Table & Knowledge Base Status */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        <div className="glass-panel p-6 rounded-2xl border border-emerald-800/60 space-y-4">
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <BarChart3 className="w-5 h-5 text-teal-400" />
            Disease & Outbreak Distribution
          </h3>

          <div className="space-y-3">
            {stats.disease_distribution.map((item, idx) => (
              <div key={idx} className="space-y-1">
                <div className="flex justify-between text-xs text-emerald-200">
                  <span>{item.disease}</span>
                  <span className="font-bold">{item.count} scans</span>
                </div>
                <div className="w-full bg-emerald-950 h-2 rounded-full overflow-hidden border border-emerald-800">
                  <div
                    className="bg-emerald-400 h-full rounded-full"
                    style={{ width: `${Math.round((item.count / 1420) * 100)}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="glass-panel p-6 rounded-2xl border border-emerald-800/60 space-y-4">
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <FileText className="w-5 h-5 text-emerald-400" />
            Knowledge Base & RAG Telemetry
          </h3>

          <div className="space-y-3 text-xs text-emerald-200/90">
            <div className="bg-emerald-950/80 border border-emerald-800/60 p-3.5 rounded-xl flex items-center justify-between">
              <span>Ingested Agricultural Documents:</span>
              <strong className="text-white">1,480 Docs</strong>
            </div>

            <div className="bg-emerald-950/80 border border-emerald-800/60 p-3.5 rounded-xl flex items-center justify-between">
              <span>Verified Treatment Knowledge Entries:</span>
              <strong className="text-white">620 Pathogens</strong>
            </div>

            <div className="bg-emerald-950/80 border border-emerald-800/60 p-3.5 rounded-xl flex items-center justify-between">
              <span>Vector Embedding Dimension:</span>
              <strong className="text-teal-300">1536 (pgvector)</strong>
            </div>

            <div className="bg-emerald-950/80 border border-emerald-800/60 p-3.5 rounded-xl flex items-center justify-between">
              <span>Uncertainty Safety Escalations:</span>
              <strong className="text-amber-300">{stats.low_confidence_rate}</strong>
            </div>
          </div>
        </div>

      </div>

    </div>
  );
}
