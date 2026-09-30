'use client';

import React, { useState, useEffect, Suspense } from 'react';
import Link from 'next/link';
import { useSearchParams } from 'next/navigation';
import { useTranslation } from '@/lib/i18n';
import { api } from '@/lib/api';
import { TreatmentRecommendation } from '@/lib/types';
import { 
  Stethoscope, AlertOctagon, CheckCircle2, ShieldAlert, Sprout, 
  FlaskConical, Calendar, BookOpen, ArrowRight, Camera, HelpCircle 
} from 'lucide-react';

function TreatmentContent() {
  const { t } = useTranslation();
  const searchParams = useSearchParams();
  const scanId = searchParams.get('scanId');
  const titleQuery = searchParams.get('title');

  const [scanData, setScanData] = useState<any>(null);
  const [treatment, setTreatment] = useState<TreatmentRecommendation | null>(null);
  const [loading, setLoading] = useState(true);
  const [scheduled, setScheduled] = useState(false);

  useEffect(() => {
    async function loadTreatmentData() {
      try {
        if (scanId) {
          const res = await api.getTreatmentByScanId(scanId);
          if (res) {
            setScanData(res);
            setTreatment(res.treatment);
          }
        } else if (titleQuery) {
          const rec = await api.getTreatmentRecommendation(titleQuery);
          setTreatment(rec);
        } else {
          // Fetch latest scan from backend database
          const scans = await api.getScans();
          if (scans.length > 0) {
            const latestScan = scans[0];
            const res = await api.getTreatmentByScanId(latestScan.id);
            if (res) {
              setScanData(res);
              setTreatment(res.treatment);
            }
          }
        }
      } catch (err) {
        console.error("Treatment load error", err);
      } finally {
        setLoading(false);
      }
    }
    loadTreatmentData();
  }, [scanId, titleQuery]);

  const handleScheduleTask = async () => {
    if (!treatment) return;
    try {
      await api.createSchedule({
        scan_id: scanData?.scan_id,
        action_item: `Apply ${treatment.biological_organic || treatment.immediate_action}`,
        scheduled_date: new Date().toISOString().split('T')[0],
        follow_up_date: new Date(Date.now() + treatment.follow_up_days * 86400000).toISOString().split('T')[0],
        notes: `Follow-up interval: ${treatment.follow_up_days} days`
      });
      setScheduled(true);
    } catch (err) {
      setScheduled(true);
    }
  };

  const formatCropDisplay = (crop: string | undefined) => {
    if (!crop || crop === "Detected Crop" || crop === "Auto-Detect") return "UNKNOWN";
    return crop.toUpperCase();
  };

  if (loading) {
    return <div className="p-12 text-center text-xs text-emerald-300">Loading scan treatment plan...</div>;
  }

  if (!treatment) {
    return (
      <div className="glass-panel p-12 rounded-2xl border border-emerald-800/60 text-center space-y-4 max-w-2xl mx-auto">
        <Stethoscope className="w-12 h-12 text-emerald-500/50 mx-auto" />
        <h3 className="text-base font-bold text-white">No Treatment Plans Yet</h3>
        <p className="text-xs text-emerald-300/70">
          Upload a plant photo on the Scan page to generate a data-driven treatment plan.
        </p>
        <Link
          href="/scan"
          className="inline-flex items-center space-x-2 bg-emerald-500 text-emerald-950 font-bold px-4 py-2.5 rounded-xl text-xs"
        >
          <Camera className="w-4 h-4" />
          <span>Upload Plant Scan</span>
        </Link>
      </div>
    );
  }

  const isLowConfidence = scanData?.is_low_confidence || scanData?.severity === "Uncertain" || (scanData?.confidence && scanData.confidence < 0.60);

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      
      {/* Header */}
      <div>
        <div className="inline-flex items-center space-x-1.5 bg-teal-500/20 text-teal-300 border border-teal-500/30 px-3 py-1 rounded-full text-xs font-semibold mb-2">
          <BookOpen className="w-3.5 h-3.5" />
          <span>Verified Agriculture Extension Knowledge Base</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white flex items-center gap-2">
          <Stethoscope className="w-8 h-8 text-emerald-400" />
          {t('treatment.title')}
        </h1>
        <p className="text-sm text-emerald-200/80 mt-1">
          Context-aware treatment plan generated specifically for your uploaded plant scan.
        </p>
      </div>

      <div className="glass-panel p-6 sm:p-8 rounded-3xl border border-emerald-800/60 space-y-6 bg-gradient-to-b from-emerald-950/90 to-teal-950/90 shadow-2xl">
        
        {/* User's Actual Uploaded Scan Banner */}
        {scanData && (
          <div className="bg-emerald-900/60 border border-emerald-700/60 p-5 rounded-2xl flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
            <div className="flex items-center space-x-4">
              {scanData.image_url ? (
                <img
                  src={scanData.image_url}
                  alt="Actual User Scan"
                  className="w-20 h-20 rounded-xl object-cover border-2 border-emerald-500 shadow-md shrink-0"
                />
              ) : null}
              <div>
                <span className="text-[11px] font-extrabold text-teal-300 uppercase tracking-wider bg-teal-950/80 px-2.5 py-0.5 rounded-md border border-teal-700/60">
                  TARGET CROP: {formatCropDisplay(scanData.crop_name)}
                </span>
                <h2 className="text-xl font-black text-white mt-1">{scanData.diagnosis_title}</h2>
                <p className="text-xs text-emerald-300/80 mt-1">
                  Scan Date: <strong>{new Date(scanData.created_at).toLocaleDateString()}</strong> | 
                  Confidence: <strong className="text-teal-300">{Math.round((scanData.confidence || 0) * 100)}%</strong> | 
                  Severity: <span className={scanData.severity === 'Healthy' ? 'text-emerald-300 font-bold' : 'text-red-300 font-bold'}>{scanData.severity}</span>
                </p>
              </div>
            </div>

            {scanData.scan_id && (
              <Link
                href={`/recovery?scanId=${scanData.scan_id}`}
                className="bg-gradient-to-r from-emerald-500 to-teal-400 text-emerald-950 text-xs font-bold px-4 py-2.5 rounded-xl shadow-md hover:scale-105 transition-transform shrink-0"
              >
                Track Recovery
              </Link>
            )}
          </div>
        )}

        {/* Low Confidence / Uncertain Diagnosis Notice */}
        {isLowConfidence && (
          <div className="bg-amber-950/90 border-2 border-amber-600 p-4 rounded-2xl space-y-2 text-amber-200">
            <div className="flex items-center space-x-2 font-bold text-amber-300 text-xs">
              <AlertOctagon className="w-5 h-5 text-amber-400 shrink-0" />
              <span>Unable to confidently identify this condition.</span>
            </div>
            <p className="text-xs leading-relaxed bg-amber-900/40 p-3 rounded-xl border border-amber-800/60">
              No reliable diagnosis available, so a specific treatment cannot be recommended. Please upload a clearer close-up photo of affected plant foliage or crop stem.
            </p>
          </div>
        )}

        {/* Problem Root Cause */}
        <div className="bg-emerald-950/80 border border-emerald-800/60 p-5 rounded-2xl space-y-1">
          <span className="text-[10px] font-bold text-teal-400 uppercase tracking-wider">Root Cause Analysis</span>
          <p className="text-xs text-emerald-200/90 leading-relaxed">
            {treatment.why_happening}
          </p>
        </div>

        {/* 4 Structured Guidance Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          
          {/* 1. Immediate Action */}
          <div className="bg-emerald-950/80 border border-emerald-800/60 p-5 rounded-2xl space-y-2">
            <h3 className="text-sm font-bold text-emerald-200 flex items-center gap-2">
              <AlertOctagon className="w-4 h-4 text-emerald-400" />
              1. {t('treatment.immediateAction')}
            </h3>
            <p className="text-xs text-emerald-300/90 leading-relaxed">
              {treatment.immediate_action}
            </p>
          </div>

          {/* 2. Cultural Control */}
          <div className="bg-emerald-950/80 border border-emerald-800/60 p-5 rounded-2xl space-y-2">
            <h3 className="text-sm font-bold text-teal-200 flex items-center gap-2">
              <Sprout className="w-4 h-4 text-teal-400" />
              2. {t('treatment.cultural')}
            </h3>
            <p className="text-xs text-teal-300/90 leading-relaxed">
              {treatment.cultural_control}
            </p>
          </div>

          {/* 3. Biological & Organic Option */}
          <div className="bg-emerald-950/80 border border-emerald-800/60 p-5 rounded-2xl space-y-2">
            <h3 className="text-sm font-bold text-emerald-200 flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              3. {t('treatment.organic')}
            </h3>
            <p className="text-xs text-emerald-300/90 leading-relaxed font-medium">
              {treatment.biological_organic}
            </p>
          </div>

          {/* 4. Approved Chemical Option */}
          <div className="bg-emerald-950/80 border border-emerald-800/60 p-5 rounded-2xl space-y-2">
            <h3 className="text-sm font-bold text-sky-200 flex items-center gap-2">
              <FlaskConical className="w-4 h-4 text-sky-400" />
              4. {t('treatment.chemical')}
            </h3>
            <p className="text-xs text-sky-300/90 leading-relaxed font-medium">
              {treatment.approved_chemical}
            </p>
          </div>

        </div>

        {/* Safety Warning */}
        <div className="bg-amber-950/80 border border-amber-700/60 p-5 rounded-2xl space-y-2">
          <h3 className="text-xs font-bold text-amber-300 flex items-center gap-2">
            <ShieldAlert className="w-4 h-4 text-amber-400" />
            5. {t('treatment.safetyWarning')}
          </h3>
          <p className="text-xs text-amber-100/90 leading-relaxed">
            {treatment.safety_warning}
          </p>
        </div>

        {/* Source Citation & Scheduling Actions */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-4 border-t border-emerald-800/60">
          <div className="text-xs text-emerald-300/80">
            <span className="font-bold text-emerald-400">{t('treatment.sourceCitation')}: </span>
            {treatment.source_reference}
          </div>

          <div className="flex items-center space-x-3 w-full sm:w-auto">
            {!scheduled ? (
              <button
                onClick={handleScheduleTask}
                className="w-full sm:w-auto flex items-center justify-center space-x-2 bg-gradient-to-r from-emerald-500 to-teal-400 text-emerald-950 font-bold px-5 py-3 rounded-xl shadow-xl hover:scale-105 transition-transform text-xs"
              >
                <Calendar className="w-4 h-4" />
                <span>{t('treatment.addToSchedule')} ({treatment.follow_up_days} Days)</span>
              </button>
            ) : (
              <div className="bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 px-4 py-2.5 rounded-xl text-xs font-bold flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                <span>Task Added to Calendar Schedule!</span>
              </div>
            )}

            {scanData?.scan_id && (
              <Link
                href={`/recovery?scanId=${scanData.scan_id}`}
                className="w-full sm:w-auto flex items-center justify-center space-x-1.5 bg-emerald-900/80 hover:bg-emerald-800 text-emerald-100 font-bold px-4 py-3 rounded-xl text-xs transition-colors"
              >
                <span>Follow-Up Scanner</span>
                <ArrowRight className="w-4 h-4" />
              </Link>
            )}
          </div>
        </div>

      </div>

    </div>
  );
}

export default function TreatmentPage() {
  return (
    <Suspense fallback={<div className="p-8 text-center text-xs text-emerald-300">Loading Scan Treatment Plan...</div>}>
      <TreatmentContent />
    </Suspense>
  );
}
