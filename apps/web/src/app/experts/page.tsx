'use client';

import React, { useState } from 'react';
import { useTranslation } from '@/lib/i18n';
import { 
  UserCheck, MessageSquare, Plus, CheckCircle2, AlertCircle, Send, Image as ImageIcon 
} from 'lucide-react';

interface ExpertReq {
  id: string;
  crop_name: string;
  farmer_name: string;
  question: string;
  image_url?: string;
  status: 'Open' | 'Answered' | 'Closed';
  created_at: string;
  answers: {
    id: string;
    expert_name: string;
    response_text: string;
    recommended_action?: string;
    created_at: string;
  }[];
}

export default function ExpertsPage() {
  const { t } = useTranslation();
  const [requests, setRequests] = useState<ExpertReq[]>([]);

  const [showSubmitModal, setShowSubmitModal] = useState(false);
  const [questionText, setQuestionText] = useState("");
  const [cropName, setCropName] = useState("");

  const handleSubmitQuestion = (e: React.FormEvent) => {
    e.preventDefault();
    if (!questionText.trim() || !cropName.trim()) return;

    const newReq: ExpertReq = {
      id: `exp-${Date.now()}`,
      crop_name: cropName,
      farmer_name: "Farmer",
      question: questionText,
      status: "Open",
      created_at: "Just Now",
      answers: []
    };
    setRequests([newReq, ...requests]);
    setShowSubmitModal(false);
    setQuestionText("");
    setCropName("");
  };

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white flex items-center gap-2">
            <UserCheck className="w-8 h-8 text-emerald-400" />
            {t('nav.experts')} Consultation Escalation Hub
          </h1>
          <p className="text-sm text-emerald-200/80 mt-1">
            Connect directly with verified agricultural university scientists when AI confidence is uncertain.
          </p>
        </div>

        <button
          onClick={() => setShowSubmitModal(true)}
          className="flex items-center space-x-2 bg-gradient-to-r from-emerald-500 to-teal-400 text-emerald-950 font-bold px-4 py-2.5 rounded-xl shadow-lg hover:scale-105 transition-transform text-sm"
        >
          <Plus className="w-4 h-4 stroke-[3]" />
          <span>Ask Human Expert</span>
        </button>
      </div>

      {/* Requests Queue List */}
      <div className="space-y-4">
        {requests.length > 0 ? (
          requests.map((req) => (
            <div key={req.id} className="glass-panel p-6 rounded-2xl border border-emerald-800/60 space-y-4">
              
              <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 pb-3 border-b border-emerald-800/40">
                <div>
                  <span className="text-[10px] font-bold uppercase tracking-wider text-teal-400">Crop: {req.crop_name}</span>
                  <h3 className="text-base font-bold text-white mt-0.5">{req.question}</h3>
                </div>
                <span className={`text-xs font-bold px-3 py-1 rounded-full border ${
                  req.status === 'Answered'
                    ? 'bg-emerald-950 text-emerald-300 border-emerald-700'
                    : 'bg-amber-950 text-amber-300 border-amber-700'
                }`}>
                  {req.status}
                </span>
              </div>

              {req.image_url && (
                <img src={req.image_url} alt="Expert Query Image" className="w-32 h-24 object-cover rounded-xl border border-emerald-700/60" />
              )}

              {/* Expert Replies */}
              {req.answers.length > 0 ? (
                <div className="space-y-3 pt-2">
                  <span className="text-xs font-bold text-teal-300">Expert Response</span>
                  {req.answers.map((ans) => (
                    <div key={ans.id} className="bg-emerald-950/80 border border-emerald-700/60 p-4 rounded-xl space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-bold text-white">{ans.expert_name}</span>
                        <span className="text-[10px] text-emerald-400">{ans.created_at}</span>
                      </div>
                      <p className="text-xs text-emerald-200/90 leading-relaxed">{ans.response_text}</p>
                      {ans.recommended_action && (
                        <div className="bg-emerald-900/60 p-2.5 rounded-lg text-xs text-teal-200 font-semibold border border-emerald-700/40">
                          💡 Action Recommendation: {ans.recommended_action}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-xs text-amber-300/80 bg-amber-950/40 p-3 rounded-xl border border-amber-800/40">
                  ⏳ Request submitted to expert queue. Expected response within 2-4 hours.
                </div>
              )}

            </div>
          ))
        ) : (
          <div className="glass-panel p-10 rounded-2xl border border-emerald-800/60 text-center space-y-3">
            <UserCheck className="w-12 h-12 text-emerald-500/50 mx-auto" />
            <h4 className="text-base font-bold text-white">No expert consultation requests yet.</h4>
            <p className="text-xs text-emerald-200/70 max-w-md mx-auto">
              If an AI diagnosis is uncertain or you need agricultural scientist guidance, click &quot;Ask Human Expert&quot; to open a consultation request.
            </p>
          </div>
        )}
      </div>

      {/* Submit Question Modal */}
      {showSubmitModal && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-emerald-950 border border-emerald-700/60 rounded-3xl p-6 max-w-md w-full space-y-4 shadow-2xl">
            <h3 className="text-lg font-bold text-white">Ask an Agricultural Expert</h3>
            
            <form onSubmit={handleSubmitQuestion} className="space-y-3 text-xs">
              <div>
                <label className="block text-emerald-300 mb-1">Crop</label>
                <select
                  value={cropName}
                  onChange={(e) => setCropName(e.target.value)}
                  className="w-full bg-emerald-900/60 border border-emerald-700 rounded-xl p-2.5 text-white focus:outline-none"
                >
                  <option value="Tomato">Tomato</option>
                  <option value="Rice">Paddy Rice</option>
                  <option value="Corn">Corn / Maize</option>
                  <option value="Cotton">Cotton</option>
                </select>
              </div>

              <div>
                <label className="block text-emerald-300 mb-1">Detailed Question & Description</label>
                <textarea
                  rows={4}
                  value={questionText}
                  onChange={(e) => setQuestionText(e.target.value)}
                  placeholder="Describe leaf symptoms, weather conditions, or prior treatment..."
                  className="w-full bg-emerald-900/60 border border-emerald-700 rounded-xl p-2.5 text-white focus:outline-none placeholder-emerald-400/50"
                  required
                />
              </div>

              <div className="flex items-center justify-end space-x-3 pt-3">
                <button
                  type="button"
                  onClick={() => setShowSubmitModal(false)}
                  className="px-4 py-2 bg-emerald-900 text-emerald-300 rounded-xl font-semibold"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 bg-gradient-to-r from-emerald-500 to-teal-400 text-emerald-950 font-bold rounded-xl shadow-md"
                >
                  Submit Request
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

    </div>
  );
}
