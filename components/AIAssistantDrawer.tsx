'use client';

import React, { useState } from 'react';
import {
  Sparkles,
  X,
  Send,
  Bot,
  User,
  Quote,
  CheckCircle2,
  Cpu,
  Layers,
} from 'lucide-react';

interface Citation {
  source: string;
  document_id: string;
  snippet: string;
  confidence: number;
}

interface Message {
  id: string;
  sender: 'user' | 'ai';
  text: string;
  citations?: Citation[];
  provider?: string;
  groundingScore?: number;
  timestamp: string;
}

interface AIAssistantDrawerProps {
  isOpen: boolean;
  onClose: () => void;
}

export function AIAssistantDrawer({ isOpen, onClose }: AIAssistantDrawerProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'msg-welcome',
      sender: 'ai',
      text: 'Greetings. I am the Election Intelligence RAG Assistant. Ask me anything about election schedules, regional voter turnouts, candidate Form 26 affidavits, or verified constituency results.',
      timestamp: 'Just now',
    },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  if (!isOpen) return null;

  const quickQuestions = [
    'Who won the Varanasi election and by what margin?',
    'What is the average national voter turnout?',
    'Summarize Rahul Gandhi’s declared affidavits in Wayanad',
    'What are the active platform health metrics?',
  ];

  const handleSend = async (questionText?: string) => {
    const query = questionText || input;
    if (!query.trim() || loading) return;

    const userMsg: Message = {
      id: `usr-${Date.now()}`,
      sender: 'user',
      text: query,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const res = await fetch('/api/v1/ai/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: query, enable_rag: true }),
      });

      const data = await res.json();
      const aiMsg: Message = {
        id: `ai-${Date.now()}`,
        sender: 'ai',
        text: data.answer || 'No response returned from the model.',
        citations: data.citations,
        provider: data.provider,
        groundingScore: data.grounding_score,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };

      setMessages((prev) => [...prev, aiMsg]);
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        {
          id: `ai-err-${Date.now()}`,
          sender: 'ai',
          text: 'Encountered an error connecting to the AI inference gateway. Please retry.',
          timestamp: 'Just now',
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/35 dark:bg-black/60 backdrop-blur-md flex justify-end">
      <div className="bg-white/95 dark:bg-[#1c1c1e]/95 backdrop-blur-2xl border-l border-black/[0.08] dark:border-white/[0.12] w-full max-w-md h-full flex flex-col justify-between shadow-2xl animate-in slide-in-from-right duration-200 transition-colors">
        {/* Drawer Header */}
        <div className="px-5 py-4 border-b border-black/[0.06] dark:border-white/[0.08] flex items-center justify-between bg-black/[0.01] dark:bg-white/[0.02]">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-[#0071e3] via-[#af52de] to-[#ff2d55] text-white shadow-md flex items-center justify-center">
              <Sparkles className="w-4 h-4" />
            </div>
            <div>
              <h3 className="text-[15px] font-semibold text-[#1d1d1f] dark:text-[#f5f5f7] flex items-center gap-1.5 tracking-tight">
                Apple Intelligence
                <span className="text-[11px] font-medium text-[#0071e3] dark:text-[#2997ff]">
                  · RAG
                </span>
              </h3>
              <p className="text-[11px] text-[#86868b]">
                Grounded Election Synthesis Engine
              </p>
            </div>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="p-1 rounded-lg text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7] hover:bg-black/[0.04] dark:hover:bg-white/[0.08] transition"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Chat Message List */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex flex-col ${
                msg.sender === 'user' ? 'items-end' : 'items-start'
              }`}
            >
              <div
                className={`flex gap-2.5 max-w-[92%] ${
                  msg.sender === 'user' ? 'flex-row-reverse' : 'flex-row'
                }`}
              >
                <div
                  className={`w-7 h-7 rounded-full shrink-0 flex items-center justify-center text-xs font-bold ${
                    msg.sender === 'user'
                      ? 'bg-[#0071e3] text-white'
                      : 'bg-black/[0.05] dark:bg-white/[0.08] text-[#0071e3] dark:text-[#2997ff]'
                  }`}
                >
                  {msg.sender === 'user' ? <User className="w-3.5 h-3.5" /> : <Bot className="w-3.5 h-3.5" />}
                </div>

                <div
                  className={`p-3.5 text-[13px] leading-relaxed ${
                    msg.sender === 'user'
                      ? 'bg-[#0071e3] text-white rounded-2xl rounded-tr-xs shadow-sm'
                      : 'bg-black/[0.03] dark:bg-white/[0.06] border border-black/[0.04] dark:border-white/[0.06] text-[#1d1d1f] dark:text-[#f5f5f7] rounded-2xl rounded-tl-xs shadow-xs'
                  }`}
                >
                  <p className="whitespace-pre-wrap">{msg.text}</p>

                  {/* Grounded Citations Box */}
                  {msg.citations && msg.citations.length > 0 && (
                    <div className="mt-3 pt-2.5 border-t border-black/[0.06] dark:border-white/[0.08] space-y-1.5">
                      <div className="text-[10px] font-medium text-[#86868b] uppercase tracking-wider flex items-center gap-1">
                        <Quote className="w-3 h-3 text-[#ff9500]" />
                        Verified Source Citations:
                      </div>
                      {msg.citations.map((cite, i) => (
                        <div
                          key={i}
                          className="p-2.5 rounded-xl bg-black/[0.02] dark:bg-white/[0.04] border border-black/[0.04] dark:border-white/[0.06] text-[11px]"
                        >
                          <div className="font-medium text-[#0071e3] dark:text-[#2997ff]">
                            {cite.source}
                          </div>
                          <div className="text-[#86868b] mt-0.5 font-mono text-[10px]">
                            Confidence: {(cite.confidence * 100).toFixed(0)}%
                          </div>
                        </div>
                      ))}
                    </div>
                  )}

                  <div className="mt-2 flex items-center justify-between text-[10px] opacity-70">
                    <span>{msg.timestamp}</span>
                    {msg.provider && (
                      <span className="font-mono">{msg.provider}</span>
                    )}
                  </div>
                </div>
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex items-center gap-2 text-[12px] text-[#0071e3] dark:text-[#2997ff] bg-black/[0.03] dark:bg-white/[0.05] p-3 rounded-2xl border border-black/[0.06] dark:border-white/[0.08] w-fit">
              <Bot className="w-4 h-4 animate-spin" />
              <span>Querying Grounded Semantic Knowledge Base...</span>
            </div>
          )}
        </div>

        {/* Quick Questions & Input Box */}
        <div className="p-4 border-t border-black/[0.06] dark:border-white/[0.08] bg-black/[0.01] dark:bg-white/[0.02] space-y-3">
          {/* Quick suggestions */}
          <div className="flex flex-wrap gap-1.5">
            {quickQuestions.map((q, i) => (
              <button
                key={i}
                type="button"
                onClick={() => handleSend(q)}
                className="text-[11px] px-3 py-1 rounded-full bg-black/[0.04] dark:bg-white/[0.06] hover:bg-black/[0.08] dark:hover:bg-white/[0.1] text-[#1d1d1f] dark:text-[#f5f5f7] transition cursor-pointer text-left"
              >
                {q}
              </button>
            ))}
          </div>

          {/* Input form */}
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSend();
            }}
            className="flex items-center gap-2"
          >
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask election intelligence questions..."
              className="flex-1 bg-black/[0.03] dark:bg-white/[0.05] border border-black/[0.08] dark:border-white/[0.1] rounded-full px-4 py-2 text-[13px] text-[#1d1d1f] dark:text-[#f5f5f7] placeholder-[#86868b] focus:outline-none focus:ring-2 focus:ring-[#0071e3]/40 dark:focus:ring-[#2997ff]/40 transition"
            />
            <button
              type="submit"
              disabled={loading || !input.trim()}
              className="w-9 h-9 rounded-full bg-[#0071e3] hover:bg-[#0077ed] disabled:opacity-40 text-white flex items-center justify-center transition active:scale-95 cursor-pointer shrink-0"
            >
              <Send className="w-4 h-4" />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
