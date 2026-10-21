'use client';

import React, { useState } from 'react';
import { Sliders, X, Check, Bot } from 'lucide-react';

interface ModelConfigModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSave?: (config: any) => void;
}

export function ModelConfigModal({ isOpen, onClose, onSave }: ModelConfigModalProps) {
  const [provider, setProvider] = useState('gemini-2.5-flash');
  const [temperature, setTemperature] = useState(0.2);
  const [maxTokens, setMaxTokens] = useState(2048);
  const [enableRag, setEnableRag] = useState(true);
  const [groundingThreshold, setGroundingThreshold] = useState(0.85);

  if (!isOpen) return null;

  const handleSave = () => {
    if (onSave) {
      onSave({ provider, temperature, maxTokens, enableRag, groundingThreshold });
    }
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/35 dark:bg-black/60 backdrop-blur-md flex items-center justify-center p-4">
      <div className="bg-white/95 dark:bg-[#1e1e1e]/95 backdrop-blur-2xl border border-black/[0.08] dark:border-white/[0.12] rounded-2xl w-full max-w-lg p-6 shadow-2xl animate-in zoom-in-95 duration-150 transition-colors">
        <div className="flex items-center justify-between pb-4 border-b border-black/[0.06] dark:border-white/[0.08] mb-4">
          <div className="flex items-center gap-2.5">
            <div className="w-7 h-7 rounded-lg bg-[#0071e3]/10 text-[#0071e3] flex items-center justify-center">
              <Bot className="w-4 h-4" />
            </div>
            <div>
              <h3 className="text-[16px] font-semibold text-[#1d1d1f] dark:text-[#f5f5f7] tracking-tight">AI Model Routing</h3>
              <p className="text-[11px] text-[#86868b]">Inference parameters &amp; RAG policies</p>
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

        <div className="space-y-4">
          <div>
            <label className="block text-[11px] font-medium text-[#86868b] dark:text-[#a1a1a6] tracking-tight mb-1">
              Active LLM Model &amp; Provider
            </label>
            <select
              value={provider}
              onChange={(e) => setProvider(e.target.value)}
              className="w-full bg-black/[0.03] dark:bg-white/[0.05] border border-black/[0.08] dark:border-white/[0.1] rounded-xl px-3 py-2 text-[#1d1d1f] dark:text-[#f5f5f7] text-[13px] focus:outline-none focus:ring-2 focus:ring-[#0071e3]/40 dark:focus:ring-[#2997ff]/40 transition"
            >
              <option value="gemini-2.5-flash">Gemini 2.5 Flash (Recommended for RAG)</option>
              <option value="gemini-2.5-pro">Gemini 2.5 Pro (Deep Reasoning &amp; Complex Legal)</option>
              <option value="local-sal-engine">Local Semantic Hybrid Vector Engine</option>
            </select>
          </div>

          <div>
            <div className="flex justify-between items-center mb-1">
              <label className="text-[12px] font-medium text-[#1d1d1f] dark:text-[#f5f5f7]">
                Temperature (Determinism)
              </label>
              <span className="font-mono text-[12px] text-[#0071e3] dark:text-[#2997ff] font-medium">{temperature}</span>
            </div>
            <input
              type="range"
              min="0.0"
              max="1.0"
              step="0.05"
              value={temperature}
              onChange={(e) => setTemperature(parseFloat(e.target.value))}
              className="w-full accent-[#0071e3]"
            />
            <p className="text-[11px] text-[#86868b] mt-0.5">
              Lower temperature (0.1 - 0.3) ensures strictly factual election citations.
            </p>
          </div>

          <div>
            <div className="flex justify-between items-center mb-1">
              <label className="text-[12px] font-medium text-[#1d1d1f] dark:text-[#f5f5f7]">
                Grounding Verification Threshold
              </label>
              <span className="font-mono text-[12px] text-[#34c759] font-medium">{groundingThreshold}</span>
            </div>
            <input
              type="range"
              min="0.5"
              max="0.99"
              step="0.01"
              value={groundingThreshold}
              onChange={(e) => setGroundingThreshold(parseFloat(e.target.value))}
              className="w-full accent-[#34c759]"
            />
          </div>

          <div className="p-3 rounded-xl bg-black/[0.02] dark:bg-white/[0.03] border border-black/[0.06] dark:border-white/[0.08] flex items-center justify-between">
            <div>
              <div className="text-[13px] font-medium text-[#1d1d1f] dark:text-[#f5f5f7]">Hybrid Dense/Sparse RAG</div>
              <div className="text-[11px] text-[#86868b]">
                Retrieve verified Form 26 and ECI gazette snippets
              </div>
            </div>
            <button
              type="button"
              onClick={() => setEnableRag(!enableRag)}
              className={`w-11 h-6 flex items-center rounded-full p-0.5 transition-colors cursor-pointer ${
                enableRag ? 'bg-[#34c759]' : 'bg-black/20 dark:bg-white/20'
              }`}
            >
              <div
                className={`bg-white w-5 h-5 rounded-full shadow-sm transform transition-transform ${
                  enableRag ? 'translate-x-5' : 'translate-x-0'
                }`}
              />
            </button>
          </div>

          <div className="flex items-center justify-end gap-2 pt-4 border-t border-black/[0.06] dark:border-white/[0.08]">
            <button
              type="button"
              onClick={onClose}
              className="px-3.5 py-1.5 rounded-xl bg-black/[0.04] dark:bg-white/[0.06] hover:bg-black/[0.08] dark:hover:bg-white/[0.1] text-[#1d1d1f] dark:text-[#f5f5f7] text-[13px] font-medium transition cursor-pointer"
            >
              Cancel
            </button>
            <button
              type="button"
              onClick={handleSave}
              className="px-4 py-1.5 rounded-xl bg-[#0071e3] hover:bg-[#0077ed] text-white text-[13px] font-medium shadow-sm transition active:scale-[0.98] flex items-center gap-1.5 cursor-pointer"
            >
              <Check className="w-4 h-4" />
              Apply Configuration
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
