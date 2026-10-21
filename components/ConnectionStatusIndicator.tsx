'use client';

import React, { useState, useRef, useEffect } from 'react';
import {
  Wifi,
  WifiOff,
  RefreshCw,
  Server,
  Activity,
  AlertTriangle,
  CheckCircle2,
  ChevronDown,
} from 'lucide-react';
import { useConnectionStatus } from '@/lib/useConnectionStatus';

export function ConnectionStatusIndicator() {
  const {
    status,
    latencyMs,
    lastHeartbeat,
    isSimulatedOffline,
    reconnect,
    toggleSimulateOffline,
  } = useConnectionStatus();

  const [isOpen, setIsOpen] = useState(false);
  const [isReconnecting, setIsReconnecting] = useState(false);
  const popoverRef = useRef<HTMLDivElement>(null);

  // Close popover on outside click
  useEffect(() => {
    const handleOutsideClick = (e: MouseEvent) => {
      if (popoverRef.current && !popoverRef.current.contains(e.target as Node)) {
        setIsOpen(false);
      }
    };
    if (isOpen) {
      document.addEventListener('mousedown', handleOutsideClick);
    }
    return () => document.removeEventListener('mousedown', handleOutsideClick);
  }, [isOpen]);

  const handleManualReconnect = async () => {
    setIsReconnecting(true);
    await reconnect();
    setTimeout(() => setIsReconnecting(false), 600);
  };

  const getStatusConfig = () => {
    switch (status) {
      case 'connected':
        return {
          dotClass: 'bg-[#34c759] dark:bg-[#30d158]',
          badgeClass:
            'text-[#34c759] dark:text-[#30d158] bg-[#34c759]/10 hover:bg-[#34c759]/15 border border-[#34c759]/20',
          label: 'Operational',
          icon: Wifi,
          description: 'Heartbeat active · All services responding',
        };
      case 'reconnecting':
        return {
          dotClass: 'bg-[#ff9500] dark:bg-[#ff9f0a] animate-ping',
          badgeClass:
            'text-[#ff9500] dark:text-[#ff9f0a] bg-[#ff9500]/10 hover:bg-[#ff9500]/15 border border-[#ff9500]/20',
          label: 'Reconnecting...',
          icon: RefreshCw,
          description: 'Heartbeat timed out · Retrying connection...',
        };
      case 'offline':
      default:
        return {
          dotClass: 'bg-[#ff3b30] dark:bg-[#ff453a]',
          badgeClass:
            'text-[#ff3b30] dark:text-[#ff453a] bg-[#ff3b30]/10 hover:bg-[#ff3b30]/15 border border-[#ff3b30]/25 animate-pulse',
          label: 'Offline',
          icon: WifiOff,
          description: 'Backend services unreachable · Heartbeat failed',
        };
    }
  };

  const config = getStatusConfig();
  const StatusIcon = config.icon;

  return (
    <div className="relative" ref={popoverRef}>
      {/* Visual Indicator Button in Header */}
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        aria-label={`Backend connection status: ${config.label}`}
        aria-expanded={isOpen}
        title={`Backend status: ${config.label}. Click for diagnostics.`}
        className={`flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[12px] font-medium transition-all cursor-pointer select-none active:scale-95 ${config.badgeClass}`}
      >
        <span className={`w-1.5 h-1.5 rounded-full ${config.dotClass}`} />
        <span>{config.label}</span>
        {status === 'connected' && latencyMs !== null && (
          <span className="hidden xl:inline text-[10px] opacity-75 font-mono">
            {latencyMs}ms
          </span>
        )}
        <ChevronDown className="w-3 h-3 opacity-60 ml-0.5" />
      </button>

      {/* Diagnostics Popover Menu (Apple macOS Sheet/Popover Style) */}
      {isOpen && (
        <div className="absolute right-0 top-10 z-50 w-72 rounded-2xl bg-white/95 dark:bg-[#1e1e1e]/95 backdrop-blur-2xl border border-black/[0.08] dark:border-white/[0.12] shadow-2xl p-4 text-[12px] animate-in fade-in zoom-in-95 duration-100 transition-colors">
          {/* Header */}
          <div className="flex items-center justify-between pb-3 border-b border-black/[0.06] dark:border-white/[0.08]">
            <div className="flex items-center gap-2">
              <div
                className={`w-6 h-6 rounded-lg flex items-center justify-center ${
                  status === 'connected'
                    ? 'bg-[#34c759]/15 text-[#34c759]'
                    : status === 'reconnecting'
                    ? 'bg-[#ff9500]/15 text-[#ff9500]'
                    : 'bg-[#ff3b30]/15 text-[#ff3b30]'
                }`}
              >
                <StatusIcon className="w-3.5 h-3.5" />
              </div>
              <div>
                <div className="font-semibold text-[#1d1d1f] dark:text-[#f5f5f7]">
                  Backend Services
                </div>
                <div className="text-[10px] text-[#86868b] leading-tight">
                  {config.description}
                </div>
              </div>
            </div>
          </div>

          {/* Diagnostics Metrics */}
          <div className="py-3 space-y-2 text-[11px]">
            <div className="flex items-center justify-between text-[#86868b]">
              <span>Connection State:</span>
              <span
                className={`font-semibold capitalize ${
                  status === 'connected'
                    ? 'text-[#34c759]'
                    : status === 'reconnecting'
                    ? 'text-[#ff9500]'
                    : 'text-[#ff3b30]'
                }`}
              >
                {status}
              </span>
            </div>

            <div className="flex items-center justify-between text-[#86868b]">
              <span>Heartbeat Latency:</span>
              <span className="font-mono text-[#1d1d1f] dark:text-[#f5f5f7]">
                {status === 'connected' && latencyMs !== null ? `${latencyMs} ms` : 'Unreachable'}
              </span>
            </div>

            <div className="flex items-center justify-between text-[#86868b]">
              <span>Protocol / Transport:</span>
              <span className="font-mono text-[#1d1d1f] dark:text-[#f5f5f7]">
                HTTP/2 + WebSocket Sync
              </span>
            </div>

            <div className="flex items-center justify-between text-[#86868b]">
              <span>Last Heartbeat:</span>
              <span className="text-[#1d1d1f] dark:text-[#f5f5f7]">
                {lastHeartbeat ? lastHeartbeat.toLocaleTimeString() : 'Never'}
              </span>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="pt-3 border-t border-black/[0.06] dark:border-white/[0.08] space-y-1.5">
            <button
              type="button"
              onClick={handleManualReconnect}
              disabled={isReconnecting}
              className="w-full flex items-center justify-center gap-1.5 py-1.5 px-3 rounded-xl bg-black/[0.04] dark:bg-white/[0.06] hover:bg-black/[0.08] dark:hover:bg-white/[0.1] text-[#1d1d1f] dark:text-[#f5f5f7] text-[11px] font-medium transition cursor-pointer active:scale-98"
            >
              <RefreshCw className={`w-3 h-3 ${isReconnecting ? 'animate-spin' : ''}`} />
              <span>{isReconnecting ? 'Pinging Service...' : 'Ping Heartbeat Now'}</span>
            </button>

            {/* Simulated Outage Switch for Testing Criteria */}
            <button
              type="button"
              onClick={toggleSimulateOffline}
              className={`w-full flex items-center justify-center gap-1.5 py-1.5 px-3 rounded-xl text-[11px] font-medium transition cursor-pointer active:scale-98 ${
                isSimulatedOffline
                  ? 'bg-[#34c759]/10 hover:bg-[#34c759]/20 text-[#34c759] border border-[#34c759]/25'
                  : 'bg-[#ff3b30]/10 hover:bg-[#ff3b30]/20 text-[#ff3b30] border border-[#ff3b30]/20'
              }`}
            >
              {isSimulatedOffline ? (
                <>
                  <CheckCircle2 className="w-3 h-3" />
                  <span>Restore Live Connection</span>
                </>
              ) : (
                <>
                  <AlertTriangle className="w-3 h-3" />
                  <span>Simulate Heartbeat / WebSocket Failure</span>
                </>
              )}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
