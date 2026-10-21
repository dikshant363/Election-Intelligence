'use client';

import React, { useState, useEffect } from 'react';
import { Sidebar } from '@/components/Sidebar';
import { Header } from '@/components/Header';
import { EnterpriseControlCenterView } from '@/components/EnterpriseControlCenterView';
import { ExecutiveCommandCenterView } from '@/components/ExecutiveCommandCenterView';
import { OperationsConsoleView } from '@/components/OperationsConsoleView';
import { PublicPortalView } from '@/components/PublicPortalView';
import { CommandPaletteDialog } from '@/components/CommandPaletteDialog';
import { AIAssistantDrawer } from '@/components/AIAssistantDrawer';
import { NotificationsModal } from '@/components/NotificationsModal';
import { ModelConfigModal } from '@/components/ModelConfigModal';
import { FloatingExportButton } from '@/components/FloatingExportButton';
import {
  ControlInterface,
  Election,
  Candidate,
  Constituency,
  Party,
  ElectionResult,
  ETLBatch,
  FeatureFlag,
  SystemHealthMetrics,
  AuditLog,
  UserAccount,
  ExecutiveKpis,
  RegionalTurnout,
  SearchHit,
} from '@/lib/types';
import {
  initialElections,
  initialCandidates,
  initialConstituencies,
  initialParties,
  initialElectionResults,
  initialRegionalTurnout,
  initialETLBatches,
  initialFeatureFlags,
  initialHealthMetrics,
  initialExecutiveKpis,
  initialAuditLogs,
  initialUserAccounts,
  store,
} from '@/lib/store';
import { CheckCircle2, AlertCircle, Sparkles, Volume2 } from 'lucide-react';
import { subscribeSpeechAnnouncements } from '@/lib/voiceOver';

export default function ControlCenterApp() {
  const [currentInterface, setCurrentInterface] =
    useState<ControlInterface>('enterpriseControlCenter');

  // Theme state: dark | light, persisted in localStorage
  const [theme, setTheme] = useState<'dark' | 'light'>('dark');

  useEffect(() => {
    try {
      const saved = localStorage.getItem('election_theme') || localStorage.getItem('theme');
      if (saved === 'light') {
        setTheme('light');
        document.documentElement.classList.remove('dark');
      } else {
        setTheme('dark');
        document.documentElement.classList.add('dark');
      }
    } catch (e) {}
  }, []);

  const handleToggleTheme = () => {
    const next = theme === 'dark' ? 'light' : 'dark';
    setTheme(next);
    try {
      localStorage.setItem('election_theme', next);
      localStorage.setItem('theme', next);
    } catch (e) {}
    if (next === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
    showToast(`Switched to ${next === 'dark' ? 'Dark' : 'Light'} Mode.`);
  };

  // Core state synced with store
  const [elections, setElections] = useState<Election[]>(initialElections);
  const [candidates, setCandidates] = useState<Candidate[]>(initialCandidates);
  const [constituencies, setConstituencies] = useState<Constituency[]>(initialConstituencies);
  const [parties, setParties] = useState<Party[]>(initialParties);
  const [results, setResults] = useState<ElectionResult[]>(initialElectionResults);
  const [regionalTurnout, setRegionalTurnout] = useState<RegionalTurnout[]>(initialRegionalTurnout);
  const [etlBatches, setEtlBatches] = useState<ETLBatch[]>(initialETLBatches);
  const [featureFlags, setFeatureFlags] = useState<FeatureFlag[]>(initialFeatureFlags);
  const [healthMetrics, setHealthMetrics] = useState<SystemHealthMetrics>(initialHealthMetrics);
  const [kpis, setKpis] = useState<ExecutiveKpis>(initialExecutiveKpis);
  const [auditLogs, setAuditLogs] = useState<AuditLog[]>(initialAuditLogs);
  const [userAccounts, setUserAccounts] = useState<UserAccount[]>(initialUserAccounts);

  // Dialog and drawer visibility
  const [isCommandPaletteOpen, setIsCommandPaletteOpen] = useState(false);
  const [isAIAssistantOpen, setIsAIAssistantOpen] = useState(false);
  const [isNotificationsOpen, setIsNotificationsOpen] = useState(false);
  const [isModelConfigOpen, setIsModelConfigOpen] = useState(false);
  const [mobileSidebarOpen, setMobileSidebarOpen] = useState(false);

  // Toast feedback
  const [toastMessage, setToastMessage] = useState<string | null>(null);
  const [activeSpeech, setActiveSpeech] = useState<string | null>(null);

  useEffect(() => {
    return subscribeSpeechAnnouncements((text) => {
      setActiveSpeech(text);
      const timer = setTimeout(() => {
        setActiveSpeech(null);
      }, 5500);
      return () => clearTimeout(timer);
    });
  }, []);

  const showToast = (msg: string) => {
    setToastMessage(msg);
    setTimeout(() => {
      setToastMessage(null);
    }, 3500);
  };

  // Notifications list
  const [notifications, setNotifications] = useState([
    {
      id: 'notif-1',
      title: 'ETL Ingestion Completed',
      message: 'Batch-8841 results CSV validated across 543 seats with 0 schema violations.',
      time: '12m ago',
      type: 'success' as const,
      read: false,
    },
    {
      id: 'notif-2',
      title: 'Official Result Declared',
      message: 'Varanasi (UP-77) declaration certified by Returning Officer.',
      time: '1h ago',
      type: 'info' as const,
      read: false,
    },
    {
      id: 'notif-3',
      title: 'SLO Target Verified',
      message: 'Cluster uptime recorded at 99.98% exceeding statutory 99.9% target.',
      time: '3h ago',
      type: 'success' as const,
      read: true,
    },
  ]);

  // Handlers for mutations
  const handleToggleFlag = (flagName: string) => {
    const updated = store.toggleFeatureFlag(flagName);
    setFeatureFlags([...updated]);
    setAuditLogs([...store.auditLogs]);
    showToast(`Feature flag "${flagName}" updated.`);
  };

  const handleAddElection = (election: Omit<Election, 'id'>) => {
    const created = store.addElection(election);
    setElections([...store.elections]);
    setKpis({ ...store.kpis });
    setAuditLogs([...store.auditLogs]);
    showToast(`Election "${created.title}" scheduled successfully.`);
  };

  const handleAddCandidate = (candidate: Omit<Candidate, 'id' | 'submission_date'>) => {
    const created = store.addCandidate(candidate);
    setCandidates([...store.candidates]);
    setKpis({ ...store.kpis });
    setAuditLogs([...store.auditLogs]);
    showToast(`Candidate "${created.name}" registered under Form 26.`);
  };

  const handleDeclareResult = (result: ElectionResult) => {
    const saved = store.declareResult(result);
    setResults([...store.results]);
    setAuditLogs([...store.auditLogs]);
    showToast(`Official result declared for constituency.`);
  };

  const handleImportBatch = (filename: string, records: string, provenance: string) => {
    const newBatch = store.addETLBatch(filename, records, provenance);
    setEtlBatches([...store.etlBatches]);
    setAuditLogs([...store.auditLogs]);
    showToast(`Ingestion started for "${newBatch.sourceFile}".`);
  };

  const handleActionTrigger = (actionKey: string) => {
    if (actionKey === 'flush_cache') {
      showToast('Flushed Redis & In-Memory Application Caches.');
    } else if (actionKey === 'reindex_search') {
      showToast('Reindexed 9,540 electoral entities in Search Abstraction Layer.');
    } else if (actionKey === 'ai_config') {
      setIsModelConfigOpen(true);
    } else if (actionKey === 'validate_checksums') {
      setCurrentInterface('operationsConsole');
      showToast('Opening Automated Checksum Validation Suite...');
    }
  };

  const handleSearch = (query: string): SearchHit[] => {
    return store.search(query);
  };

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100 flex flex-col md:flex-row antialiased transition-colors duration-150" suppressHydrationWarning>
      {/* Sidebar Navigation */}
      <div className="hidden md:block">
        <Sidebar
          currentInterface={currentInterface}
          onSelectInterface={setCurrentInterface}
          onOpenPalette={() => setIsCommandPaletteOpen(true)}
        />
      </div>

      {/* Mobile Sidebar Overlay */}
      {mobileSidebarOpen && (
        <div className="fixed inset-0 z-40 bg-black/60 md:hidden flex">
          <div className="w-72 bg-white dark:bg-slate-900 h-full">
            <Sidebar
              currentInterface={currentInterface}
              onSelectInterface={(i) => {
                setCurrentInterface(i);
                setMobileSidebarOpen(false);
              }}
              onOpenPalette={() => {
                setIsCommandPaletteOpen(true);
                setMobileSidebarOpen(false);
              }}
            />
          </div>
          <div
            className="flex-1"
            onClick={() => setMobileSidebarOpen(false)}
          />
        </div>
      )}

      {/* Main Workspace Body */}
      <div className="flex-1 flex flex-col min-w-0 min-h-screen overflow-x-hidden">
        {/* Top Header Bar */}
        <Header
          currentInterface={currentInterface}
          onOpenCommandPalette={() => setIsCommandPaletteOpen(true)}
          onOpenAIAssistant={() => setIsAIAssistantOpen(true)}
          onOpenNotifications={() => setIsNotificationsOpen(true)}
          unreadCount={notifications.filter((n) => !n.read).length}
          onToggleMobileSidebar={() => setMobileSidebarOpen(!mobileSidebarOpen)}
          theme={theme}
          onToggleTheme={handleToggleTheme}
        />

        {/* Dynamic Body View Area based on currentInterface */}
        <main className="flex-1 bg-[#f5f5f7] dark:bg-black pb-24 transition-colors">
          {currentInterface === 'enterpriseControlCenter' && (
            <EnterpriseControlCenterView
              metrics={healthMetrics}
              featureFlags={featureFlags}
              auditLogs={auditLogs}
              userAccounts={userAccounts}
              onToggleFlag={handleToggleFlag}
              onOpenModelConfig={() => setIsModelConfigOpen(true)}
            />
          )}

          {currentInterface === 'executiveCommandCenter' && (
            <ExecutiveCommandCenterView
              kpis={kpis}
              regionalTurnout={regionalTurnout}
            />
          )}

          {currentInterface === 'operationsConsole' && (
            <OperationsConsoleView
              elections={elections}
              candidates={candidates}
              constituencies={constituencies}
              parties={parties}
              results={results}
              etlBatches={etlBatches}
              auditLogs={auditLogs}
              onAddElection={handleAddElection}
              onAddCandidate={handleAddCandidate}
              onDeclareResult={handleDeclareResult}
              onImportBatch={handleImportBatch}
              onShowToast={showToast}
            />
          )}

          {currentInterface === 'publicPortal' && (
            <PublicPortalView
              elections={elections}
              candidates={candidates}
              constituencies={constituencies}
              parties={parties}
              onSearch={handleSearch}
            />
          )}
        </main>
      </div>

      {/* Floating Quick Action 'Export Data' Button in Bottom-Left */}
      <FloatingExportButton
        currentInterface={currentInterface}
        elections={elections}
        candidates={candidates}
        constituencies={constituencies}
        parties={parties}
        results={results}
        regionalTurnout={regionalTurnout}
        featureFlags={featureFlags}
        healthMetrics={healthMetrics}
        kpis={kpis}
        auditLogs={auditLogs}
        userAccounts={userAccounts}
        onShowToast={showToast}
      />

      {/* Floating Apple Intelligence Pill on Bottom Right */}
      <button
        type="button"
        onClick={() => setIsAIAssistantOpen(true)}
        className="fixed bottom-6 right-6 z-30 px-4 py-2.5 rounded-full bg-[#0071e3] hover:bg-[#0077ed] dark:bg-[#2997ff] dark:hover:bg-[#47a6ff] text-white shadow-[0_8px_24px_rgba(0,113,227,0.35)] dark:shadow-[0_8px_24px_rgba(41,151,255,0.4)] flex items-center gap-2 group cursor-pointer transition-all hover:scale-105 active:scale-95"
        aria-label="Ask Apple Intelligence Assistant"
      >
        <Sparkles className="w-3.5 h-3.5 text-white" />
        <span className="text-[13px] font-semibold tracking-tight">
          Intelligence
        </span>
        <span className="w-1.5 h-1.5 rounded-full bg-white/80 animate-pulse" />
      </button>

      {/* Voice-over Dynamic Island Active Speech Feedback */}
      {activeSpeech && (
        <div className="fixed top-4 left-1/2 -translate-x-1/2 z-50 bg-[#1d1d1f]/95 dark:bg-[#1c1c1e]/95 text-white border border-white/15 px-4 py-2 rounded-full text-[12px] font-medium shadow-2xl flex items-center gap-2.5 backdrop-blur-2xl animate-in fade-in slide-in-from-top-3 max-w-lg">
          <span className="w-2 h-2 rounded-full bg-[#0071e3] dark:bg-[#2997ff] animate-ping shrink-0" />
          <Volume2 className="w-3.5 h-3.5 text-[#2997ff] shrink-0" />
          <span className="truncate">Voice-over: {activeSpeech}</span>
        </div>
      )}

      {/* Apple Dynamic Island Style Toast */}
      {toastMessage && (
        <div className="fixed bottom-6 left-1/2 -translate-x-1/2 z-50 bg-[#1d1d1f]/95 dark:bg-[#2c2c2e]/95 text-white border border-white/10 px-4 py-2 rounded-full text-[12px] font-medium shadow-2xl flex items-center gap-2 backdrop-blur-2xl animate-in fade-in slide-in-from-bottom-2">
          <CheckCircle2 className="w-3.5 h-3.5 text-[#34c759] shrink-0" />
          <span>{toastMessage}</span>
        </div>
      )}

      {/* Command Palette (Cmd + K) */}
      <CommandPaletteDialog
        isOpen={isCommandPaletteOpen}
        onClose={() => setIsCommandPaletteOpen(false)}
        onSelectInterface={(intf) => setCurrentInterface(intf)}
        onTriggerAction={handleActionTrigger}
      />

      {/* AI Assistant RAG Drawer */}
      <AIAssistantDrawer
        isOpen={isAIAssistantOpen}
        onClose={() => setIsAIAssistantOpen(false)}
      />

      {/* System Notifications Modal */}
      <NotificationsModal
        isOpen={isNotificationsOpen}
        onClose={() => setIsNotificationsOpen(false)}
        notifications={notifications}
        onMarkAllAsRead={() => {
          setNotifications(notifications.map((n) => ({ ...n, read: true })));
          showToast('All notifications marked as read.');
        }}
      />

      {/* Model Hyperparameters Configuration Modal */}
      <ModelConfigModal
        isOpen={isModelConfigOpen}
        onClose={() => setIsModelConfigOpen(false)}
        onSave={(cfg) => {
          showToast(`Model routing updated: ${cfg.provider}`);
        }}
      />
    </div>
  );
}
