'use client';

import React, { useState, useMemo } from 'react';
import {
  Vote,
  MapPin,
  UserPlus,
  RefreshCw,
  Upload,
  CalendarPlus,
  Trophy,
  CheckCircle2,
  FileSpreadsheet,
  AlertCircle,
  Plus,
  FileText,
  Download,
  Shield,
  Table,
  ShieldCheck,
  Lock,
  ArrowUp,
  ArrowDown,
  ArrowUpDown,
  Sliders,
  Activity,
  Cpu,
  LayoutGrid,
} from 'lucide-react';
import { MetricCard } from './MetricCard';
import { Candidate, Constituency, Election, ElectionResult, ETLBatch, Party, AuditLog } from '@/lib/types';
import {
  exportResultsCSV,
  exportResultsPDF,
  exportAuditLogsCSV,
  exportAuditLogsPDF,
} from '@/lib/exportUtils';
import {
  announceEtlStart,
  announceEtlComplete,
  announceOperation,
  speakVoiceOver,
} from '@/lib/voiceOver';
import { StorageChecksumModal } from './StorageChecksumModal';
import { SystemDiagnosticsView } from './SystemDiagnosticsView';

// Generic sort direction type
type SortDirection = 'asc' | 'desc';

// Sort keys for each table
type ResultsSortKey = 'constituency' | 'state' | 'winner' | 'party' | 'margin' | 'total_votes' | 'declaration_time';
type AuditSortKey = 'timestamp' | 'actor' | 'action' | 'resource' | 'status';
type EtlSortKey = 'id' | 'sourceFile' | 'recordsCount' | 'provenance' | 'importedAt' | 'status';
type ElectionSortKey = 'title' | 'election_type' | 'start_date' | 'total_constituencies' | 'turnout_percentage' | 'status';

interface SortableHeaderProps<T extends string> {
  label: string;
  sortKey: T;
  currentKey: T;
  direction: SortDirection;
  onSort: (key: T) => void;
  align?: 'left' | 'right' | 'center';
}

function SortableHeader<T extends string>({
  label,
  sortKey,
  currentKey,
  direction,
  onSort,
  align = 'left',
}: SortableHeaderProps<T>) {
  const isSorted = currentKey === sortKey;
  return (
    <th
      scope="col"
      className={`py-2.5 px-3 font-semibold text-[11px] uppercase tracking-wider text-[#86868b] dark:text-[#a1a1a6] select-none ${
        align === 'right' ? 'text-right' : align === 'center' ? 'text-center' : 'text-left'
      }`}
    >
      <button
        type="button"
        onClick={() => onSort(sortKey)}
        className={`inline-flex items-center gap-1.5 transition-colors cursor-pointer group py-0.5 px-1 -mx-1 rounded-md hover:bg-black/[0.04] dark:hover:bg-white/[0.06] ${
          isSorted ? 'text-[#0071e3] dark:text-[#2997ff] font-bold' : 'hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7]'
        } ${align === 'right' ? 'flex-row-reverse' : ''}`}
        aria-sort={isSorted ? (direction === 'asc' ? 'ascending' : 'descending') : 'none'}
        title={`Sort by ${label} (${isSorted ? (direction === 'asc' ? 'Descending' : 'Ascending') : 'Ascending'})`}
      >
        <span>{label}</span>
        <span className="shrink-0">
          {isSorted ? (
            direction === 'asc' ? (
              <ArrowUp className="w-3.5 h-3.5 text-[#0071e3] dark:text-[#2997ff]" />
            ) : (
              <ArrowDown className="w-3.5 h-3.5 text-[#0071e3] dark:text-[#2997ff]" />
            )
          ) : (
            <ArrowUpDown className="w-3 h-3 text-[#86868b] opacity-40 group-hover:opacity-100 transition-opacity" />
          )}
        </span>
      </button>
    </th>
  );
}

interface OperationsConsoleViewProps {
  elections: Election[];
  candidates: Candidate[];
  constituencies: Constituency[];
  parties: Party[];
  results: ElectionResult[];
  etlBatches: ETLBatch[];
  auditLogs: AuditLog[];
  onAddElection: (election: Omit<Election, 'id'>) => void;
  onAddCandidate: (candidate: Omit<Candidate, 'id' | 'submission_date'>) => void;
  onDeclareResult: (result: ElectionResult) => void;
  onImportBatch: (filename: string, records: string, provenance: string) => void;
  onShowToast: (msg: string) => void;
}

export function OperationsConsoleView({
  elections,
  candidates,
  constituencies,
  parties,
  results,
  etlBatches,
  auditLogs,
  onAddElection,
  onAddCandidate,
  onDeclareResult,
  onImportBatch,
  onShowToast,
}: OperationsConsoleViewProps) {
  // Navigation tab: Electoral Operations vs System Diagnostics
  const [activeTab, setActiveTab] = useState<'operations' | 'diagnostics'>('operations');

  // Modal states
  const [showScheduleModal, setShowScheduleModal] = useState(false);
  const [showCandidateModal, setShowCandidateModal] = useState(false);
  const [showResultModal, setShowResultModal] = useState(false);
  const [showETLModal, setShowETLModal] = useState(false);
  const [showChecksumModal, setShowChecksumModal] = useState(false);
  const [showExportMenu, setShowExportMenu] = useState(false);

  // Sorting state for Declared Results Table
  const [resultsSortKey, setResultsSortKey] = useState<ResultsSortKey>('declaration_time');
  const [resultsSortDir, setResultsSortDir] = useState<SortDirection>('desc');
  const [resultsViewMode, setResultsViewMode] = useState<'table' | 'cards'>('table');

  // Sorting state for Audit Logs Table
  const [auditSortKey, setAuditSortKey] = useState<AuditSortKey>('timestamp');
  const [auditSortDir, setAuditSortDir] = useState<SortDirection>('desc');

  // Sorting state for ETL Ingestion Batches Table
  const [etlSortKey, setEtlSortKey] = useState<EtlSortKey>('importedAt');
  const [etlSortDir, setEtlSortDir] = useState<SortDirection>('desc');

  // Sorting state for Scheduled Elections Table
  const [electionSortKey, setElectionSortKey] = useState<ElectionSortKey>('start_date');
  const [electionSortDir, setElectionSortDir] = useState<SortDirection>('desc');

  // Toggle handlers for sorting
  const toggleResultsSort = (key: ResultsSortKey) => {
    if (resultsSortKey === key) {
      setResultsSortDir((prev) => (prev === 'asc' ? 'desc' : 'asc'));
    } else {
      setResultsSortKey(key);
      setResultsSortDir(key === 'margin' || key === 'total_votes' || key === 'declaration_time' ? 'desc' : 'asc');
    }
  };

  const toggleAuditSort = (key: AuditSortKey) => {
    if (auditSortKey === key) {
      setAuditSortDir((prev) => (prev === 'asc' ? 'desc' : 'asc'));
    } else {
      setAuditSortKey(key);
      setAuditSortDir(key === 'timestamp' ? 'desc' : 'asc');
    }
  };

  const toggleEtlSort = (key: EtlSortKey) => {
    if (etlSortKey === key) {
      setEtlSortDir((prev) => (prev === 'asc' ? 'desc' : 'asc'));
    } else {
      setEtlSortKey(key);
      setEtlSortDir(key === 'importedAt' || key === 'recordsCount' ? 'desc' : 'asc');
    }
  };

  const toggleElectionSort = (key: ElectionSortKey) => {
    if (electionSortKey === key) {
      setElectionSortDir((prev) => (prev === 'asc' ? 'desc' : 'asc'));
    } else {
      setElectionSortKey(key);
      setElectionSortDir(key === 'total_constituencies' || key === 'turnout_percentage' ? 'desc' : 'asc');
    }
  };

  // Memoized sorted datasets
  const sortedResults = useMemo(() => {
    return [...results].sort((a, b) => {
      let comp = 0;
      if (resultsSortKey === 'constituency') {
        const nameA = constituencies.find((c) => c.id === a.constituency_id)?.name || '';
        const nameB = constituencies.find((c) => c.id === b.constituency_id)?.name || '';
        comp = nameA.localeCompare(nameB);
      } else if (resultsSortKey === 'state') {
        const stateA = constituencies.find((c) => c.id === a.constituency_id)?.state_name || '';
        const stateB = constituencies.find((c) => c.id === b.constituency_id)?.state_name || '';
        comp = stateA.localeCompare(stateB);
      } else if (resultsSortKey === 'winner') {
        const winnerA = candidates.find((c) => c.id === a.winning_candidate_id)?.name || '';
        const winnerB = candidates.find((c) => c.id === b.winning_candidate_id)?.name || '';
        comp = winnerA.localeCompare(winnerB);
      } else if (resultsSortKey === 'party') {
        const winnerA = candidates.find((c) => c.id === a.winning_candidate_id);
        const partyA = parties.find((p) => p.id === winnerA?.party_id)?.code || '';
        const winnerB = candidates.find((c) => c.id === b.winning_candidate_id);
        const partyB = parties.find((p) => p.id === winnerB?.party_id)?.code || '';
        comp = partyA.localeCompare(partyB);
      } else if (resultsSortKey === 'margin') {
        comp = a.margin - b.margin;
      } else if (resultsSortKey === 'total_votes') {
        comp = a.total_votes - b.total_votes;
      } else if (resultsSortKey === 'declaration_time') {
        comp = new Date(a.declaration_time).getTime() - new Date(b.declaration_time).getTime();
      }
      return resultsSortDir === 'asc' ? comp : -comp;
    });
  }, [results, resultsSortKey, resultsSortDir, constituencies, candidates, parties]);

  const sortedAuditLogs = useMemo(() => {
    return [...auditLogs].sort((a, b) => {
      let comp = 0;
      if (auditSortKey === 'timestamp') {
        comp = a.timestamp.localeCompare(b.timestamp);
      } else if (auditSortKey === 'actor') {
        comp = a.actor.localeCompare(b.actor);
      } else if (auditSortKey === 'action') {
        comp = a.action.localeCompare(b.action);
      } else if (auditSortKey === 'resource') {
        comp = a.resource.localeCompare(b.resource);
      } else if (auditSortKey === 'status') {
        comp = a.status.localeCompare(b.status);
      }
      return auditSortDir === 'asc' ? comp : -comp;
    });
  }, [auditLogs, auditSortKey, auditSortDir]);

  const sortedEtlBatches = useMemo(() => {
    return [...etlBatches].sort((a, b) => {
      let comp = 0;
      if (etlSortKey === 'id') {
        comp = a.id.localeCompare(b.id);
      } else if (etlSortKey === 'sourceFile') {
        comp = a.sourceFile.localeCompare(b.sourceFile);
      } else if (etlSortKey === 'recordsCount') {
        const numA = parseInt(a.recordsCount.replace(/[^0-9]/g, '')) || 0;
        const numB = parseInt(b.recordsCount.replace(/[^0-9]/g, '')) || 0;
        comp = numA - numB;
      } else if (etlSortKey === 'provenance') {
        comp = a.provenance.localeCompare(b.provenance);
      } else if (etlSortKey === 'importedAt') {
        comp = a.importedAt.localeCompare(b.importedAt);
      } else if (etlSortKey === 'status') {
        comp = a.status.localeCompare(b.status);
      }
      return etlSortDir === 'asc' ? comp : -comp;
    });
  }, [etlBatches, etlSortKey, etlSortDir]);

  const sortedElections = useMemo(() => {
    return [...elections].sort((a, b) => {
      let comp = 0;
      if (electionSortKey === 'title') {
        comp = a.title.localeCompare(b.title);
      } else if (electionSortKey === 'election_type') {
        comp = a.election_type.localeCompare(b.election_type);
      } else if (electionSortKey === 'start_date') {
        comp = a.start_date.localeCompare(b.start_date);
      } else if (electionSortKey === 'total_constituencies') {
        comp = a.total_constituencies - b.total_constituencies;
      } else if (electionSortKey === 'turnout_percentage') {
        comp = a.turnout_percentage - b.turnout_percentage;
      } else if (electionSortKey === 'status') {
        comp = a.status.localeCompare(b.status);
      }
      return electionSortDir === 'asc' ? comp : -comp;
    });
  }, [elections, electionSortKey, electionSortDir]);

  // Form states
  const [newElection, setNewElection] = useState({
    title: '',
    election_type: 'GENERAL' as const,
    start_date: '2026-05-01',
    end_date: '2026-05-15',
    status: 'SCHEDULED' as const,
    total_registered_voters: 2500000,
    total_constituencies: 5,
    phases: 1,
    turnout_percentage: 0,
  });

  const [newCandidate, setNewCandidate] = useState({
    name: '',
    age: 35,
    email: '',
    phone: '',
    constituency_id: constituencies[0]?.id || '',
    party_id: parties[0]?.id || '',
    education: 'Graduate',
    declared_assets_cr: 2.5,
    criminal_cases: 0,
    affidavit_status: 'VERIFIED' as const,
  });

  const [newResult, setNewResult] = useState({
    election_id: elections[0]?.id || '',
    constituency_id: constituencies[0]?.id || '',
    candidate1_id: candidates[0]?.id || '',
    candidate1_votes: 550000,
    candidate2_id: candidates[1]?.id || '',
    candidate2_votes: 420000,
  });

  const [etlForm, setEtlForm] = useState({
    filename: 'constituency_turnout_feed_v4.csv',
    records: '150,000 records',
    provenance: 'Chief Electoral Officer / District Returning Officer',
  });

  // Export handlers
  const handleExportResultsPDF = () => {
    try {
      exportResultsPDF(results, constituencies, candidates, parties);
      onShowToast('Official Election Results exported as PDF.');
      setShowExportMenu(false);
    } catch (err: any) {
      onShowToast(`Failed to export PDF: ${err.message}`);
    }
  };

  const handleExportResultsCSV = () => {
    try {
      exportResultsCSV(results, constituencies, candidates, parties);
      onShowToast('Election Results exported as CSV.');
      setShowExportMenu(false);
    } catch (err: any) {
      onShowToast(`Failed to export CSV: ${err.message}`);
    }
  };

  const handleExportAuditLogsPDF = () => {
    try {
      exportAuditLogsPDF(auditLogs);
      onShowToast('Security & Audit Logs exported as PDF.');
      setShowExportMenu(false);
    } catch (err: any) {
      onShowToast(`Failed to export PDF: ${err.message}`);
    }
  };

  const handleExportAuditLogsCSV = () => {
    try {
      exportAuditLogsCSV(auditLogs);
      onShowToast('Audit Logs exported as CSV.');
      setShowExportMenu(false);
    } catch (err: any) {
      onShowToast(`Failed to export CSV: ${err.message}`);
    }
  };

  const handleScheduleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newElection.title) return;
    const title = newElection.title;
    onAddElection(newElection);
    setShowScheduleModal(false);
    announceOperation(`New election cycle scheduled: ${title}`);
    setNewElection({
      title: '',
      election_type: 'GENERAL',
      start_date: '2026-05-01',
      end_date: '2026-05-15',
      status: 'SCHEDULED',
      total_registered_voters: 2500000,
      total_constituencies: 5,
      phases: 1,
      turnout_percentage: 0,
    });
  };

  const handleCandidateSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newCandidate.name || !newCandidate.email) return;
    const name = newCandidate.name;
    onAddCandidate(newCandidate);
    setShowCandidateModal(false);
    announceOperation(`Candidate registered: ${name} filed Form 26 nomination affidavit.`);
    setNewCandidate({
      name: '',
      age: 35,
      email: '',
      phone: '',
      constituency_id: constituencies[0]?.id || '',
      party_id: parties[0]?.id || '',
      education: 'Graduate',
      declared_assets_cr: 2.5,
      criminal_cases: 0,
      affidavit_status: 'VERIFIED',
    });
  };

  const handleResultSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const totalVotes = newResult.candidate1_votes + newResult.candidate2_votes;
    const isCand1Winner = newResult.candidate1_votes >= newResult.candidate2_votes;
    const winningId = isCand1Winner ? newResult.candidate1_id : newResult.candidate2_id;
    const margin = Math.abs(newResult.candidate1_votes - newResult.candidate2_votes);

    onDeclareResult({
      result_key: `res-${newResult.constituency_id}-${Date.now().toString(36)}`,
      election_id: newResult.election_id,
      constituency_id: newResult.constituency_id,
      winning_candidate_id: winningId,
      total_votes: totalVotes,
      candidate_votes: {
        [newResult.candidate1_id]: newResult.candidate1_votes,
        [newResult.candidate2_id]: newResult.candidate2_votes,
      },
      margin,
      is_declared: true,
      declaration_time: new Date().toISOString(),
    });
    setShowResultModal(false);
    announceOperation('Statutory constituency election result officially declared with certified tally.');
  };

  const handleETLSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const { filename, records, provenance } = etlForm;
    onImportBatch(filename, records, provenance);
    setShowETLModal(false);

    // Audio status updates for long-running ETL processes via Web Speech API
    announceEtlStart(filename, records);

    // Progressive status updates
    setTimeout(() => {
      speakVoiceOver(`ETL batch ${filename} status: Parsed records, running cryptographic hash verification and schema normalization.`);
    }, 1800);

    setTimeout(() => {
      announceEtlComplete(filename, records);
    }, 4200);
  };

  return (
    <div className="p-6 sm:p-8 space-y-6 max-w-7xl mx-auto">
      {/* Sub-Navigation Switcher: Electoral Operations vs System Diagnostics */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-black/[0.06] dark:border-white/[0.08]">
        <div>
          <h2 className="text-2xl sm:text-3xl font-bold text-[#1d1d1f] dark:text-[#f5f5f7] tracking-tight">
            Operations Console
          </h2>
          <p className="text-[13px] text-[#86868b] dark:text-[#a1a1a6] mt-0.5">
            Command electoral cycles, verify storage integrity, and inspect real-time system diagnostics.
          </p>
        </div>

        {/* Apple HIG Segmented Pill Switcher */}
        <div className="inline-flex items-center p-1 bg-black/[0.04] dark:bg-white/[0.06] rounded-xl border border-black/[0.04] dark:border-white/[0.06] self-start sm:self-auto">
          <button
            type="button"
            onClick={() => setActiveTab('operations')}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-[13px] font-medium transition-all cursor-pointer ${
              activeTab === 'operations'
                ? 'bg-white dark:bg-[#2c2c2e] text-[#1d1d1f] dark:text-[#f5f5f7] shadow-sm'
                : 'text-[#86868b] dark:text-[#a1a1a6] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7]'
            }`}
          >
            <Sliders className="w-3.5 h-3.5 text-[#0071e3] dark:text-[#2997ff]" />
            <span>Electoral Operations</span>
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('diagnostics')}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-[13px] font-medium transition-all cursor-pointer ${
              activeTab === 'diagnostics'
                ? 'bg-white dark:bg-[#2c2c2e] text-[#1d1d1f] dark:text-[#f5f5f7] shadow-sm'
                : 'text-[#86868b] dark:text-[#a1a1a6] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7]'
            }`}
          >
            <Activity className="w-3.5 h-3.5 text-[#34c759] dark:text-[#30d158]" />
            <span>System Diagnostics</span>
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-[#34c759] opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-[#34c759]"></span>
            </span>
          </button>
        </div>
      </div>

      {/* Conditionally render System Diagnostics or Electoral Operations */}
      {activeTab === 'diagnostics' ? (
        <SystemDiagnosticsView />
      ) : (
        <div className="space-y-6">
          {/* Action Toolbar */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div className="flex items-center gap-2 text-[12px] text-[#86868b] dark:text-[#a1a1a6]">
              <span className="w-2 h-2 rounded-full bg-[#34c759]"></span>
              <span>All 4 Data Tables support ascending/descending column sorting</span>
            </div>

            {/* Action Buttons Group */}
            <div className="flex flex-wrap items-center gap-2 relative">
              {/* Export Dropdown Hub */}
              <div className="relative">
                <button
                  type="button"
                  onClick={() => setShowExportMenu(!showExportMenu)}
                  className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-black/[0.04] dark:bg-white/[0.06] hover:bg-black/[0.08] dark:hover:bg-white/[0.1] text-[#1d1d1f] dark:text-[#f5f5f7] text-[12px] font-medium transition-all cursor-pointer active:scale-95"
                  aria-label="Export Data and Reports"
                >
                  <Download className="w-3.5 h-3.5 text-[#0071e3] dark:text-[#2997ff]" />
                  <span>Export Reports</span>
                </button>

                {/* Dropdown Menu */}
                {showExportMenu && (
                  <div className="absolute right-0 top-10 z-40 w-64 rounded-2xl bg-white/95 dark:bg-[#1c1c1e]/95 backdrop-blur-2xl border border-black/[0.08] dark:border-white/[0.12] shadow-2xl p-2 text-[12px] space-y-1 animate-in fade-in zoom-in-95 duration-100">
                    <div className="px-3 py-1.5 text-[10px] font-semibold uppercase tracking-wider text-[#86868b] border-b border-black/[0.04] dark:border-white/[0.04]">
                      Election Results
                    </div>
                    <button
                      type="button"
                      onClick={handleExportResultsPDF}
                      className="w-full text-left px-3 py-2 rounded-xl hover:bg-black/[0.04] dark:hover:bg-white/[0.06] text-[#1d1d1f] dark:text-[#f5f5f7] flex items-center justify-between transition-colors cursor-pointer"
                    >
                      <span className="flex items-center gap-2">
                        <FileText className="w-3.5 h-3.5 text-[#ff3b30]" />
                        Export Results as PDF
                      </span>
                      <span className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-black/[0.04] dark:bg-white/[0.06] text-[#86868b]">
                        PDF
                      </span>
                    </button>
                    <button
                      type="button"
                      onClick={handleExportResultsCSV}
                      className="w-full text-left px-3 py-2 rounded-xl hover:bg-black/[0.04] dark:hover:bg-white/[0.06] text-[#1d1d1f] dark:text-[#f5f5f7] flex items-center justify-between transition-colors cursor-pointer"
                    >
                      <span className="flex items-center gap-2">
                        <Table className="w-3.5 h-3.5 text-[#34c759]" />
                        Export Results as CSV
                      </span>
                      <span className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-black/[0.04] dark:bg-white/[0.06] text-[#86868b]">
                        CSV
                      </span>
                    </button>

                    <div className="px-3 pt-2 pb-1 text-[10px] font-semibold uppercase tracking-wider text-[#86868b] border-t border-black/[0.04] dark:border-white/[0.04]">
                      Security &amp; Audit Logs
                    </div>
                    <button
                      type="button"
                      onClick={handleExportAuditLogsPDF}
                      className="w-full text-left px-3 py-2 rounded-xl hover:bg-black/[0.04] dark:hover:bg-white/[0.06] text-[#1d1d1f] dark:text-[#f5f5f7] flex items-center justify-between transition-colors cursor-pointer"
                    >
                      <span className="flex items-center gap-2">
                        <Shield className="w-3.5 h-3.5 text-[#0071e3] dark:text-[#2997ff]" />
                        Export Audit Logs (PDF)
                      </span>
                      <span className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-black/[0.04] dark:bg-white/[0.06] text-[#86868b]">
                        PDF
                      </span>
                    </button>
                    <button
                      type="button"
                      onClick={handleExportAuditLogsCSV}
                      className="w-full text-left px-3 py-2 rounded-xl hover:bg-black/[0.04] dark:hover:bg-white/[0.06] text-[#1d1d1f] dark:text-[#f5f5f7] flex items-center justify-between transition-colors cursor-pointer"
                    >
                      <span className="flex items-center gap-2">
                        <FileSpreadsheet className="w-3.5 h-3.5 text-[#34c759]" />
                        Export Audit Logs (CSV)
                      </span>
                      <span className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-black/[0.04] dark:bg-white/[0.06] text-[#86868b]">
                        CSV
                      </span>
                    </button>
                  </div>
                )}
              </div>

              <button
                type="button"
                onClick={() => setShowScheduleModal(true)}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-[#0071e3] hover:bg-[#0077ed] dark:bg-[#2997ff] dark:hover:bg-[#47a6ff] text-white text-[12px] font-medium shadow-sm transition-all cursor-pointer active:scale-95"
              >
                <CalendarPlus className="w-3.5 h-3.5" />
                Schedule Election
              </button>
              <button
                type="button"
                onClick={() => setShowCandidateModal(true)}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-black/[0.04] dark:bg-white/[0.06] hover:bg-black/[0.08] dark:hover:bg-white/[0.1] text-[#1d1d1f] dark:text-[#f5f5f7] text-[12px] font-medium transition-all cursor-pointer active:scale-95"
              >
                <UserPlus className="w-3.5 h-3.5 text-[#34c759] dark:text-[#30d158]" />
                Register Candidate
              </button>
              <button
                type="button"
                onClick={() => setShowResultModal(true)}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-black/[0.04] dark:bg-white/[0.06] hover:bg-black/[0.08] dark:hover:bg-white/[0.1] text-[#1d1d1f] dark:text-[#f5f5f7] text-[12px] font-medium transition-all cursor-pointer active:scale-95"
              >
                <Trophy className="w-3.5 h-3.5 text-[#ff9500] dark:text-[#ff9f0a]" />
                Declare Result
              </button>
              <button
                type="button"
                onClick={() => setShowETLModal(true)}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-black/[0.04] dark:bg-white/[0.06] hover:bg-black/[0.08] dark:hover:bg-white/[0.1] text-[#1d1d1f] dark:text-[#f5f5f7] text-[12px] font-medium transition-all cursor-pointer active:scale-95"
              >
                <Upload className="w-3.5 h-3.5 text-[#af52de] dark:text-[#bf5af2]" />
                Import ETL
              </button>
              <button
                type="button"
                onClick={() => setShowChecksumModal(true)}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-[#34c759]/10 hover:bg-[#34c759]/20 text-[#34c759] dark:text-[#30d158] border border-[#34c759]/20 text-[12px] font-medium transition-all cursor-pointer active:scale-95"
                title="Automated Checksum & Storage Integrity Validation (Detect data corruption)"
              >
                <ShieldCheck className="w-3.5 h-3.5" />
                <span>Verify Checksums</span>
              </button>
            </div>
          </div>

          {/* 4 Operations Metric Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <MetricCard
              title="Active Elections"
              value={`${elections.length}`}
              subtitle="Lok Sabha & State Assemblies"
              icon={Vote}
              iconColorClass="text-[#0071e3] dark:text-[#2997ff] bg-[#0071e3]/10 dark:bg-[#2997ff]/15"
              badgeText="Active"
              badgeColorClass="text-[#0071e3] dark:text-[#2997ff] bg-[#0071e3]/10"
            />
            <MetricCard
              title="Constituencies"
              value="543"
              subtitle="Lok Sabha Seats Indexed"
              icon={MapPin}
              iconColorClass="text-[#34c759] dark:text-[#30d158] bg-[#34c759]/10 dark:bg-[#30d158]/15"
            />
            <MetricCard
              title="Registered Candidates"
              value={`${candidates.length.toLocaleString()}`}
              subtitle="Form 26 Affidavits Processed"
              icon={UserPlus}
              iconColorClass="text-[#ff9500] dark:text-[#ff9f0a] bg-[#ff9500]/10 dark:bg-[#ff9f0a]/15"
            />
            <MetricCard
              title="ETL Pipeline"
              value={etlBatches[0]?.id || 'Batch-8841'}
              subtitle="100% Validated (0 Errors)"
              icon={RefreshCw}
              iconColorClass="text-[#af52de] dark:text-[#bf5af2] bg-[#af52de]/10 dark:bg-[#bf5af2]/15"
              badgeText="Nominal"
              badgeColorClass="text-[#34c759] dark:text-[#30d158] bg-[#34c759]/10"
            />
          </div>

          {/* Table 1: Declared Election Results with Column Sorting */}
          <div className="bg-white dark:bg-[#1c1c1e] border border-black/[0.06] dark:border-white/[0.08] rounded-2xl p-5 sm:p-6 shadow-[0_2px_12px_rgba(0,0,0,0.03)] dark:shadow-none transition-colors">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-black/[0.04] dark:border-white/[0.04]">
              <div>
                <div className="flex items-center gap-2">
                  <h3 className="text-[15px] font-semibold text-[#1d1d1f] dark:text-[#f5f5f7] flex items-center gap-2">
                    <Trophy className="w-4 h-4 text-[#ff9500] dark:text-[#ff9f0a]" />
                    Declared Constituency Results
                  </h3>
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-black/[0.04] dark:bg-white/[0.06] text-[#86868b]">
                    Sorted by {resultsSortKey} ({resultsSortDir.toUpperCase()})
                  </span>
                </div>
                <p className="text-[12px] text-[#86868b] dark:text-[#a1a1a6] mt-0.5">
                  Click any column header to toggle ascending or descending sort order
                </p>
              </div>

              <div className="flex items-center gap-2">
                {/* View Mode Switcher (Table vs Grid) */}
                <div className="flex items-center p-0.5 bg-black/[0.04] dark:bg-white/[0.06] rounded-xl border border-black/[0.04] dark:border-white/[0.06]">
                  <button
                    type="button"
                    onClick={() => setResultsViewMode('table')}
                    className={`p-1.5 rounded-lg transition-colors cursor-pointer ${
                      resultsViewMode === 'table'
                        ? 'bg-white dark:bg-[#2c2c2e] text-[#0071e3] dark:text-[#2997ff] shadow-sm'
                        : 'text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7]'
                    }`}
                    title="Table View"
                    aria-label="Table View"
                  >
                    <Table className="w-3.5 h-3.5" />
                  </button>
                  <button
                    type="button"
                    onClick={() => setResultsViewMode('cards')}
                    className={`p-1.5 rounded-lg transition-colors cursor-pointer ${
                      resultsViewMode === 'cards'
                        ? 'bg-white dark:bg-[#2c2c2e] text-[#0071e3] dark:text-[#2997ff] shadow-sm'
                        : 'text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7]'
                    }`}
                    title="Cards View"
                    aria-label="Cards View"
                  >
                    <LayoutGrid className="w-3.5 h-3.5" />
                  </button>
                </div>

                <button
                  type="button"
                  onClick={handleExportResultsPDF}
                  className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-[#0071e3]/10 dark:bg-[#2997ff]/15 hover:bg-[#0071e3]/20 text-[#0071e3] dark:text-[#2997ff] text-[12px] font-medium transition-all cursor-pointer active:scale-95"
                >
                  <FileText className="w-3.5 h-3.5" />
                  Export PDF
                </button>
                <button
                  type="button"
                  onClick={handleExportResultsCSV}
                  className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-black/[0.04] dark:bg-white/[0.06] hover:bg-black/[0.08] dark:hover:bg-white/[0.1] text-[#1d1d1f] dark:text-[#f5f5f7] text-[12px] font-medium transition-all cursor-pointer active:scale-95"
                >
                  <Table className="w-3.5 h-3.5" />
                  Export CSV
                </button>
              </div>
            </div>

            {resultsViewMode === 'table' ? (
              <div className="overflow-x-auto mt-3">
                <table className="w-full text-left">
                  <thead className="border-b border-black/[0.04] dark:border-white/[0.04]">
                    <tr>
                      <SortableHeader
                        label="Constituency"
                        sortKey="constituency"
                        currentKey={resultsSortKey}
                        direction={resultsSortDir}
                        onSort={toggleResultsSort}
                      />
                      <SortableHeader
                        label="State"
                        sortKey="state"
                        currentKey={resultsSortKey}
                        direction={resultsSortDir}
                        onSort={toggleResultsSort}
                      />
                      <SortableHeader
                        label="Winning Candidate"
                        sortKey="winner"
                        currentKey={resultsSortKey}
                        direction={resultsSortDir}
                        onSort={toggleResultsSort}
                      />
                      <SortableHeader
                        label="Party"
                        sortKey="party"
                        currentKey={resultsSortKey}
                        direction={resultsSortDir}
                        onSort={toggleResultsSort}
                      />
                      <SortableHeader
                        label="Victory Margin"
                        sortKey="margin"
                        currentKey={resultsSortKey}
                        direction={resultsSortDir}
                        onSort={toggleResultsSort}
                        align="right"
                      />
                      <SortableHeader
                        label="Total Polled"
                        sortKey="total_votes"
                        currentKey={resultsSortKey}
                        direction={resultsSortDir}
                        onSort={toggleResultsSort}
                        align="right"
                      />
                      <SortableHeader
                        label="Declaration Time"
                        sortKey="declaration_time"
                        currentKey={resultsSortKey}
                        direction={resultsSortDir}
                        onSort={toggleResultsSort}
                      />
                      <th scope="col" className="py-2.5 px-3 font-semibold text-[11px] uppercase tracking-wider text-[#86868b] text-right">
                        Status
                      </th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-black/[0.03] dark:divide-white/[0.03] text-[12px]">
                    {sortedResults.map((res) => {
                      const constituency = constituencies.find((c) => c.id === res.constituency_id);
                      const winner = candidates.find((can) => can.id === res.winning_candidate_id);
                      const party = parties.find((p) => p.id === winner?.party_id);
                      return (
                        <tr key={res.result_key} className="hover:bg-black/[0.02] dark:hover:bg-white/[0.02] transition-colors">
                          <td className="py-3 px-3 font-semibold text-[#1d1d1f] dark:text-[#f5f5f7] whitespace-nowrap">
                            {constituency?.name || 'Constituency'}
                            <span className="text-[11px] text-[#86868b] font-normal ml-1.5 font-mono">
                              ({constituency?.code || 'AC'})
                            </span>
                          </td>
                          <td className="py-3 px-3 text-[#86868b] dark:text-[#a1a1a6] whitespace-nowrap">
                            {constituency?.state_name || 'State'}
                          </td>
                          <td className="py-3 px-3 text-[#1d1d1f] dark:text-[#f5f5f7] font-medium whitespace-nowrap">
                            {winner?.name || 'Nominee'}
                          </td>
                          <td className="py-3 px-3 whitespace-nowrap">
                            <span className="px-2 py-0.5 rounded-md text-[11px] font-medium bg-black/[0.04] dark:bg-white/[0.06] text-[#1d1d1f] dark:text-[#f5f5f7]">
                              {party?.code || 'IND'}
                            </span>
                          </td>
                          <td className="py-3 px-3 text-right font-mono font-semibold text-[#34c759] dark:text-[#30d158] whitespace-nowrap">
                            +{res.margin.toLocaleString()}
                          </td>
                          <td className="py-3 px-3 text-right font-mono text-[#1d1d1f] dark:text-[#f5f5f7] whitespace-nowrap">
                            {res.total_votes.toLocaleString()}
                          </td>
                          <td className="py-3 px-3 text-[#86868b] dark:text-[#a1a1a6] font-mono text-[11px] whitespace-nowrap">
                            {res.declaration_time.replace('T', ' ').slice(0, 16)} UTC
                          </td>
                          <td className="py-3 px-3 text-right whitespace-nowrap">
                            <span className="text-[10px] font-semibold px-2 py-0.5 rounded-full text-[#34c759] dark:text-[#30d158] bg-[#34c759]/10">
                              DECLARED
                            </span>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3.5 mt-4">
                {sortedResults.map((res) => {
                  const constituency = constituencies.find((c) => c.id === res.constituency_id);
                  const winner = candidates.find((can) => can.id === res.winning_candidate_id);
                  const party = parties.find((p) => p.id === winner?.party_id);
                  return (
                    <div
                      key={res.result_key}
                      className="p-4 rounded-xl bg-black/[0.02] dark:bg-white/[0.03] border border-black/[0.04] dark:border-white/[0.04] flex flex-col justify-between"
                    >
                      <div>
                        <div className="flex items-start justify-between gap-2">
                          <div>
                            <div className="text-[13px] font-semibold text-[#1d1d1f] dark:text-[#f5f5f7]">
                              {constituency?.name} ({constituency?.code})
                            </div>
                            <div className="text-[11px] text-[#86868b] dark:text-[#a1a1a6]">
                              {constituency?.state_name}
                            </div>
                          </div>
                          <span className="text-[10px] font-medium px-2 py-0.5 rounded-full text-[#34c759] dark:text-[#30d158] bg-[#34c759]/10">
                            DECLARED
                          </span>
                        </div>

                        <div className="mt-3 pt-2 border-t border-black/[0.04] dark:border-white/[0.04] text-[12px] space-y-1">
                          <div className="flex items-center justify-between">
                            <span className="text-[#86868b] dark:text-[#a1a1a6]">Winner:</span>
                            <span className="font-medium text-[#1d1d1f] dark:text-[#f5f5f7]">
                              {winner?.name} ({party?.code})
                            </span>
                          </div>
                          <div className="flex items-center justify-between">
                            <span className="text-[#86868b] dark:text-[#a1a1a6]">Margin:</span>
                            <span className="font-mono font-semibold text-[#34c759] dark:text-[#30d158]">
                              +{res.margin.toLocaleString()} votes
                            </span>
                          </div>
                          <div className="flex items-center justify-between">
                            <span className="text-[#86868b] dark:text-[#a1a1a6]">Total Polled:</span>
                            <span className="font-mono text-[#1d1d1f] dark:text-[#f5f5f7]">
                              {res.total_votes.toLocaleString()}
                            </span>
                          </div>
                        </div>
                      </div>

                      <div className="mt-3 pt-2 border-t border-black/[0.04] dark:border-white/[0.04] text-[10px] text-[#86868b] dark:text-[#a1a1a6] font-mono">
                        {res.declaration_time.replace('T', ' ').slice(0, 16)} UTC
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>

          {/* Table 2: Operations Audit & Event Stream with Column Sorting */}
          <div className="bg-white dark:bg-[#1c1c1e] border border-black/[0.06] dark:border-white/[0.08] rounded-2xl p-5 sm:p-6 shadow-[0_2px_12px_rgba(0,0,0,0.03)] dark:shadow-none transition-colors">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-black/[0.04] dark:border-white/[0.04]">
              <div>
                <div className="flex items-center gap-2">
                  <h3 className="text-[15px] font-semibold text-[#1d1d1f] dark:text-[#f5f5f7] flex items-center gap-2">
                    <Shield className="w-4 h-4 text-[#0071e3] dark:text-[#2997ff]" />
                    Operations Audit &amp; Event Stream
                  </h3>
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-black/[0.04] dark:bg-white/[0.06] text-[#86868b]">
                    Sorted by {auditSortKey} ({auditSortDir.toUpperCase()})
                  </span>
                </div>
                <p className="text-[12px] text-[#86868b] dark:text-[#a1a1a6] mt-0.5">
                  Click headers to sort events by timestamp, actor, action, target resource, or status
                </p>
              </div>
              <div className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={handleExportAuditLogsPDF}
                  className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-[#0071e3]/10 dark:bg-[#2997ff]/15 hover:bg-[#0071e3]/20 text-[#0071e3] dark:text-[#2997ff] text-[12px] font-medium transition-all cursor-pointer active:scale-95"
                >
                  <FileText className="w-3.5 h-3.5" />
                  Export PDF
                </button>
                <button
                  type="button"
                  onClick={handleExportAuditLogsCSV}
                  className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-black/[0.04] dark:bg-white/[0.06] hover:bg-black/[0.08] dark:hover:bg-white/[0.1] text-[#1d1d1f] dark:text-[#f5f5f7] text-[12px] font-medium transition-all cursor-pointer active:scale-95"
                >
                  <Table className="w-3.5 h-3.5" />
                  Export CSV
                </button>
              </div>
            </div>

            <div className="overflow-x-auto mt-3">
              <table className="w-full text-left">
                <thead className="border-b border-black/[0.04] dark:border-white/[0.04]">
                  <tr>
                    <SortableHeader
                      label="Timestamp"
                      sortKey="timestamp"
                      currentKey={auditSortKey}
                      direction={auditSortDir}
                      onSort={toggleAuditSort}
                    />
                    <SortableHeader
                      label="Actor"
                      sortKey="actor"
                      currentKey={auditSortKey}
                      direction={auditSortDir}
                      onSort={toggleAuditSort}
                    />
                    <SortableHeader
                      label="Action"
                      sortKey="action"
                      currentKey={auditSortKey}
                      direction={auditSortDir}
                      onSort={toggleAuditSort}
                    />
                    <SortableHeader
                      label="Resource"
                      sortKey="resource"
                      currentKey={auditSortKey}
                      direction={auditSortDir}
                      onSort={toggleAuditSort}
                    />
                    <SortableHeader
                      label="Status"
                      sortKey="status"
                      currentKey={auditSortKey}
                      direction={auditSortDir}
                      onSort={toggleAuditSort}
                    />
                  </tr>
                </thead>
                <tbody className="divide-y divide-black/[0.03] dark:divide-white/[0.03] text-[12px]">
                  {sortedAuditLogs.map((log) => (
                    <tr key={log.id} className="hover:bg-black/[0.02] dark:hover:bg-white/[0.02] transition-colors">
                      <td className="py-3 px-3 text-[#86868b] dark:text-[#a1a1a6] font-mono whitespace-nowrap">
                        {log.timestamp}
                      </td>
                      <td className="py-3 px-3 font-semibold text-[#1d1d1f] dark:text-[#f5f5f7] whitespace-nowrap">
                        {log.actor}
                      </td>
                      <td className="py-3 px-3 text-[#0071e3] dark:text-[#2997ff] font-medium whitespace-nowrap">
                        {log.action}
                      </td>
                      <td className="py-3 px-3 text-[#1d1d1f] dark:text-[#f5f5f7] whitespace-nowrap">
                        {log.resource}
                      </td>
                      <td className="py-3 px-3 whitespace-nowrap">
                        <span className="text-[11px] font-medium text-[#34c759] dark:text-[#30d158] bg-[#34c759]/10 px-2 py-0.5 rounded-full">
                          {log.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Table 3: Recent ETL Ingestion Batches with Column Sorting */}
          <div className="bg-white dark:bg-[#1c1c1e] border border-black/[0.06] dark:border-white/[0.08] rounded-2xl p-5 sm:p-6 shadow-[0_2px_12px_rgba(0,0,0,0.03)] dark:shadow-none transition-colors">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-black/[0.04] dark:border-white/[0.04]">
              <div>
                <div className="flex items-center gap-2">
                  <h3 className="text-[15px] font-semibold text-[#1d1d1f] dark:text-[#f5f5f7] flex items-center gap-2">
                    <FileSpreadsheet className="w-4 h-4 text-[#af52de] dark:text-[#bf5af2]" />
                    Recent ETL Ingestion Batches
                  </h3>
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-black/[0.04] dark:bg-white/[0.06] text-[#86868b]">
                    Sorted by {etlSortKey} ({etlSortDir.toUpperCase()})
                  </span>
                </div>
                <p className="text-[12px] text-[#86868b] dark:text-[#a1a1a6] mt-0.5">
                  Click column headers to sort ingestion batches by Batch ID, source file, record count, or timestamps
                </p>
              </div>
              <button
                type="button"
                onClick={() => setShowETLModal(true)}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-black/[0.04] dark:bg-white/[0.06] hover:bg-black/[0.08] dark:hover:bg-white/[0.1] text-[#1d1d1f] dark:text-[#f5f5f7] text-[12px] font-medium transition-all cursor-pointer active:scale-95"
              >
                <Upload className="w-3.5 h-3.5" />
                Import CSV / JSON
              </button>
            </div>

            <div className="overflow-x-auto mt-3">
              <table className="w-full text-left">
                <thead className="border-b border-black/[0.04] dark:border-white/[0.04]">
                  <tr>
                    <SortableHeader
                      label="Batch ID"
                      sortKey="id"
                      currentKey={etlSortKey}
                      direction={etlSortDir}
                      onSort={toggleEtlSort}
                    />
                    <SortableHeader
                      label="Source File"
                      sortKey="sourceFile"
                      currentKey={etlSortKey}
                      direction={etlSortDir}
                      onSort={toggleEtlSort}
                    />
                    <SortableHeader
                      label="Records"
                      sortKey="recordsCount"
                      currentKey={etlSortKey}
                      direction={etlSortDir}
                      onSort={toggleEtlSort}
                      align="right"
                    />
                    <SortableHeader
                      label="Provenance"
                      sortKey="provenance"
                      currentKey={etlSortKey}
                      direction={etlSortDir}
                      onSort={toggleEtlSort}
                    />
                    <SortableHeader
                      label="Timestamp"
                      sortKey="importedAt"
                      currentKey={etlSortKey}
                      direction={etlSortDir}
                      onSort={toggleEtlSort}
                    />
                    <SortableHeader
                      label="Status"
                      sortKey="status"
                      currentKey={etlSortKey}
                      direction={etlSortDir}
                      onSort={toggleEtlSort}
                    />
                  </tr>
                </thead>
                <tbody className="divide-y divide-black/[0.03] dark:divide-white/[0.03] text-[12px]">
                  {sortedEtlBatches.map((batch) => (
                    <tr key={batch.id} className="hover:bg-black/[0.02] dark:hover:bg-white/[0.02] transition-colors">
                      <td className="py-3 px-3 font-semibold text-[#1d1d1f] dark:text-[#f5f5f7] whitespace-nowrap font-mono text-[11px]">
                        {batch.id}
                      </td>
                      <td className="py-3 px-3 text-[#0071e3] dark:text-[#2997ff] whitespace-nowrap">
                        {batch.sourceFile}
                      </td>
                      <td className="py-3 px-3 text-right text-[#1d1d1f] dark:text-[#f5f5f7] font-mono whitespace-nowrap">
                        {batch.recordsCount}
                      </td>
                      <td className="py-3 px-3 text-[#86868b] dark:text-[#a1a1a6] whitespace-nowrap">
                        {batch.provenance}
                      </td>
                      <td className="py-3 px-3 text-[#86868b] dark:text-[#a1a1a6] font-mono whitespace-nowrap">
                        {batch.importedAt}
                      </td>
                      <td className="py-3 px-3 whitespace-nowrap">
                        <span className="text-[11px] font-medium text-[#34c759] dark:text-[#30d158] bg-[#34c759]/10 px-2 py-0.5 rounded-full">
                          {batch.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Storage Layer Checksum & Cryptographic Integrity Card */}
          <div className="bg-white dark:bg-[#1c1c1e] border border-black/[0.06] dark:border-white/[0.08] rounded-2xl p-5 sm:p-6 shadow-[0_2px_12px_rgba(0,0,0,0.03)] dark:shadow-none transition-colors">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-black/[0.04] dark:border-white/[0.04]">
              <div className="flex items-center gap-3">
                <div className="w-9 h-9 rounded-xl bg-[#34c759]/10 text-[#34c759] dark:text-[#30d158] flex items-center justify-center shrink-0">
                  <ShieldCheck className="w-5 h-5" />
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <h3 className="text-[15px] font-semibold text-[#1d1d1f] dark:text-[#f5f5f7]">
                      Storage Layer Checksum &amp; Integrity Verification
                    </h3>
                    <span className="text-[11px] font-medium text-[#34c759] bg-[#34c759]/10 px-2.5 py-0.5 rounded-full">
                      Automated SHA-256
                    </span>
                  </div>
                  <p className="text-[12px] text-[#86868b] dark:text-[#a1a1a6] mt-0.5">
                    Bitwise integrity validation checks on electoral volumes to detect silent data corruption or unauthorized storage edits
                  </p>
                </div>
              </div>

              <div className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={() => setShowChecksumModal(true)}
                  className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-[#0071e3] hover:bg-[#0077ed] text-white text-[12px] font-medium shadow-sm transition-all cursor-pointer active:scale-95"
                >
                  <ShieldCheck className="w-4 h-4" />
                  <span>Run Automated Checksum Scan</span>
                </button>
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-4">
              <div className="p-3 rounded-xl bg-black/[0.02] dark:bg-white/[0.03] border border-black/[0.04] dark:border-white/[0.04]">
                <div className="text-[11px] text-[#86868b] font-medium">Monitored Storage Volumes</div>
                <div className="text-lg font-bold text-[#1d1d1f] dark:text-[#f5f5f7] mt-0.5">
                  6 Electoral Partitions
                </div>
                <div className="text-[10px] text-[#86868b] mt-0.5">Constituencies, Candidates, Form 20 Results, ETL</div>
              </div>

              <div className="p-3 rounded-xl bg-black/[0.02] dark:bg-white/[0.03] border border-black/[0.04] dark:border-white/[0.04]">
                <div className="text-[11px] text-[#86868b] font-medium">Cryptographic Standard</div>
                <div className="text-lg font-bold text-[#34c759] mt-0.5">
                  FIPS 180-4 (SHA-256)
                </div>
                <div className="text-[10px] text-[#86868b] mt-0.5">Bit-for-bit Merkle Tree validation</div>
              </div>

              <div className="p-3 rounded-xl bg-black/[0.02] dark:bg-white/[0.03] border border-black/[0.04] dark:border-white/[0.04]">
                <div className="text-[11px] text-[#86868b] font-medium">Anomaly Detection Guard</div>
                <div className="text-lg font-bold text-[#0071e3] dark:text-[#2997ff] mt-0.5">
                  Active Protection
                </div>
                <div className="text-[10px] text-[#86868b] mt-0.5">Automated bit-rot &amp; unauthorized tamper traps</div>
              </div>
            </div>
          </div>

          {/* Table 4: Scheduled & Active Elections Table with Column Sorting */}
          <div className="bg-white dark:bg-[#1c1c1e] border border-black/[0.06] dark:border-white/[0.08] rounded-2xl p-5 sm:p-6 shadow-[0_2px_12px_rgba(0,0,0,0.03)] dark:shadow-none transition-colors">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-black/[0.04] dark:border-white/[0.04]">
              <div>
                <div className="flex items-center gap-2">
                  <h3 className="text-[15px] font-semibold text-[#1d1d1f] dark:text-[#f5f5f7]">
                    Scheduled &amp; Active Elections
                  </h3>
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-black/[0.04] dark:bg-white/[0.06] text-[#86868b]">
                    Sorted by {electionSortKey} ({electionSortDir.toUpperCase()})
                  </span>
                </div>
                <p className="text-[12px] text-[#86868b] dark:text-[#a1a1a6] mt-0.5">
                  Click headers to sort election cycles by title, type, date, constituencies, or turnout
                </p>
              </div>

              <div className="flex items-center gap-2">
                <span className="text-[11px] font-medium text-[#86868b] dark:text-[#a1a1a6]">
                  {sortedElections.length} Records
                </span>
                <button
                  type="button"
                  onClick={() => setShowScheduleModal(true)}
                  className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-[#0071e3] hover:bg-[#0077ed] dark:bg-[#2997ff] dark:hover:bg-[#47a6ff] text-white text-[12px] font-medium shadow-sm transition-all cursor-pointer active:scale-95"
                >
                  <Plus className="w-3.5 h-3.5" />
                  New Election
                </button>
              </div>
            </div>

            <div className="overflow-x-auto mt-3">
              <table className="w-full text-left">
                <thead className="border-b border-black/[0.04] dark:border-white/[0.04]">
                  <tr>
                    <SortableHeader
                      label="Election Title"
                      sortKey="title"
                      currentKey={electionSortKey}
                      direction={electionSortDir}
                      onSort={toggleElectionSort}
                    />
                    <SortableHeader
                      label="Type"
                      sortKey="election_type"
                      currentKey={electionSortKey}
                      direction={electionSortDir}
                      onSort={toggleElectionSort}
                    />
                    <SortableHeader
                      label="Date Range"
                      sortKey="start_date"
                      currentKey={electionSortKey}
                      direction={electionSortDir}
                      onSort={toggleElectionSort}
                    />
                    <SortableHeader
                      label="Seats"
                      sortKey="total_constituencies"
                      currentKey={electionSortKey}
                      direction={electionSortDir}
                      onSort={toggleElectionSort}
                      align="right"
                    />
                    <SortableHeader
                      label="Turnout %"
                      sortKey="turnout_percentage"
                      currentKey={electionSortKey}
                      direction={electionSortDir}
                      onSort={toggleElectionSort}
                      align="right"
                    />
                    <SortableHeader
                      label="Status"
                      sortKey="status"
                      currentKey={electionSortKey}
                      direction={electionSortDir}
                      onSort={toggleElectionSort}
                    />
                  </tr>
                </thead>
                <tbody className="divide-y divide-black/[0.03] dark:divide-white/[0.03] text-[12px]">
                  {sortedElections.map((elec) => (
                    <tr key={elec.id} className="hover:bg-black/[0.02] dark:hover:bg-white/[0.02] transition-colors">
                      <td className="py-3 px-3 font-semibold text-[#1d1d1f] dark:text-[#f5f5f7] whitespace-nowrap">
                        {elec.title}
                      </td>
                      <td className="py-3 px-3 text-[#0071e3] dark:text-[#2997ff] font-medium whitespace-nowrap">
                        {elec.election_type}
                      </td>
                      <td className="py-3 px-3 text-[#86868b] dark:text-[#a1a1a6] font-mono text-[11px] whitespace-nowrap">
                        {elec.start_date} to {elec.end_date}
                      </td>
                      <td className="py-3 px-3 text-right font-mono text-[#1d1d1f] dark:text-[#f5f5f7] whitespace-nowrap">
                        {elec.total_constituencies}
                      </td>
                      <td className="py-3 px-3 text-right font-mono font-medium text-[#34c759] dark:text-[#30d158] whitespace-nowrap">
                        {elec.turnout_percentage > 0 ? `${elec.turnout_percentage}%` : 'Pending'}
                      </td>
                      <td className="py-3 px-3 whitespace-nowrap">
                        <span
                          className={`text-[11px] font-medium px-2.5 py-0.5 rounded-full ${
                            elec.status === 'ACTIVE'
                              ? 'bg-[#0071e3]/10 text-[#0071e3] dark:text-[#2997ff]'
                              : elec.status === 'COMPLETED'
                              ? 'bg-[#34c759]/10 text-[#34c759] dark:text-[#30d158]'
                              : 'bg-[#ff9500]/10 text-[#ff9500] dark:text-[#ff9f0a]'
                          }`}
                        >
                          {elec.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* SCHEDULE ELECTION MODAL */}
      {showScheduleModal && (
        <div className="fixed inset-0 z-50 bg-black/40 dark:bg-black/65 backdrop-blur-md flex items-center justify-center p-4">
          <div className="bg-white/95 dark:bg-[#1e1e1e]/95 backdrop-blur-2xl border border-black/[0.08] dark:border-white/[0.12] rounded-2xl w-full max-w-lg p-6 shadow-2xl">
            <h3 className="text-[17px] font-semibold text-[#1d1d1f] dark:text-[#f5f5f7] tracking-tight mb-0.5">Schedule New Election</h3>
            <p className="text-[12px] text-[#86868b] dark:text-[#a1a1a6] mb-5">
              Create an official election cycle through CQRS CommandPipeline
            </p>
            <form onSubmit={handleScheduleSubmit} className="space-y-4">
              <div>
                <label className="block text-[11px] font-medium text-[#86868b] dark:text-[#a1a1a6] tracking-tight mb-1">
                  Election Title
                </label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Maharashtra Assembly Election 2026"
                  value={newElection.title}
                  onChange={(e) => setNewElection({ ...newElection, title: e.target.value })}
                  className="w-full bg-black/[0.03] dark:bg-white/[0.05] border border-black/[0.08] dark:border-white/[0.1] rounded-xl px-3 py-2 text-[#1d1d1f] dark:text-[#f5f5f7] text-[13px] focus:outline-none focus:ring-2 focus:ring-[#0071e3]/40 dark:focus:ring-[#2997ff]/40 transition"
                />
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-[11px] font-medium text-[#86868b] dark:text-[#a1a1a6] tracking-tight mb-1">
                    Election Type
                  </label>
                  <select
                    value={newElection.election_type}
                    onChange={(e) => setNewElection({ ...newElection, election_type: e.target.value as any })}
                    className="w-full bg-black/[0.03] dark:bg-white/[0.05] border border-black/[0.08] dark:border-white/[0.1] rounded-xl px-3 py-2 text-[#1d1d1f] dark:text-[#f5f5f7] text-[13px] focus:outline-none focus:ring-2 focus:ring-[#0071e3]/40 dark:focus:ring-[#2997ff]/40 transition"
                  >
                    <option value="GENERAL">GENERAL</option>
                    <option value="ASSEMBLY">ASSEMBLY</option>
                    <option value="BY_ELECTION">BY_ELECTION</option>
                    <option value="MUNICIPAL">MUNICIPAL</option>
                  </select>
                </div>
                <div>
                  <label className="block text-[11px] font-medium text-[#86868b] dark:text-[#a1a1a6] tracking-tight mb-1">
                    Constituencies Count
                  </label>
                  <input
                    type="number"
                    value={newElection.total_constituencies}
                    onChange={(e) => setNewElection({ ...newElection, total_constituencies: parseInt(e.target.value) || 1 })}
                    className="w-full bg-black/[0.03] dark:bg-white/[0.05] border border-black/[0.08] dark:border-white/[0.1] rounded-xl px-3 py-2 text-[#1d1d1f] dark:text-[#f5f5f7] text-[13px] focus:outline-none focus:ring-2 focus:ring-[#0071e3]/40 dark:focus:ring-[#2997ff]/40 transition"
                  />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-[11px] font-medium text-[#86868b] dark:text-[#a1a1a6] tracking-tight mb-1">
                    Start Date
                  </label>
                  <input
                    type="date"
                    required
                    value={newElection.start_date}
                    onChange={(e) => setNewElection({ ...newElection, start_date: e.target.value })}
                    className="w-full bg-black/[0.03] dark:bg-white/[0.05] border border-black/[0.08] dark:border-white/[0.1] rounded-xl px-3 py-2 text-[#1d1d1f] dark:text-[#f5f5f7] text-[13px] focus:outline-none focus:ring-2 focus:ring-[#0071e3]/40 dark:focus:ring-[#2997ff]/40 transition"
                  />
                </div>
                <div>
                  <label className="block text-[11px] font-medium text-[#86868b] dark:text-[#a1a1a6] tracking-tight mb-1">
                    End Date
                  </label>
                  <input
                    type="date"
                    required
                    value={newElection.end_date}
                    onChange={(e) => setNewElection({ ...newElection, end_date: e.target.value })}
                    className="w-full bg-black/[0.03] dark:bg-white/[0.05] border border-black/[0.08] dark:border-white/[0.1] rounded-xl px-3 py-2 text-[#1d1d1f] dark:text-[#f5f5f7] text-[13px] focus:outline-none focus:ring-2 focus:ring-[#0071e3]/40 dark:focus:ring-[#2997ff]/40 transition"
                  />
                </div>
              </div>
              <div className="flex items-center justify-end gap-2 pt-4 border-t border-black/[0.06] dark:border-white/[0.08]">
                <button
                  type="button"
                  onClick={() => setShowScheduleModal(false)}
                  className="px-3.5 py-1.5 rounded-xl bg-black/[0.04] dark:bg-white/[0.06] hover:bg-black/[0.08] dark:hover:bg-white/[0.1] text-[#1d1d1f] dark:text-[#f5f5f7] text-[13px] font-medium transition cursor-pointer"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-1.5 rounded-xl bg-[#0071e3] hover:bg-[#0077ed] text-white text-[13px] font-medium shadow-sm transition active:scale-[0.98] cursor-pointer"
                >
                  Schedule Election
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* REGISTER CANDIDATE MODAL */}
      {showCandidateModal && (
        <div className="fixed inset-0 z-50 bg-black/40 dark:bg-black/65 backdrop-blur-md flex items-center justify-center p-4">
          <div className="bg-white/95 dark:bg-[#1e1e1e]/95 backdrop-blur-2xl border border-black/[0.08] dark:border-white/[0.12] rounded-2xl w-full max-w-lg p-6 shadow-2xl">
            <h3 className="text-[17px] font-semibold text-[#1d1d1f] dark:text-[#f5f5f7] tracking-tight mb-0.5">Register New Candidate</h3>
            <p className="text-[12px] text-[#86868b] dark:text-[#a1a1a6] mb-5">
              File statutory nomination affidavit under Form 26
            </p>
            <form onSubmit={handleCandidateSubmit} className="space-y-4">
              <div>
                <label className="block text-[11px] font-medium text-[#86868b] dark:text-[#a1a1a6] tracking-tight mb-1">
                  Candidate Full Name
                </label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Priya Sharma"
                  value={newCandidate.name}
                  onChange={(e) => setNewCandidate({ ...newCandidate, name: e.target.value })}
                  className="w-full bg-black/[0.03] dark:bg-white/[0.05] border border-black/[0.08] dark:border-white/[0.1] rounded-xl px-3 py-2 text-[#1d1d1f] dark:text-[#f5f5f7] text-[13px] focus:outline-none focus:ring-2 focus:ring-[#0071e3]/40 dark:focus:ring-[#2997ff]/40 transition"
                />
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-[11px] font-medium text-[#86868b] dark:text-[#a1a1a6] tracking-tight mb-1">
                    Constituency
                  </label>
                  <select
                    value={newCandidate.constituency_id}
                    onChange={(e) => setNewCandidate({ ...newCandidate, constituency_id: e.target.value })}
                    className="w-full bg-black/[0.03] dark:bg-white/[0.05] border border-black/[0.08] dark:border-white/[0.1] rounded-xl px-3 py-2 text-[#1d1d1f] dark:text-[#f5f5f7] text-[13px] focus:outline-none focus:ring-2 focus:ring-[#0071e3]/40 dark:focus:ring-[#2997ff]/40 transition"
                  >
                    {constituencies.map((c) => (
                      <option key={c.id} value={c.id}>
                        {c.name} ({c.code})
                      </option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-[11px] font-medium text-[#86868b] dark:text-[#a1a1a6] tracking-tight mb-1">
                    Political Party
                  </label>
                  <select
                    value={newCandidate.party_id}
                    onChange={(e) => setNewCandidate({ ...newCandidate, party_id: e.target.value })}
                    className="w-full bg-black/[0.03] dark:bg-white/[0.05] border border-black/[0.08] dark:border-white/[0.1] rounded-xl px-3 py-2 text-[#1d1d1f] dark:text-[#f5f5f7] text-[13px] focus:outline-none focus:ring-2 focus:ring-[#0071e3]/40 dark:focus:ring-[#2997ff]/40 transition"
                  >
                    {parties.map((p) => (
                      <option key={p.id} value={p.id}>
                        {p.name} ({p.code})
                      </option>
                    ))}
                  </select>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-[11px] font-medium text-[#86868b] dark:text-[#a1a1a6] tracking-tight mb-1">
                    Email Address
                  </label>
                  <input
                    type="email"
                    required
                    placeholder="candidate@election.in"
                    value={newCandidate.email}
                    onChange={(e) => setNewCandidate({ ...newCandidate, email: e.target.value })}
                    className="w-full bg-black/[0.03] dark:bg-white/[0.05] border border-black/[0.08] dark:border-white/[0.1] rounded-xl px-3 py-2 text-[#1d1d1f] dark:text-[#f5f5f7] text-[13px] focus:outline-none focus:ring-2 focus:ring-[#0071e3]/40 dark:focus:ring-[#2997ff]/40 transition"
                  />
                </div>
                <div>
                  <label className="block text-[11px] font-medium text-[#86868b] dark:text-[#a1a1a6] tracking-tight mb-1">
                    Phone Number
                  </label>
                  <input
                    type="tel"
                    required
                    placeholder="+919876543210"
                    value={newCandidate.phone}
                    onChange={(e) => setNewCandidate({ ...newCandidate, phone: e.target.value })}
                    className="w-full bg-black/[0.03] dark:bg-white/[0.05] border border-black/[0.08] dark:border-white/[0.1] rounded-xl px-3 py-2 text-[#1d1d1f] dark:text-[#f5f5f7] text-[13px] focus:outline-none focus:ring-2 focus:ring-[#0071e3]/40 dark:focus:ring-[#2997ff]/40 transition"
                  />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-[11px] font-medium text-[#86868b] dark:text-[#a1a1a6] tracking-tight mb-1">
                    Declared Assets (₹ Crores)
                  </label>
                  <input
                    type="number"
                    step="0.01"
                    value={newCandidate.declared_assets_cr}
                    onChange={(e) => setNewCandidate({ ...newCandidate, declared_assets_cr: parseFloat(e.target.value) || 0 })}
                    className="w-full bg-black/[0.03] dark:bg-white/[0.05] border border-black/[0.08] dark:border-white/[0.1] rounded-xl px-3 py-2 text-[#1d1d1f] dark:text-[#f5f5f7] text-[13px] focus:outline-none focus:ring-2 focus:ring-[#0071e3]/40 dark:focus:ring-[#2997ff]/40 transition"
                  />
                </div>
                <div>
                  <label className="block text-[11px] font-medium text-[#86868b] dark:text-[#a1a1a6] tracking-tight mb-1">
                    Criminal Cases
                  </label>
                  <input
                    type="number"
                    value={newCandidate.criminal_cases}
                    onChange={(e) => setNewCandidate({ ...newCandidate, criminal_cases: parseInt(e.target.value) || 0 })}
                    className="w-full bg-black/[0.03] dark:bg-white/[0.05] border border-black/[0.08] dark:border-white/[0.1] rounded-xl px-3 py-2 text-[#1d1d1f] dark:text-[#f5f5f7] text-[13px] focus:outline-none focus:ring-2 focus:ring-[#0071e3]/40 dark:focus:ring-[#2997ff]/40 transition"
                  />
                </div>
              </div>
              <div className="flex items-center justify-end gap-2 pt-4 border-t border-black/[0.06] dark:border-white/[0.08]">
                <button
                  type="button"
                  onClick={() => setShowCandidateModal(false)}
                  className="px-3.5 py-1.5 rounded-xl bg-black/[0.04] dark:bg-white/[0.06] hover:bg-black/[0.08] dark:hover:bg-white/[0.1] text-[#1d1d1f] dark:text-[#f5f5f7] text-[13px] font-medium transition cursor-pointer"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-1.5 rounded-xl bg-[#0071e3] hover:bg-[#0077ed] text-white text-[13px] font-medium shadow-sm transition active:scale-[0.98] cursor-pointer"
                >
                  Register Candidate
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* DECLARE RESULT MODAL */}
      {showResultModal && (
        <div className="fixed inset-0 z-50 bg-black/40 dark:bg-black/65 backdrop-blur-md flex items-center justify-center p-4">
          <div className="bg-white/95 dark:bg-[#1e1e1e]/95 backdrop-blur-2xl border border-black/[0.08] dark:border-white/[0.12] rounded-2xl w-full max-w-lg p-6 shadow-2xl">
            <h3 className="text-[17px] font-semibold text-[#1d1d1f] dark:text-[#f5f5f7] tracking-tight mb-0.5">Declare Constituency Result</h3>
            <p className="text-[12px] text-[#86868b] dark:text-[#a1a1a6] mb-5">
              Tally EVM &amp; Postal ballot votes and declare statutory winner
            </p>
            <form onSubmit={handleResultSubmit} className="space-y-4">
              <div>
                <label className="block text-[11px] font-medium text-[#86868b] dark:text-[#a1a1a6] tracking-tight mb-1">
                  Constituency
                </label>
                <select
                  value={newResult.constituency_id}
                  onChange={(e) => setNewResult({ ...newResult, constituency_id: e.target.value })}
                  className="w-full bg-black/[0.03] dark:bg-white/[0.05] border border-black/[0.08] dark:border-white/[0.1] rounded-xl px-3 py-2 text-[#1d1d1f] dark:text-[#f5f5f7] text-[13px] focus:outline-none focus:ring-2 focus:ring-[#0071e3]/40 dark:focus:ring-[#2997ff]/40 transition"
                >
                  {constituencies.map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.name} ({c.code}) - {c.state_name}
                    </option>
                  ))}
                </select>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-[11px] font-medium text-[#86868b] dark:text-[#a1a1a6] tracking-tight mb-1">
                    Leading Candidate
                  </label>
                  <select
                    value={newResult.candidate1_id}
                    onChange={(e) => setNewResult({ ...newResult, candidate1_id: e.target.value })}
                    className="w-full bg-black/[0.03] dark:bg-white/[0.05] border border-black/[0.08] dark:border-white/[0.1] rounded-xl px-3 py-2 text-[#1d1d1f] dark:text-[#f5f5f7] text-[13px] focus:outline-none focus:ring-2 focus:ring-[#0071e3]/40 dark:focus:ring-[#2997ff]/40 transition"
                  >
                    {candidates.map((c) => (
                      <option key={c.id} value={c.id}>
                        {c.name}
                      </option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-[11px] font-medium text-[#86868b] dark:text-[#a1a1a6] tracking-tight mb-1">
                    Votes Polled
                  </label>
                  <input
                    type="number"
                    value={newResult.candidate1_votes}
                    onChange={(e) => setNewResult({ ...newResult, candidate1_votes: parseInt(e.target.value) || 0 })}
                    className="w-full bg-black/[0.03] dark:bg-white/[0.05] border border-black/[0.08] dark:border-white/[0.1] rounded-xl px-3 py-2 text-[#1d1d1f] dark:text-[#f5f5f7] text-[13px] focus:outline-none focus:ring-2 focus:ring-[#0071e3]/40 dark:focus:ring-[#2997ff]/40 transition"
                  />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-[11px] font-medium text-[#86868b] dark:text-[#a1a1a6] tracking-tight mb-1">
                    Runner-up Candidate
                  </label>
                  <select
                    value={newResult.candidate2_id}
                    onChange={(e) => setNewResult({ ...newResult, candidate2_id: e.target.value })}
                    className="w-full bg-black/[0.03] dark:bg-white/[0.05] border border-black/[0.08] dark:border-white/[0.1] rounded-xl px-3 py-2 text-[#1d1d1f] dark:text-[#f5f5f7] text-[13px] focus:outline-none focus:ring-2 focus:ring-[#0071e3]/40 dark:focus:ring-[#2997ff]/40 transition"
                  >
                    {candidates.map((c) => (
                      <option key={c.id} value={c.id}>
                        {c.name}
                      </option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-[11px] font-medium text-[#86868b] dark:text-[#a1a1a6] tracking-tight mb-1">
                    Votes Polled
                  </label>
                  <input
                    type="number"
                    value={newResult.candidate2_votes}
                    onChange={(e) => setNewResult({ ...newResult, candidate2_votes: parseInt(e.target.value) || 0 })}
                    className="w-full bg-black/[0.03] dark:bg-white/[0.05] border border-black/[0.08] dark:border-white/[0.1] rounded-xl px-3 py-2 text-[#1d1d1f] dark:text-[#f5f5f7] text-[13px] focus:outline-none focus:ring-2 focus:ring-[#0071e3]/40 dark:focus:ring-[#2997ff]/40 transition"
                  />
                </div>
              </div>
              <div className="flex items-center justify-end gap-2 pt-4 border-t border-black/[0.06] dark:border-white/[0.08]">
                <button
                  type="button"
                  onClick={() => setShowResultModal(false)}
                  className="px-3.5 py-1.5 rounded-xl bg-black/[0.04] dark:bg-white/[0.06] hover:bg-black/[0.08] dark:hover:bg-white/[0.1] text-[#1d1d1f] dark:text-[#f5f5f7] text-[13px] font-medium transition cursor-pointer"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-1.5 rounded-xl bg-[#34c759] hover:bg-[#30be53] text-white text-[13px] font-medium shadow-sm transition active:scale-[0.98] cursor-pointer"
                >
                  Declare Official Result
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* IMPORT ETL MODAL */}
      {showETLModal && (
        <div className="fixed inset-0 z-50 bg-black/40 dark:bg-black/65 backdrop-blur-md flex items-center justify-center p-4">
          <div className="bg-white/95 dark:bg-[#1e1e1e]/95 backdrop-blur-2xl border border-black/[0.08] dark:border-white/[0.12] rounded-2xl w-full max-w-lg p-6 shadow-2xl">
            <h3 className="text-[17px] font-semibold text-[#1d1d1f] dark:text-[#f5f5f7] tracking-tight mb-0.5">Trigger ETL Ingestion Batch</h3>
            <p className="text-[12px] text-[#86868b] dark:text-[#a1a1a6] mb-5">
              Load CSV/JSON electoral files through validated ETL pipeline
            </p>
            <form onSubmit={handleETLSubmit} className="space-y-4">
              <div>
                <label className="block text-[11px] font-medium text-[#86868b] dark:text-[#a1a1a6] tracking-tight mb-1">
                  Source File Name
                </label>
                <input
                  type="text"
                  required
                  value={etlForm.filename}
                  onChange={(e) => setEtlForm({ ...etlForm, filename: e.target.value })}
                  className="w-full bg-black/[0.03] dark:bg-white/[0.05] border border-black/[0.08] dark:border-white/[0.1] rounded-xl px-3 py-2 text-[#1d1d1f] dark:text-[#f5f5f7] text-[13px] font-mono focus:outline-none focus:ring-2 focus:ring-[#0071e3]/40 dark:focus:ring-[#2997ff]/40 transition"
                />
              </div>
              <div>
                <label className="block text-[11px] font-medium text-[#86868b] dark:text-[#a1a1a6] tracking-tight mb-1">
                  Estimated Record Volume
                </label>
                <input
                  type="text"
                  required
                  value={etlForm.records}
                  onChange={(e) => setEtlForm({ ...etlForm, records: e.target.value })}
                  className="w-full bg-black/[0.03] dark:bg-white/[0.05] border border-black/[0.08] dark:border-white/[0.1] rounded-xl px-3 py-2 text-[#1d1d1f] dark:text-[#f5f5f7] text-[13px] focus:outline-none focus:ring-2 focus:ring-[#0071e3]/40 dark:focus:ring-[#2997ff]/40 transition"
                />
              </div>
              <div>
                <label className="block text-[11px] font-medium text-[#86868b] dark:text-[#a1a1a6] tracking-tight mb-1">
                  Provenance Source
                </label>
                <input
                  type="text"
                  required
                  value={etlForm.provenance}
                  onChange={(e) => setEtlForm({ ...etlForm, provenance: e.target.value })}
                  className="w-full bg-black/[0.03] dark:bg-white/[0.05] border border-black/[0.08] dark:border-white/[0.1] rounded-xl px-3 py-2 text-[#1d1d1f] dark:text-[#f5f5f7] text-[13px] focus:outline-none focus:ring-2 focus:ring-[#0071e3]/40 dark:focus:ring-[#2997ff]/40 transition"
                />
              </div>
              <div className="flex items-center justify-end gap-2 pt-4 border-t border-black/[0.06] dark:border-white/[0.08]">
                <button
                  type="button"
                  onClick={() => setShowETLModal(false)}
                  className="px-3.5 py-1.5 rounded-xl bg-black/[0.04] dark:bg-white/[0.06] hover:bg-black/[0.08] dark:hover:bg-white/[0.1] text-[#1d1d1f] dark:text-[#f5f5f7] text-[13px] font-medium transition cursor-pointer"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-1.5 rounded-xl bg-[#af52de] hover:bg-[#a143d2] text-white text-[13px] font-medium shadow-sm transition active:scale-[0.98] cursor-pointer"
                >
                  Start Ingestion
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* STORAGE LAYER CHECKSUM VALIDATION MODAL */}
      <StorageChecksumModal
        isOpen={showChecksumModal}
        onClose={() => setShowChecksumModal(false)}
        onLogAudit={(action, resource, status) => {
          onShowToast(`Checksum scan completed: ${status}`);
        }}
      />
    </div>
  );
}
