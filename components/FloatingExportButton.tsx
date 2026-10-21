'use client';

import React, { useState, useRef, useEffect } from 'react';
import {
  Download,
  FileText,
  FileSpreadsheet,
  ChevronUp,
  X,
  ShieldCheck,
  Activity,
  Layers,
  Vote,
  Sparkles,
} from 'lucide-react';
import {
  ControlInterface,
  ElectionResult,
  Constituency,
  Candidate,
  Party,
  AuditLog,
  SystemHealthMetrics,
  FeatureFlag,
  UserAccount,
  ExecutiveKpis,
  RegionalTurnout,
  Election,
} from '@/lib/types';
import {
  exportResultsPDF,
  exportResultsCSV,
  exportAuditLogsPDF,
  exportAuditLogsCSV,
  exportEnterpriseReportPDF,
  exportEnterpriseReportCSV,
  exportExecutiveReportPDF,
  exportExecutiveReportCSV,
  exportPublicPortalReportPDF,
  exportPublicPortalReportCSV,
} from '@/lib/exportUtils';

interface FloatingExportButtonProps {
  currentInterface: ControlInterface;
  elections: Election[];
  candidates: Candidate[];
  constituencies: Constituency[];
  parties: Party[];
  results: ElectionResult[];
  regionalTurnout: RegionalTurnout[];
  featureFlags: FeatureFlag[];
  healthMetrics: SystemHealthMetrics;
  kpis: ExecutiveKpis;
  auditLogs: AuditLog[];
  userAccounts: UserAccount[];
  onShowToast: (msg: string) => void;
}

export function FloatingExportButton({
  currentInterface,
  candidates,
  constituencies,
  parties,
  results,
  regionalTurnout,
  featureFlags,
  healthMetrics,
  kpis,
  auditLogs,
  userAccounts,
  onShowToast,
}: FloatingExportButtonProps) {
  const [isOpen, setIsOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);

  // Close on outside click
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    }
    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen]);

  // Close on Escape key
  useEffect(() => {
    function handleKeyDown(event: KeyboardEvent) {
      if (event.key === 'Escape' && isOpen) {
        setIsOpen(false);
      }
    }
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen]);

  // Context metadata for the active interface
  const getInterfaceMeta = () => {
    switch (currentInterface) {
      case 'enterpriseControlCenter':
        return {
          title: 'Enterprise Control Center',
          badge: 'Enterprise',
          subtitle: 'System SLOs, Infrastructure Telemetry & RBAC Audit',
          icon: Activity,
          iconColor: 'text-cyan-500 dark:text-cyan-400',
          badgeBg: 'bg-cyan-500/10 text-cyan-600 dark:text-cyan-400 border-cyan-500/30',
        };
      case 'executiveCommandCenter':
        return {
          title: 'Executive Command Center',
          badge: 'Executive',
          subtitle: 'National Turnout, Polling Booths & High-Level KPIs',
          icon: Layers,
          iconColor: 'text-amber-500 dark:text-amber-400',
          badgeBg: 'bg-amber-500/10 text-amber-600 dark:text-amber-400 border-amber-500/30',
        };
      case 'operationsConsole':
        return {
          title: 'Operations Console',
          badge: 'Operations',
          subtitle: 'Form 20 Constituency Results & EVM Audit Event Stream',
          icon: Vote,
          iconColor: 'text-indigo-500 dark:text-indigo-400',
          badgeBg: 'bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 border-indigo-500/30',
        };
      case 'publicPortal':
        return {
          title: 'Public Transparency Portal',
          badge: 'Public Portal',
          subtitle: 'Form 26 Candidate Affidavits, Assets & Criminal Antecedents',
          icon: ShieldCheck,
          iconColor: 'text-emerald-500 dark:text-emerald-400',
          badgeBg: 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border-emerald-500/30',
        };
    }
  };

  const meta = getInterfaceMeta();
  const IconComponent = meta.icon;

  // Primary export actions for current interface
  const handleExportPDF = () => {
    switch (currentInterface) {
      case 'enterpriseControlCenter':
        exportEnterpriseReportPDF(healthMetrics, featureFlags, userAccounts, auditLogs);
        onShowToast('Downloaded Enterprise Infrastructure Report (PDF)');
        break;
      case 'executiveCommandCenter':
        exportExecutiveReportPDF(kpis, regionalTurnout);
        onShowToast('Downloaded Executive Command Briefing (PDF)');
        break;
      case 'operationsConsole':
        exportResultsPDF(results, constituencies, candidates, parties);
        onShowToast('Downloaded Form 20 Statutory Election Results (PDF)');
        break;
      case 'publicPortal':
        exportPublicPortalReportPDF(candidates, parties, constituencies);
        onShowToast('Downloaded Form 26 Candidate Affidavits (PDF)');
        break;
    }
    setIsOpen(false);
  };

  const handleExportCSV = () => {
    switch (currentInterface) {
      case 'enterpriseControlCenter':
        exportEnterpriseReportCSV(healthMetrics, featureFlags, userAccounts);
        onShowToast('Downloaded Enterprise Infrastructure Dataset (CSV)');
        break;
      case 'executiveCommandCenter':
        exportExecutiveReportCSV(kpis, regionalTurnout);
        onShowToast('Downloaded Executive Turnout Dataset (CSV)');
        break;
      case 'operationsConsole':
        exportResultsCSV(results, constituencies, candidates, parties);
        onShowToast('Downloaded Constituency Results (CSV)');
        break;
      case 'publicPortal':
        exportPublicPortalReportCSV(candidates, parties, constituencies);
        onShowToast('Downloaded Candidate Transparency Data (CSV)');
        break;
    }
    setIsOpen(false);
  };

  const handleExportAuditLogsPDF = () => {
    exportAuditLogsPDF(auditLogs);
    onShowToast('Downloaded Security & Operations Audit Logs (PDF)');
    setIsOpen(false);
  };

  const handleExportAuditLogsCSV = () => {
    exportAuditLogsCSV(auditLogs);
    onShowToast('Downloaded Security & Operations Audit Logs (CSV)');
    setIsOpen(false);
  };

  return (
    <div ref={menuRef} className="fixed bottom-6 left-6 z-40">
      {/* Popover Quick-Action Menu */}
      {isOpen && (
        <div className="absolute bottom-full mb-3 left-0 w-80 sm:w-96 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-2xl shadow-indigo-950/20 dark:shadow-black/60 p-4 animate-in fade-in slide-in-from-bottom-2 duration-150 backdrop-blur-xl">
          {/* Header */}
          <div className="flex items-start justify-between pb-3 border-b border-slate-100 dark:border-slate-800/80">
            <div className="flex items-center gap-2.5">
              <div className="p-2 rounded-xl bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700">
                <IconComponent className={`w-4 h-4 ${meta.iconColor}`} />
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <h4 className="text-xs font-bold uppercase tracking-wider text-slate-900 dark:text-slate-100">
                    Export Interface Data
                  </h4>
                  <span
                    className={`text-[10px] font-semibold px-2 py-0.5 rounded-full border ${meta.badgeBg}`}
                  >
                    {meta.badge}
                  </span>
                </div>
                <p className="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5 line-clamp-1">
                  {meta.subtitle}
                </p>
              </div>
            </div>
            <button
              type="button"
              onClick={() => setIsOpen(false)}
              className="p-1 rounded-lg text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
              aria-label="Close export menu"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          {/* Quick 1-Click Primary Download */}
          <div className="mt-3">
            <button
              type="button"
              onClick={handleExportPDF}
              className="w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl bg-[#0071e3] hover:bg-[#0077ed] dark:bg-[#2997ff] dark:hover:bg-[#47a6ff] text-white font-medium shadow-sm transition-all group cursor-pointer active:scale-[0.98]"
            >
              <div className="flex items-center gap-2.5">
                <div className="p-1.5 rounded-lg bg-white/20 text-white">
                  <FileText className="w-4 h-4" />
                </div>
                <div className="text-left">
                  <div className="text-[13px] font-semibold flex items-center gap-1.5">
                    Official PDF Report
                    <span className="text-[10px] font-medium px-1.5 py-0.2 rounded bg-white/20 text-white">
                      Print Ready
                    </span>
                  </div>
                  <div className="text-[11px] text-white/80">
                    Landscape with statutory verification
                  </div>
                </div>
              </div>
              <Download className="w-4 h-4 text-white/90 group-hover:translate-y-0.5 transition-transform" />
            </button>
          </div>

          {/* CSV Download */}
          <div className="mt-2">
            <button
              type="button"
              onClick={handleExportCSV}
              className="w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl bg-black/[0.04] dark:bg-white/[0.06] hover:bg-black/[0.08] dark:hover:bg-white/[0.1] text-[#1d1d1f] dark:text-[#f5f5f7] font-medium transition-all group cursor-pointer active:scale-[0.98]"
            >
              <div className="flex items-center gap-2.5">
                <div className="p-1.5 rounded-lg bg-[#34c759]/10 text-[#34c759] dark:text-[#30d158]">
                  <FileSpreadsheet className="w-4 h-4" />
                </div>
                <div className="text-left">
                  <div className="text-[13px] font-semibold text-[#1d1d1f] dark:text-[#f5f5f7] flex items-center gap-1.5">
                    Tabular CSV Dataset
                    <span className="text-[10px] font-medium px-1.5 py-0.2 rounded bg-[#34c759]/15 text-[#34c759] dark:text-[#30d158]">
                      RFC 4180
                    </span>
                  </div>
                  <div className="text-[11px] text-[#86868b] dark:text-[#a1a1a6]">
                    Spreadsheet compatible for Excel &amp; Python
                  </div>
                </div>
              </div>
              <Download className="w-4 h-4 text-[#86868b] group-hover:translate-y-0.5 transition-transform" />
            </button>
          </div>

          {/* Operations Extra: Dedicated Audit Logs Export */}
          {currentInterface === 'operationsConsole' && (
            <div className="mt-3 pt-3 border-t border-black/[0.06] dark:border-white/[0.06]">
              <div className="text-[11px] font-medium text-[#86868b] dark:text-[#a1a1a6] mb-2 flex items-center justify-between">
                <span>Security &amp; Audit Stream</span>
                <span className="font-mono text-[11px]">
                  {auditLogs.length} events
                </span>
              </div>
              <div className="grid grid-cols-2 gap-2">
                <button
                  type="button"
                  onClick={handleExportAuditLogsPDF}
                  className="flex items-center justify-center gap-1.5 px-2.5 py-2 rounded-xl bg-black/[0.04] dark:bg-white/[0.06] hover:bg-black/[0.08] dark:hover:bg-white/[0.1] text-[12px] font-medium text-[#1d1d1f] dark:text-[#f5f5f7] transition-all cursor-pointer active:scale-95"
                >
                  <FileText className="w-3.5 h-3.5 text-[#ff3b30]" />
                  <span>Audit Logs (PDF)</span>
                </button>
                <button
                  type="button"
                  onClick={handleExportAuditLogsCSV}
                  className="flex items-center justify-center gap-1.5 px-2.5 py-2 rounded-xl bg-black/[0.04] dark:bg-white/[0.06] hover:bg-black/[0.08] dark:hover:bg-white/[0.1] text-[12px] font-medium text-[#1d1d1f] dark:text-[#f5f5f7] transition-all cursor-pointer active:scale-95"
                >
                  <FileSpreadsheet className="w-3.5 h-3.5 text-[#34c759]" />
                  <span>Audit Logs (CSV)</span>
                </button>
              </div>
            </div>
          )}

          {/* Footer note */}
          <div className="mt-3 pt-2.5 border-t border-black/[0.04] dark:border-white/[0.04] flex items-center justify-between text-[11px] text-[#86868b] dark:text-[#a1a1a6]">
            <span className="flex items-center gap-1.5">
              <Sparkles className="w-3 h-3 text-[#ff9500]" />
              <span>Certified Election Commission Data</span>
            </span>
            <span>Real-time</span>
          </div>
        </div>
      )}

      {/* Floating Trigger Button in Bottom-Left (Apple Dynamic Capsule style) */}
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2.5 px-4 py-2.5 rounded-full bg-white/80 dark:bg-[#1c1c1e]/85 text-[#1d1d1f] dark:text-[#f5f5f7] border border-black/[0.08] dark:border-white/[0.12] shadow-[0_8px_32px_rgba(0,0,0,0.1)] dark:shadow-[0_8px_32px_rgba(0,0,0,0.6)] backdrop-blur-2xl group cursor-pointer transition-all hover:scale-105 active:scale-95"
        aria-label="Export Data for currently viewed interface"
        aria-expanded={isOpen}
      >
        <div className="p-1 rounded-full bg-[#0071e3]/10 dark:bg-[#2997ff]/20 text-[#0071e3] dark:text-[#2997ff] group-hover:bg-[#0071e3] group-hover:text-white transition-colors">
          <Download className="w-3.5 h-3.5" />
        </div>
        <div className="flex items-center gap-2">
          <span className="text-[13px] font-semibold tracking-tight">Export Data</span>
          <span className="text-[11px] font-medium text-[#86868b] dark:text-[#a1a1a6]">
            · {meta.badge}
          </span>
        </div>
        <ChevronUp
          className={`w-3.5 h-3.5 text-[#86868b] transition-transform duration-200 ${
            isOpen ? 'rotate-180' : ''
          }`}
        />
      </button>
    </div>
  );
}
