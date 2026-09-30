'use client';

import React, { useState, useEffect } from 'react';
import { useTranslation } from '@/lib/i18n';
import { Mic, MicOff, Volume2, Square, Sparkles, AlertCircle } from 'lucide-react';

interface VoiceAssistantProps {
  onTranscriptReceived?: (transcript: string) => void;
}

export const VoiceAssistantBar: React.FC<VoiceAssistantProps> = ({ onTranscriptReceived }) => {
  const { language, t } = useTranslation();
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [isPlayingSpeech, setIsPlayingSpeech] = useState(false);
  const [statusText, setStatusText] = useState<string>('');

  const sampleVoicePrompts: Record<string, string> = {
    en: "How can I protect my plant crop from leaf disease?",
    ta: "என் பயிரை இலை நோயிலிருந்து எவ்வாறு பாதுகாப்பது?",
    hi: "मैं अपनी फसल को पत्तों की बीमारी से कैसे बचाऊं?",
    te: "నా పంటను ఆకు తెగుళ్ల నుండి ఎలా కాపాడుకోవాలి?",
    ml: "എന്റെ വിളയെ ഇല രോഗങ്ങളിൽ നിന്ന് എങ്ങനെ സംരക്ഷിക്കാം?",
    kn: "ನನ್ನ ಬೆಳೆಯನ್ನು ಎಲೆ ರೋಗದಿಂದ ಹೇಗೆ ರಕ್ಷಿಸುವುದು?"
  };

  const sampleVoiceAnswers: Record<string, string> = {
    en: "Please upload a photo of your affected crop leaf or ask a specific question for AI treatment guidance.",
    ta: "தயவுசெய்து உங்கள் பயிர் இலையின் புகைப்படத்தைப் பதிவேற்றவும்.",
    hi: "कृपया प्रभावित फसल की पत्ती की फोटो अपलोड करें।",
    te: "దయచేసి ప్రభావిత పంట ఆకు ఫోటోను అప్‌లోడ్ చేయండి.",
    ml: "ദയവായി ബാധിച്ച ഇലയുടെ ഫോട്ടോ അപ്‌ലോഡ് ചെയ്യുക.",
    kn: "ದಯವಿಟ್ಟು ಬಾಧಿತ ಎಲೆಯ ಫೋಟೋವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ."
  };

  const handleStartVoice = () => {
    setIsRecording(true);
    setStatusText(t('assistant.listening'));

    // Simulated speech-to-text audio capture
    setTimeout(() => {
      setIsRecording(false);
      setIsProcessing(true);
      setStatusText("Processing speech audio...");

      setTimeout(() => {
        setIsProcessing(false);
        const text = sampleVoicePrompts[language] || sampleVoicePrompts['en'];
        setStatusText(`Recognized (${language.toUpperCase()}): "${text}"`);
        if (onTranscriptReceived) {
          onTranscriptReceived(text);
        }

        // Trigger Web Speech API audio playback synthesis
        speakResponse(sampleVoiceAnswers[language] || sampleVoiceAnswers['en']);
      }, 1000);
    }, 2500);
  };

  const speakResponse = (text: string) => {
    if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 0.9;
      utterance.onstart = () => setIsPlayingSpeech(true);
      utterance.onend = () => setIsPlayingSpeech(false);
      utterance.onerror = () => setIsPlayingSpeech(false);
      window.speechSynthesis.speak(utterance);
    }
  };

  const handleStopSpeech = () => {
    if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      setIsPlayingSpeech(false);
    }
  };

  return (
    <div className="bg-gradient-to-r from-emerald-900/90 via-teal-900/90 to-emerald-950/90 border border-emerald-700/60 rounded-2xl p-4 shadow-xl text-white">
      <div className="flex flex-col sm:flex-row items-center justify-between gap-3">
        
        <div className="flex items-center space-x-3 w-full sm:w-auto">
          <div className="w-10 h-10 rounded-xl bg-emerald-500/20 border border-emerald-400/40 flex items-center justify-center text-emerald-300">
            <Sparkles className="w-5 h-5 animate-pulse" />
          </div>
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-emerald-300">
              Multilingual Voice Assistant
            </h4>
            <p className="text-xs text-emerald-200/80">
              {statusText || `Press mic to speak in ${language.toUpperCase()}`}
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-2 w-full sm:w-auto justify-end">
          
          {!isRecording && !isProcessing && (
            <button
              onClick={handleStartVoice}
              className="w-full sm:w-auto flex items-center justify-center space-x-2 bg-gradient-to-r from-emerald-500 to-teal-400 text-emerald-950 font-bold px-4 py-2 rounded-xl shadow-md hover:scale-105 active:scale-95 transition-all text-xs"
            >
              <Mic className="w-4 h-4" />
              <span>🎤 {t('assistant.micStart')}</span>
            </button>
          )}

          {isRecording && (
            <div className="flex items-center space-x-2 bg-red-600/90 text-white px-4 py-2 rounded-xl text-xs font-bold animate-pulse">
              <Mic className="w-4 h-4" />
              <span>{t('assistant.listening')}</span>
            </div>
          )}

          {isProcessing && (
            <div className="flex items-center space-x-2 bg-teal-600/90 text-white px-4 py-2 rounded-xl text-xs font-bold">
              <span className="w-3 h-3 border-2 border-white border-t-transparent rounded-full animate-spin" />
              <span>AI Processing...</span>
            </div>
          )}

          {isPlayingSpeech && (
            <button
              onClick={handleStopSpeech}
              className="flex items-center space-x-1.5 bg-amber-500/90 text-amber-950 font-bold px-3 py-2 rounded-xl text-xs shadow-md"
            >
              <Square className="w-3.5 h-3.5 fill-current" />
              <span>Stop Voice</span>
            </button>
          )}

        </div>

      </div>
    </div>
  );
};
