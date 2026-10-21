'use client';

import React, { useEffect } from 'react';
import { AlertTriangle, RefreshCw } from 'lucide-react';

export default function ErrorBoundary({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error('Unhandled app error:', error);
  }, [error]);

  return (
    <div className="min-h-screen bg-[#f5f5f7] dark:bg-black text-[#1d1d1f] dark:text-[#f5f5f7] flex items-center justify-center p-6 antialiased">
      <div className="max-w-md w-full bg-white/90 dark:bg-[#1c1c1e]/90 backdrop-blur-2xl border border-black/[0.08] dark:border-white/[0.12] rounded-3xl p-8 shadow-2xl text-center">
        <div className="w-12 h-12 rounded-2xl bg-[#ff3b30]/10 text-[#ff3b30] flex items-center justify-center mx-auto mb-4">
          <AlertTriangle className="w-6 h-6" />
        </div>
        <h1 className="text-xl font-bold tracking-tight mb-1">Application Error</h1>
        <p className="text-[13px] text-[#86868b] dark:text-[#a1a1a6] mb-6">
          An error occurred in the election intelligence platform pipeline.
        </p>
        <button
          type="button"
          onClick={() => reset()}
          className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full bg-[#0071e3] hover:bg-[#0077ed] text-white text-[13px] font-medium transition active:scale-95 shadow-sm cursor-pointer"
        >
          <RefreshCw className="w-4 h-4" />
          <span>Reload Interface</span>
        </button>
      </div>
    </div>
  );
}
