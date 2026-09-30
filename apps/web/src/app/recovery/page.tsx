'use client';

import React, { useState, useEffect, Suspense } from 'react';
import { useSearchParams } from 'next/navigation';
import { useTranslation } from '@/lib/i18n';
import { api } from '@/lib/api';
import { BeforeAfterSlider } from '@/components/BeforeAfterSlider';
import { 
  TrendingUp, Sliders, Camera, Upload, CheckCircle2, ArrowRight, Activity, Calendar, FileCheck 
} from 'lucide-react';

function RecoveryContent() {
  const { t } = useTranslation();
  const searchParams = useSearchParams();
  const scanId = searchParams.get('scanId');

  const [scanData, setScanData] = useState<any>(null);
  const [followUpImage, setFollowUpImage] = useState<string | null>(null);
  const [followUpFile, setFollowUpFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadRecoveryData() {
      try {
        if (scanId) {
          const res = await api.getRecoveryByScanId(scanId);
          if (res) {
            setScanData(res);
            if (res.has_followup && res.recovery) {
              setFollowUpImage(res.recovery.followup_image_url);
            }
          }
        } else {
          // Fetch latest scan from backend database
          const scans = await api.getScans();
          if (scans.length > 0) {
            const latestScan = scans[0];
            const res = await api.getRecoveryByScanId(latestScan.id);
            if (res) {
              setScanData(res);
              if (res.has_followup && res.recovery) {
                setFollowUpImage(res.recovery.followup_image_url);
              }
            }
          }
        }
      } catch (err) {
        console.error("Recovery load error", err);
      } finally {
        setLoading(false);
      }
    }
    loadRecoveryData();
  }, [scanId]);

  const handleFollowUpUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0] && scanData) {
      const file = e.target.files[0];
      setFollowUpFile(file);

      const reader = new FileReader();
      reader.onload = async (ev) => {
        const b64 = ev.target?.result as string;
        setFollowUpImage(b64);
        setIsUploading(true);

        try {
          const formData = new FormData();
          formData.append('original_scan_id', scanData.scan_id);
          formData.append('file', file);
          formData.append('notes', 'Follow-up foliage recovery scan');

          const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';
          const res = await fetch(`${API_URL}/recovery/upload`, {
            method: 'POST',
            body: formData
          });

          if (res.ok) {
            const updated = await res.json();
            setScanData({
              ...scanData,
              has_followup: true,
              recovery: updated
            });
          }
        } catch (err) {
          console.error("Upload error", err);
        } finally {
          setIsUploading(false);
        }
      };
      reader.readAsDataURL(file);
    }
  };

  if (loading) {
    return <div className="p-12 text-center text-xs text-emerald-300">Loading Scan Recovery Record...</div>;
  }

  if (!scanData) {
    return (
      <div className="glass-panel p-12 rounded-2xl border border-emerald-800/60 text-center space-y-4 max-w-2xl mx-auto">
        <TrendingUp className="w-12 h-12 text-emerald-500/50 mx-auto" />
        <h3 className="text-base font-bold text-white">No Recovery Scans Available Yet</h3>
        <p className="text-xs text-emerald-300/70">
          Upload a plant photo on the Scan page to begin recovery comparison tracking.
        </p>
        <a
          href="/scan"
          className="inline-flex items-center space-x-2 bg-emerald-500 text-emerald-950 font-bold px-4 py-2.5 rounded-xl text-xs"
        >
          <Camera className="w-4 h-4" />
          <span>Upload Initial Scan</span>
        </a>
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      
      {/* Header */}
      <div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white flex items-center gap-2">
          <TrendingUp className="w-8 h-8 text-emerald-400" />
          {t('recovery.title')} ({scanData.crop_name})
        </h1>
        <p className="text-sm text-emerald-200/80 mt-1">
          {t('recovery.subtitle')}
        </p>
      </div>

      {/* Recovery Metrics & Status Bar */}
      <div className="glass-panel p-6 rounded-2xl border border-emerald-800/60 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 bg-gradient-to-r from-emerald-950 via-emerald-900 to-teal-950">
        
        <div className="bg-emerald-900/60 p-4 rounded-xl border border-emerald-700/60 space-y-1">
          <span className="text-[10px] font-bold uppercase text-emerald-300">Initial Severity</span>
          <div className="text-xl font-bold text-red-300">{scanData.initial_severity}</div>
          <p className="text-[11px] text-emerald-400/60">
            Scanned on {new Date(scanData.initial_date).toLocaleDateString()}
          </p>
        </div>

        <div className="bg-emerald-900/60 p-4 rounded-xl border border-emerald-700/60 space-y-1">
          <span className="text-[10px] font-bold uppercase text-emerald-300">Current Severity</span>
          <div className="text-xl font-bold text-teal-300">
            {scanData.recovery ? scanData.recovery.current_severity : scanData.initial_severity}
          </div>
          <p className="text-[11px] text-teal-400/60">
            {scanData.recovery ? `Updated on ${new Date(scanData.recovery.created_at).toLocaleDateString()}` : "Awaiting follow-up photo"}
          </p>
        </div>

        <div className="bg-emerald-900/60 p-4 rounded-xl border border-emerald-700/60 space-y-1">
          <span className="text-[10px] font-bold uppercase text-emerald-300">Measured Improvement</span>
          <div className="text-xl font-black text-emerald-300">
            {scanData.recovery?.improvement_percentage !== undefined ? `+${scanData.recovery.improvement_percentage}%` : "--"}
          </div>
          <p className="text-[11px] text-emerald-400/60">Lesion Regression</p>
        </div>

        <div className="bg-emerald-900/60 p-4 rounded-xl border border-emerald-700/60 space-y-1">
          <span className="text-[10px] font-bold uppercase text-emerald-300">{t('recovery.status')}</span>
          <div className="inline-block bg-emerald-500 text-emerald-950 font-black px-3 py-1 rounded-full text-xs mt-1">
            {scanData.recovery ? scanData.recovery.recovery_status : "Pending Follow-Up"}
          </div>
          <p className="text-[11px] text-emerald-300/80">Closed-Loop Audit</p>
        </div>

      </div>

      {/* Interactive Visual Before/After Split Image Slider */}
      <div className="glass-panel p-6 rounded-2xl border border-emerald-800/60 space-y-4">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
          <div>
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              <Sliders className="w-5 h-5 text-teal-400" />
              Interactive Visual Comparison Slider
            </h3>
            <p className="text-xs text-emerald-300/80 mt-0.5">
              Comparing your original scan ({new Date(scanData.initial_date).toLocaleDateString()}) with follow-up photo.
            </p>
          </div>

          <label className="cursor-pointer bg-gradient-to-r from-emerald-500 to-teal-400 text-emerald-950 font-bold px-4 py-2.5 rounded-xl text-xs shadow-md hover:scale-105 transition-transform flex items-center gap-1.5 shrink-0">
            <Upload className="w-4 h-4" />
            <span>{followUpImage ? 'Upload Newer Follow-Up Photo' : 'Upload Follow-Up Photo'}</span>
            <input type="file" accept="image/*" onChange={handleFollowUpUpload} className="hidden" />
          </label>
        </div>

        {followUpImage ? (
          <BeforeAfterSlider
            beforeImage={scanData.initial_image_url}
            afterImage={followUpImage}
            beforeLabel={`Original Scan (${new Date(scanData.initial_date).toLocaleDateString()})`}
            afterLabel="Follow-Up Photo"
          />
        ) : (
          <div className="bg-emerald-950/80 border-2 border-dashed border-emerald-700/60 p-12 rounded-2xl text-center space-y-4">
            <Camera className="w-12 h-12 text-emerald-400/50 mx-auto" />
            <div>
              <h4 className="text-base font-bold text-white">No follow-up scan available yet.</h4>
              <p className="text-xs text-emerald-300/70 max-w-sm mx-auto mt-1">
                Upload a new photo of your crop foliage to audit recovery progress against your original scan.
              </p>
            </div>
            <label className="cursor-pointer inline-flex items-center space-x-2 bg-emerald-500 text-emerald-950 font-bold px-5 py-2.5 rounded-xl text-xs shadow-md">
              <Upload className="w-4 h-4" />
              <span>{t('recovery.uploadFollowUp')}</span>
              <input type="file" accept="image/*" onChange={handleFollowUpUpload} className="hidden" />
            </label>
          </div>
        )}

        {/* Computer Vision Analysis Explanation */}
        {scanData.recovery?.analysis_notes && (
          <div className="bg-emerald-900/40 border border-emerald-700/50 p-4 rounded-xl text-xs text-emerald-200/90 leading-relaxed">
            <strong className="text-teal-300">AI Computer Vision Recovery Audit: </strong>
            {scanData.recovery.analysis_notes}
          </div>
        )}
      </div>

    </div>
  );
}

export default function RecoveryPage() {
  return (
    <Suspense fallback={<div className="p-8 text-center text-xs text-emerald-300">Loading Scan Recovery Record...</div>}>
      <RecoveryContent />
    </Suspense>
  );
}
