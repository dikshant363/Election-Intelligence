'use client';

import React, { useState } from 'react';
import {
  Cpu,
  HardDrive,
  Database,
  Zap,
  Bot,
  ShieldCheck,
  Quote,
  Sliders,
  Download,
  Users,
  CheckCircle,
  FileText,
  Volume2,
  VolumeX,
  Radio,
  Play,
  AlertTriangle,
} from 'lucide-react';
import { MetricCard } from './MetricCard';
import { FeatureFlag, SystemHealthMetrics, AuditLog, UserAccount } from '@/lib/types';
import { exportAuditLogsCSV, exportAuditLogsPDF } from '@/lib/exportUtils';
import {
  getVoiceOverState,
  setVoiceOverState,
  subscribeVoiceOver,
  speakVoiceOver,
  announceCriticalAlert,
  announceEtlStart,
  announceEtlComplete,
  isVoiceOverSupported,
} from '@/lib/voiceOver';

interface EnterpriseControlCenterViewProps {
  metrics: SystemHealthMetrics;
  featureFlags: FeatureFlag[];
  auditLogs: AuditLog[];
  userAccounts: UserAccount[];
  onToggleFlag: (flagName: string) => void;
  onOpenModelConfig: () => void;
}

export function EnterpriseControlCenterView({
  metrics,
  featureFlags,
  auditLogs,
  userAccounts,
  onToggleFlag,
  onOpenModelConfig,
}: EnterpriseControlCenterViewProps) {
  const [filterAction, setFilterAction] = useState<string>('ALL');
  const [voiceOverEnabled, setVoiceOverEnabled] = useState(false);
  const [lastSpeechStatus, setLastSpeechStatus] = useState<string | null>(null);

  React.useEffect(() => {
    setVoiceOverEnabled(getVoiceOverState());
    return subscribeVoiceOver((enabled) => setVoiceOverEnabled(enabled));
  }, []);

  const handleToggleVoiceOver = () => {
    const next = !voiceOverEnabled;
    setVoiceOverState(next);
    setVoiceOverEnabled(next);
  };

  const handleTestAudio = () => {
    speakVoiceOver(
      'Voice-over audio check: Election Intelligence Platform telemetry running normally with 99.98% platform SLA. All regional feeds nominal.',
      { priority: 'high' }
    );
    setLastSpeechStatus('Audio status check announced.');
    setTimeout(() => setLastSpeechStatus(null), 4000);
  };

  const handleSimulateEtlVoice = () => {
    announceEtlStart('Maharashtra_Assembly_2026_VoterRolls.csv', '2,450,000');
    setTimeout(() => {
      speakVoiceOver('ETL Pipeline Progress: Running statutory validation on Form 20 and postal ballot tallies.');
    }, 2000);
    setTimeout(() => {
      announceEtlComplete('Maharashtra_Assembly_2026_VoterRolls.csv', '2,450,000');
    }, 4500);
    setLastSpeechStatus('ETL audio update sequence initiated.');
    setTimeout(() => setLastSpeechStatus(null), 5000);
  };

  const handleSimulateCriticalAlert = () => {
    announceCriticalAlert(
      'High latency spike detected on Redis cluster replica node 2. Traffic automatically rerouted to standby replica.',
      'critical'
    );
    setLastSpeechStatus('Critical alert broadcasted.');
    setTimeout(() => setLastSpeechStatus(null), 4000);
  };

  const filteredLogs = auditLogs.filter((log) => {
    if (filterAction === 'ALL') return true;
    return log.action.includes(filterAction);
  });

  return (
    <div className="p-6 sm:p-8 space-y-6 max-w-7xl mx-auto">
      {/* Apple Header */}
      <div>
        <h2 className="text-2xl sm:text-3xl font-bold text-[#1d1d1f] dark:text-[#f5f5f7] tracking-tight">
          Enterprise Control
        </h2>
        <p className="text-[13px] text-[#86868b] dark:text-[#a1a1a6] mt-1">
          Monitor system resources, toggle feature flags, audit security events, and manage AI model routing.
        </p>
      </div>

      {/* System Health Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard
          title="CPU Utilization"
          value={`${metrics.cpuUtilization}%`}
          subtitle="Apple Silicon Cluster • 16 Cores"
          icon={Cpu}
          iconColorClass="text-[#0071e3] dark:text-[#2997ff] bg-[#0071e3]/10 dark:bg-[#2997ff]/15"
          badgeText="Optimal"
          badgeColorClass="text-[#34c759] dark:text-[#30d158] bg-[#34c759]/10"
        />
        <MetricCard
          title="RAM Utilization"
          value={`${metrics.memoryUtilization}%`}
          subtitle="6.16 GB of 16 GB used • Heap steady"
          icon={HardDrive}
          iconColorClass="text-[#af52de] dark:text-[#bf5af2] bg-[#af52de]/10 dark:bg-[#bf5af2]/15"
          badgeText="Normal"
          badgeColorClass="text-[#34c759] dark:text-[#30d158] bg-[#34c759]/10"
        />
        <MetricCard
          title="Database Pool"
          value={`${metrics.dbPoolActive} / 15`}
          subtitle="Active connection pool • 0 overflow"
          icon={Database}
          iconColorClass="text-[#ff9500] dark:text-[#ff9f0a] bg-[#ff9500]/10 dark:bg-[#ff9f0a]/15"
          badgeText="Healthy"
          badgeColorClass="text-[#34c759] dark:text-[#30d158] bg-[#34c759]/10"
        />
        <MetricCard
          title="Cache Hit Ratio"
          value="94.6%"
          subtitle={`Redis latency ${metrics.redisLatencyMs}ms`}
          icon={Zap}
          iconColorClass="text-[#34c759] dark:text-[#30d158] bg-[#34c759]/10 dark:bg-[#30d158]/15"
          badgeText="Nominal"
          badgeColorClass="text-[#34c759] dark:text-[#30d158] bg-[#34c759]/10"
        />
      </div>

      {/* Two Column Section: Feature Flags & AI Subsystem Control */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        {/* Feature Flags Manager (macOS Settings list style) */}
        <div className="bg-white dark:bg-[#1c1c1e] border border-black/[0.06] dark:border-white/[0.08] rounded-2xl p-5 sm:p-6 shadow-[0_2px_12px_rgba(0,0,0,0.03)] dark:shadow-none transition-colors">
          <div className="flex items-center justify-between pb-4 border-b border-black/[0.04] dark:border-white/[0.04]">
            <div>
              <h3 className="text-[15px] font-semibold text-[#1d1d1f] dark:text-[#f5f5f7]">Feature Flags</h3>
              <p className="text-[12px] text-[#86868b] dark:text-[#a1a1a6] mt-0.5">
                Runtime configuration flags persisted across cluster
              </p>
            </div>
            <span className="text-[11px] font-medium text-[#34c759] dark:text-[#30d158] bg-[#34c759]/10 px-2.5 py-0.5 rounded-full">
              {featureFlags.filter((f) => f.enabled).length} Enabled
            </span>
          </div>

          <div className="divide-y divide-black/[0.03] dark:divide-white/[0.03] mt-2">
            {featureFlags.map((flag) => (
              <div
                key={flag.name}
                className="py-3 flex items-center justify-between gap-4 group"
              >
                <div className="min-w-0">
                  <div className="flex items-center gap-2">
                    <span className="font-medium text-[13px] text-[#1d1d1f] dark:text-[#f5f5f7]">
                      {flag.name}
                    </span>
                    <span className="text-[10px] uppercase font-mono px-1.5 py-0.2 rounded bg-black/[0.04] dark:bg-white/[0.06] text-[#86868b] dark:text-[#a1a1a6]">
                      {flag.environment}
                    </span>
                  </div>
                  <p className="text-[12px] text-[#86868b] dark:text-[#a1a1a6] mt-0.5 truncate">
                    {flag.description}
                  </p>
                </div>
                {/* Apple HIG iOS Toggle Switch */}
                <button
                  type="button"
                  onClick={() => onToggleFlag(flag.name)}
                  className={`w-11 h-6 rounded-full p-0.5 transition-colors relative shrink-0 cursor-pointer ${
                    flag.enabled ? 'bg-[#34c759] dark:bg-[#30d158]' : 'bg-[#e3e3e8] dark:bg-[#3a3a3c]'
                  }`}
                  aria-pressed={flag.enabled}
                  aria-label={`Toggle ${flag.name}`}
                >
                  <span
                    className={`block w-5 h-5 rounded-full bg-white shadow-md transition-transform ${
                      flag.enabled ? 'translate-x-5' : 'translate-x-0'
                    }`}
                  />
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* AI Subsystem Control Center */}
        <div className="bg-white dark:bg-[#1c1c1e] border border-black/[0.06] dark:border-white/[0.08] rounded-2xl p-5 sm:p-6 shadow-[0_2px_12px_rgba(0,0,0,0.03)] dark:shadow-none flex flex-col justify-between transition-colors">
          <div>
            <div className="flex items-center justify-between pb-4 border-b border-black/[0.04] dark:border-white/[0.04]">
              <div>
                <h3 className="text-[15px] font-semibold text-[#1d1d1f] dark:text-[#f5f5f7]">AI Model Routing</h3>
                <p className="text-[12px] text-[#86868b] dark:text-[#a1a1a6] mt-0.5">
                  Multi-provider gateway, grounding guardrails, and citation verification
                </p>
              </div>
              <span className="text-[11px] font-medium text-[#0071e3] dark:text-[#2997ff] bg-[#0071e3]/10 px-2 py-0.5 rounded-full">
                RAG Active
              </span>
            </div>

            <div className="space-y-3 mt-4">
              <div className="flex items-start gap-3 p-3 rounded-xl bg-black/[0.02] dark:bg-white/[0.03] border border-black/[0.04] dark:border-white/[0.04]">
                <div className="p-2 rounded-lg bg-[#0071e3]/10 dark:bg-[#2997ff]/15 text-[#0071e3] dark:text-[#2997ff] shrink-0">
                  <Bot className="w-4 h-4" />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <span className="text-[13px] font-semibold text-[#1d1d1f] dark:text-[#f5f5f7]">
                      Active Model
                    </span>
                    <span className="text-[11px] font-medium text-[#0071e3] dark:text-[#2997ff]">
                      Gemini 2.5 Flash
                    </span>
                  </div>
                  <p className="text-[11px] text-[#86868b] dark:text-[#a1a1a6] mt-0.5">
                    Multi-turn election intelligence with semantic RAG vector grounding.
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-3 p-3 rounded-xl bg-black/[0.02] dark:bg-white/[0.03] border border-black/[0.04] dark:border-white/[0.04]">
                <div className="p-2 rounded-lg bg-[#34c759]/10 text-[#34c759] dark:text-[#30d158] shrink-0">
                  <ShieldCheck className="w-4 h-4" />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <span className="text-[13px] font-semibold text-[#1d1d1f] dark:text-[#f5f5f7]">
                      Safety Guardrails
                    </span>
                    <CheckCircle className="w-3.5 h-3.5 text-[#34c759] dark:text-[#30d158]" />
                  </div>
                  <p className="text-[11px] text-[#86868b] dark:text-[#a1a1a6] mt-0.5">
                    Pre-LLM neutrality filters with post-generation statutory fact checking.
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-3 p-3 rounded-xl bg-black/[0.02] dark:bg-white/[0.03] border border-black/[0.04] dark:border-white/[0.04]">
                <div className="p-2 rounded-lg bg-[#ff9500]/10 text-[#ff9500] dark:text-[#ff9f0a] shrink-0">
                  <Quote className="w-4 h-4" />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <span className="text-[13px] font-semibold text-[#1d1d1f] dark:text-[#f5f5f7]">
                      Citation System
                    </span>
                    <CheckCircle className="w-3.5 h-3.5 text-[#34c759] dark:text-[#30d158]" />
                  </div>
                  <p className="text-[11px] text-[#86868b] dark:text-[#a1a1a6] mt-0.5">
                    Strict evidence citations: Form 26 affidavits and official ECI notifications.
                  </p>
                </div>
              </div>
            </div>
          </div>

          <div className="pt-4 mt-4 border-t border-black/[0.04] dark:border-white/[0.04]">
            <button
              type="button"
              onClick={onOpenModelConfig}
              className="w-full flex items-center justify-center gap-2 py-2 px-3 rounded-xl bg-black/[0.04] dark:bg-white/[0.06] hover:bg-black/[0.08] dark:hover:bg-white/[0.1] text-[#1d1d1f] dark:text-[#f5f5f7] text-[12px] font-medium transition-all cursor-pointer active:scale-95"
            >
              <Sliders className="w-3.5 h-3.5 text-[#0071e3] dark:text-[#2997ff]" />
              Configure Model Routing &amp; Hyperparameters
            </button>
          </div>
        </div>
      </div>

      {/* Voice-over & Speech Accessibility Control Card */}
      <div className="bg-white dark:bg-[#1c1c1e] border border-black/[0.06] dark:border-white/[0.08] rounded-2xl p-5 sm:p-6 shadow-[0_2px_12px_rgba(0,0,0,0.03)] dark:shadow-none transition-colors">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-black/[0.04] dark:border-white/[0.04]">
          <div className="flex items-center gap-3">
            <div className={`w-8 h-8 rounded-xl flex items-center justify-center transition-colors ${
              voiceOverEnabled ? 'bg-[#0071e3]/10 text-[#0071e3] dark:text-[#2997ff]' : 'bg-black/[0.04] dark:bg-white/[0.08] text-[#86868b]'
            }`}>
              {voiceOverEnabled ? <Volume2 className="w-4 h-4 animate-pulse" /> : <VolumeX className="w-4 h-4" />}
            </div>
            <div>
              <h3 className="text-[15px] font-semibold text-[#1d1d1f] dark:text-[#f5f5f7] flex items-center gap-2">
                Voice-over Status Updates
                <span className="text-[11px] font-medium text-[#0071e3] dark:text-[#2997ff]">
                  · Web Speech API
                </span>
              </h3>
              <p className="text-[12px] text-[#86868b] dark:text-[#a1a1a6] mt-0.5">
                Spoken audio narration for long-running ETL ingestion batches and critical system infrastructure alerts
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <span className={`text-[11px] font-medium px-2.5 py-0.5 rounded-full ${
              voiceOverEnabled
                ? 'bg-[#34c759]/10 text-[#34c759] dark:text-[#30d158]'
                : 'bg-black/[0.05] dark:bg-white/[0.08] text-[#86868b]'
            }`}>
              {voiceOverEnabled ? 'Audio Active' : 'Audio Muted'}
            </span>
            {/* Apple HIG iOS Toggle Switch */}
            <button
              type="button"
              onClick={handleToggleVoiceOver}
              className={`w-12 h-6.5 rounded-full p-0.5 transition-colors relative shrink-0 cursor-pointer ${
                voiceOverEnabled ? 'bg-[#34c759] dark:bg-[#30d158]' : 'bg-[#e3e3e8] dark:bg-[#3a3a3c]'
              }`}
              aria-label="Toggle Voice-over audio status updates"
              aria-pressed={voiceOverEnabled}
            >
              <div
                className={`w-5.5 h-5.5 rounded-full bg-white shadow-sm transform transition-transform ${
                  voiceOverEnabled ? 'translate-x-5.5' : 'translate-x-0'
                }`}
              />
            </button>
          </div>
        </div>

        {/* Feature Actions / Test Buttons */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-4">
          <button
            type="button"
            onClick={handleTestAudio}
            className="flex items-center justify-center gap-2 px-3.5 py-2.5 rounded-xl bg-black/[0.03] dark:bg-white/[0.05] hover:bg-black/[0.06] dark:hover:bg-white/[0.08] text-[#1d1d1f] dark:text-[#f5f5f7] text-[12px] font-medium transition cursor-pointer active:scale-98"
          >
            <Play className="w-3.5 h-3.5 text-[#0071e3] dark:text-[#2997ff]" />
            Test Voice-over Audio
          </button>

          <button
            type="button"
            onClick={handleSimulateEtlVoice}
            className="flex items-center justify-center gap-2 px-3.5 py-2.5 rounded-xl bg-black/[0.03] dark:bg-white/[0.05] hover:bg-black/[0.06] dark:hover:bg-white/[0.08] text-[#1d1d1f] dark:text-[#f5f5f7] text-[12px] font-medium transition cursor-pointer active:scale-98"
          >
            <Radio className="w-3.5 h-3.5 text-[#af52de]" />
            Simulate ETL Ingestion Progress
          </button>

          <button
            type="button"
            onClick={handleSimulateCriticalAlert}
            className="flex items-center justify-center gap-2 px-3.5 py-2.5 rounded-xl bg-black/[0.03] dark:bg-white/[0.05] hover:bg-black/[0.06] dark:hover:bg-white/[0.08] text-[#1d1d1f] dark:text-[#f5f5f7] text-[12px] font-medium transition cursor-pointer active:scale-98"
          >
            <AlertTriangle className="w-3.5 h-3.5 text-[#ff3b30]" />
            Simulate Critical Alert
          </button>
        </div>

        {lastSpeechStatus && (
          <div className="mt-3 pt-2.5 border-t border-black/[0.04] dark:border-white/[0.04] flex items-center gap-2 text-[11px] text-[#0071e3] dark:text-[#2997ff]">
            <span className="w-2 h-2 rounded-full bg-[#0071e3] dark:bg-[#2997ff] animate-ping" />
            <span>{lastSpeechStatus}</span>
          </div>
        )}
      </div>

      {/* Security & Audit Event Stream Table */}
      <div className="bg-white dark:bg-[#1c1c1e] border border-black/[0.06] dark:border-white/[0.08] rounded-2xl p-5 sm:p-6 shadow-[0_2px_12px_rgba(0,0,0,0.03)] dark:shadow-none transition-colors">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-black/[0.04] dark:border-white/[0.04]">
          <div>
            <h3 className="text-[15px] font-semibold text-[#1d1d1f] dark:text-[#f5f5f7]">Security &amp; Audit Event Stream</h3>
            <p className="text-[12px] text-[#86868b] dark:text-[#a1a1a6] mt-0.5">
              Immutable cryptographically chained administrative audit logs
            </p>
          </div>
          <div className="flex items-center gap-2">
            <select
              value={filterAction}
              onChange={(e) => setFilterAction(e.target.value)}
              className="text-[12px] bg-black/[0.03] dark:bg-white/[0.05] border border-black/[0.06] dark:border-white/[0.08] rounded-xl px-2.5 py-1.5 text-[#1d1d1f] dark:text-[#f5f5f7] focus:outline-none focus:ring-2 focus:ring-[#0071e3]/30"
            >
              <option value="ALL">All Actions</option>
              <option value="UPDATE">Update Flags</option>
              <option value="INGEST">Ingest Data</option>
              <option value="ROTATE">Rotate Keys</option>
              <option value="DECLARE">Declare Results</option>
            </select>
            <button
              type="button"
              onClick={() => exportAuditLogsPDF(auditLogs)}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-[#0071e3]/10 dark:bg-[#2997ff]/15 hover:bg-[#0071e3]/20 text-[#0071e3] dark:text-[#2997ff] text-[12px] font-medium transition-all cursor-pointer active:scale-95"
            >
              <FileText className="w-3.5 h-3.5" />
              Export PDF
            </button>
            <button
              type="button"
              onClick={() => exportAuditLogsCSV(auditLogs)}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-black/[0.04] dark:bg-white/[0.06] hover:bg-black/[0.08] dark:hover:bg-white/[0.1] text-[#1d1d1f] dark:text-[#f5f5f7] text-[12px] font-medium transition-all cursor-pointer active:scale-95"
            >
              <Download className="w-3.5 h-3.5" />
              Export CSV
            </button>
          </div>
        </div>

        <div className="overflow-x-auto mt-3">
          <table className="w-full text-left">
            <thead className="text-[11px] uppercase tracking-wider text-[#86868b] dark:text-[#a1a1a6] border-b border-black/[0.04] dark:border-white/[0.04]">
              <tr>
                <th className="py-2.5 px-3 font-semibold">Timestamp</th>
                <th className="py-2.5 px-3 font-semibold">Actor</th>
                <th className="py-2.5 px-3 font-semibold">Action</th>
                <th className="py-2.5 px-3 font-semibold">Resource</th>
                <th className="py-2.5 px-3 font-semibold">IP Address</th>
                <th className="py-2.5 px-3 font-semibold">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-black/[0.03] dark:divide-white/[0.03] text-[12px]">
              {filteredLogs.map((log) => (
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
                  <td className="py-3 px-3 text-[#86868b] dark:text-[#a1a1a6] font-mono whitespace-nowrap">
                    {log.ipAddress}
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

      {/* User Accounts & IAM */}
      <div className="bg-white dark:bg-[#1c1c1e] border border-black/[0.06] dark:border-white/[0.08] rounded-2xl p-5 sm:p-6 shadow-[0_2px_12px_rgba(0,0,0,0.03)] dark:shadow-none transition-colors">
        <div className="flex items-center justify-between pb-4 border-b border-black/[0.04] dark:border-white/[0.04]">
          <div>
            <h3 className="text-[15px] font-semibold text-[#1d1d1f] dark:text-[#f5f5f7] flex items-center gap-2">
              <Users className="w-4 h-4 text-[#0071e3] dark:text-[#2997ff]" />
              Administrative User Accounts
            </h3>
            <p className="text-[12px] text-[#86868b] dark:text-[#a1a1a6] mt-0.5">
              Role-based access privileges with enforced Multi-Factor Authentication
            </p>
          </div>
          <span className="text-[11px] font-medium text-[#86868b] dark:text-[#a1a1a6]">
            {userAccounts.length} Active Operators
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3 mt-4">
          {userAccounts.map((user) => (
            <div
              key={user.id}
              className="p-3.5 rounded-xl bg-black/[0.02] dark:bg-white/[0.03] border border-black/[0.04] dark:border-white/[0.04] flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center justify-between mb-2">
                  <div className="w-7 h-7 rounded-full bg-[#0071e3]/10 dark:bg-[#2997ff]/20 text-[#0071e3] dark:text-[#2997ff] flex items-center justify-center font-bold text-[11px]">
                    {user.username.slice(0, 2).toUpperCase()}
                  </div>
                  <span className="text-[10px] font-medium text-[#34c759] dark:text-[#30d158] bg-[#34c759]/10 px-1.5 py-0.5 rounded-full">
                    MFA
                  </span>
                </div>
                <div className="font-semibold text-[13px] text-[#1d1d1f] dark:text-[#f5f5f7]">{user.username}</div>
                <div className="text-[11px] text-[#0071e3] dark:text-[#2997ff] font-medium">{user.role}</div>
                <div className="text-[11px] text-[#86868b] dark:text-[#a1a1a6] mt-0.5 truncate">{user.email}</div>
              </div>
              <div className="mt-3 pt-2 border-t border-black/[0.04] dark:border-white/[0.04] text-[10px] text-[#86868b] dark:text-[#a1a1a6]">
                Last Login: {user.lastLogin.split('T')[0]}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

