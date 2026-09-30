'use client';

import React, { useState } from 'react';
import { useTranslation } from '@/lib/i18n';
import { api } from '@/lib/api';
import { VoiceAssistantBar } from '@/components/VoiceAssistantBar';
import { 
  Bot, Send, Image as ImageIcon, Mic, BookOpen, User, Sparkles, CheckCircle2, AlertCircle, RefreshCw 
} from 'lucide-react';

interface ChatMsg {
  id: string;
  sender: 'user' | 'assistant';
  text: string;
  image_url?: string;
  citations?: string[];
  created_at: string;
}

export default function AssistantPage() {
  const { language, t } = useTranslation();
  const [inputText, setInputText] = useState('');
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [messages, setMessages] = useState<ChatMsg[]>([
    {
      id: 'msg-init-1',
      sender: 'assistant',
      text: 'Hello! I am your PhytoVeyra AI Agricultural Companion. Ask me anything about your registered crops, plant health, treatments, or disease diagnosis.',
      citations: ['ICAR Crop Protection Handbook', 'State Agritech Knowledge Base'],
      created_at: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
  ]);
  const [isSending, setIsSending] = useState(false);

  const handleImageSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      const reader = new FileReader();
      reader.onload = (ev) => {
        setSelectedImage(ev.target?.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSendMessage = async (textToSend?: string) => {
    if (isSending) return; // Prevent duplicate requests when send clicked multiple times

    const text = (textToSend || inputText).trim();
    if (!text && !selectedImage) return;

    setErrorMessage(null);

    const userMsg: ChatMsg = {
      id: `usr-${Date.now()}`,
      sender: 'user',
      text: text || "Uploaded plant photo for diagnosis.",
      image_url: selectedImage || undefined,
      created_at: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    const currentHistory = messages.map(m => ({
      sender: m.sender,
      text: m.text
    }));

    setMessages((prev) => [...prev, userMsg]);
    setInputText('');
    setSelectedImage(null);
    setIsSending(true);

    try {
      const res = await api.sendChatMessage({
        text: text || "Analyze this crop image",
        language: language || "en",
        history: currentHistory
      });

      if (res && res.text) {
        const assistantMsg: ChatMsg = {
          id: res.id || `ast-${Date.now()}`,
          sender: 'assistant',
          text: res.text,
          citations: res.citations || ['PhytoVeyra Agricultural Knowledge Base'],
          created_at: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        };
        setMessages((prev) => [...prev, assistantMsg]);
      } else {
        setErrorMessage("Failed to receive AI response. Please try again.");
      }
    } catch (err: any) {
      setErrorMessage(err?.message || "Error connecting to AI Backend Service.");
    } finally {
      setIsSending(false);
    }
  };

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white flex items-center gap-2">
          <Bot className="w-8 h-8 text-emerald-400" />
          {t('assistant.title')}
        </h1>
        <p className="text-sm text-emerald-200/80 mt-1">
          {t('assistant.subtitle')}
        </p>
      </div>

      {/* Voice Assistant Microphone Integration Bar */}
      <VoiceAssistantBar
        onTranscriptReceived={(transcript) => handleSendMessage(transcript)}
      />

      {/* Main Chat Interface Window */}
      <div className="glass-panel rounded-3xl border border-emerald-800/60 flex flex-col h-[520px] overflow-hidden bg-emerald-950/80 shadow-2xl">
        
        {/* Messages Scroll Area */}
        <div className="flex-1 p-4 sm:p-6 overflow-y-auto space-y-4">
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex items-start space-x-3 ${
                msg.sender === 'user' ? 'justify-end' : 'justify-start'
              }`}
            >
              {msg.sender === 'assistant' && (
                <div className="w-8 h-8 rounded-xl bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 flex items-center justify-center shrink-0">
                  <Bot className="w-5 h-5" />
                </div>
              )}

              <div
                className={`max-w-[85%] sm:max-w-[75%] p-4 rounded-2xl text-xs leading-relaxed space-y-2 shadow-md ${
                  msg.sender === 'user'
                    ? 'bg-gradient-to-r from-emerald-600 to-teal-500 text-white rounded-tr-none font-medium'
                    : 'bg-emerald-900/90 text-emerald-100 border border-emerald-700/60 rounded-tl-none'
                }`}
              >
                {msg.image_url && (
                  <img
                    src={msg.image_url}
                    alt="Chat Upload"
                    className="w-48 h-36 object-cover rounded-xl border border-emerald-400/30"
                  />
                )}
                <p className="whitespace-pre-wrap">{msg.text}</p>

                {msg.citations && msg.citations.length > 0 && (
                  <div className="pt-2 border-t border-emerald-700/40 text-[10px] text-teal-300 space-y-1">
                    <span className="font-bold uppercase tracking-wider flex items-center gap-1">
                      <BookOpen className="w-3 h-3" />
                      {t('assistant.citations')}:
                    </span>
                    <ul className="list-disc list-inside space-y-0.5 text-emerald-200/90">
                      {msg.citations.map((c, i) => (
                        <li key={i}>{c}</li>
                      ))}
                    </ul>
                  </div>
                )}

                <span className="block text-[9px] text-right text-emerald-300/60 font-mono">
                  {msg.created_at}
                </span>
              </div>

              {msg.sender === 'user' && (
                <div className="w-8 h-8 rounded-xl bg-teal-500 text-emerald-950 font-bold flex items-center justify-center shrink-0">
                  <User className="w-4 h-4" />
                </div>
              )}
            </div>
          ))}

          {isSending && (
            <div className="flex items-center space-x-2 text-xs text-emerald-300 bg-emerald-900/40 p-3 rounded-xl border border-emerald-800/60 w-fit">
              <RefreshCw className="w-4 h-4 animate-spin text-emerald-400" />
              <span>PhytoVeyra AI is generating response...</span>
            </div>
          )}

          {errorMessage && (
            <div className="flex items-center space-x-2 text-xs text-amber-300 bg-amber-950/80 border border-amber-700/60 p-3 rounded-xl">
              <AlertCircle className="w-4 h-4 text-amber-400 shrink-0" />
              <span>{errorMessage}</span>
            </div>
          )}
        </div>

        {/* Selected Image Thumbnail Preview */}
        {selectedImage && (
          <div className="px-4 py-2 bg-emerald-900/60 border-t border-emerald-800 flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <img src={selectedImage} alt="Preview" className="w-10 h-10 object-cover rounded-lg border border-emerald-600" />
              <span className="text-xs text-emerald-200">Image attached for analysis</span>
            </div>
            <button onClick={() => setSelectedImage(null)} className="text-xs text-red-400 font-bold">Remove</button>
          </div>
        )}

        {/* Input Bar */}
        <div className="p-3 sm:p-4 bg-emerald-950 border-t border-emerald-800/60 flex items-center space-x-2">
          
          <label className="cursor-pointer p-2.5 bg-emerald-900/60 hover:bg-emerald-800/60 text-emerald-300 rounded-xl border border-emerald-700/60 transition-colors">
            <ImageIcon className="w-4 h-4" />
            <input type="file" accept="image/*" onChange={handleImageSelect} className="hidden" />
          </label>

          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && !isSending && handleSendMessage()}
            placeholder={t('assistant.placeholder')}
            disabled={isSending}
            className="flex-1 bg-emerald-900/60 border border-emerald-700/60 rounded-xl px-4 py-2.5 text-xs text-white placeholder-emerald-400/60 focus:outline-none focus:border-emerald-400 disabled:opacity-50"
          />

          <button
            onClick={() => handleSendMessage()}
            disabled={isSending || (!inputText.trim() && !selectedImage)}
            className={`p-2.5 rounded-xl shadow-md transition-transform ${
              isSending || (!inputText.trim() && !selectedImage)
                ? 'bg-emerald-900/40 text-emerald-600 border border-emerald-800/60 cursor-not-allowed'
                : 'bg-gradient-to-r from-emerald-500 to-teal-400 text-emerald-950 font-bold hover:scale-105 cursor-pointer'
            }`}
          >
            {isSending ? (
              <RefreshCw className="w-4 h-4 animate-spin text-emerald-950" />
            ) : (
              <Send className="w-4 h-4 stroke-[2.5]" />
            )}
          </button>

        </div>

      </div>
    </div>
  );
}
