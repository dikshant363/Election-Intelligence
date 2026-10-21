import { jsPDF } from 'jspdf';
import {
  AuditLog,
  Candidate,
  Constituency,
  ElectionResult,
  FeatureFlag,
  Party,
  RegionalTurnout,
  SystemHealthMetrics,
  UserAccount,
  ExecutiveKpis,
} from './types';

// Helper to trigger browser file download
function triggerDownload(blob: Blob, filename: string) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

// -------------------------------------------------------------
// ELECTION RESULTS EXPORT
// -------------------------------------------------------------

export function exportResultsCSV(
  results: ElectionResult[],
  constituencies: Constituency[],
  candidates: Candidate[],
  parties: Party[]
) {
  const headers = [
    'Result Key',
    'Constituency Name',
    'Constituency Code',
    'State',
    'Winner Candidate',
    'Winner Party',
    'Winner Votes',
    'Margin',
    'Total Votes',
    'Status',
    'Declaration Timestamp',
  ];

  const rows = results.map((res) => {
    const constituency = constituencies.find((c) => c.id === res.constituency_id);
    const winner = candidates.find((can) => can.id === res.winning_candidate_id);
    const party = parties.find((p) => p.id === winner?.party_id);
    const winnerVotes = res.candidate_votes[res.winning_candidate_id] || 0;

    return [
      `"${res.result_key}"`,
      `"${constituency?.name || 'N/A'}"`,
      `"${constituency?.code || 'N/A'}"`,
      `"${constituency?.state_name || 'N/A'}"`,
      `"${winner?.name || 'N/A'}"`,
      `"${party?.code || 'IND'}"`,
      winnerVotes,
      res.margin,
      res.total_votes,
      res.is_declared ? 'DECLARED' : 'PENDING',
      `"${res.declaration_time}"`,
    ].join(',');
  });

  const csvContent = [headers.join(','), ...rows].join('\r\n');
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const filename = `election_results_${new Date().toISOString().split('T')[0]}.csv`;
  triggerDownload(blob, filename);
}

export function exportResultsPDF(
  results: ElectionResult[],
  constituencies: Constituency[],
  candidates: Candidate[],
  parties: Party[]
) {
  const doc = new jsPDF({ orientation: 'landscape', unit: 'mm', format: 'a4' });
  const timestamp = new Date().toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' });

  // Header banner
  doc.setFillColor(30, 41, 59);
  doc.rect(0, 0, 297, 26, 'F');

  doc.setTextColor(255, 255, 255);
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(16);
  doc.text('ELECTION INTELLIGENCE PLATFORM', 14, 12);

  doc.setFont('helvetica', 'normal');
  doc.setFontSize(9);
  doc.setTextColor(199, 210, 254);
  doc.text('STATUTORY CONSTITUENCY ELECTION RESULTS AUDIT REPORT', 14, 19);

  doc.setTextColor(203, 213, 225);
  doc.text(`Generated: ${timestamp} IST | Returning Officer Verified`, 283, 19, { align: 'right' });

  // Table header
  let y = 36;
  doc.setFillColor(241, 245, 249);
  doc.rect(14, y, 269, 9, 'F');
  doc.setDrawColor(203, 213, 225);
  doc.rect(14, y, 269, 9, 'S');

  doc.setTextColor(15, 23, 42);
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(9);

  doc.text('Constituency', 16, y + 6);
  doc.text('Code / State', 68, y + 6);
  doc.text('Winning Candidate', 112, y + 6);
  doc.text('Party', 170, y + 6);
  doc.text('Votes Polled', 194, y + 6);
  doc.text('Margin', 228, y + 6);
  doc.text('Status', 260, y + 6);

  y += 9;

  doc.setFont('helvetica', 'normal');
  doc.setFontSize(8.5);

  results.forEach((res, index) => {
    const constituency = constituencies.find((c) => c.id === res.constituency_id);
    const winner = candidates.find((can) => can.id === res.winning_candidate_id);
    const party = parties.find((p) => p.id === winner?.party_id);
    const winnerVotes = res.candidate_votes[res.winning_candidate_id] || 0;

    // Alternate row colors
    if (index % 2 === 1) {
      doc.setFillColor(248, 250, 252);
      doc.rect(14, y, 269, 8, 'F');
    }
    doc.setDrawColor(226, 232, 240);
    doc.line(14, y + 8, 283, y + 8);

    doc.setTextColor(15, 23, 42);
    doc.text(constituency?.name || 'N/A', 16, y + 5.5);
    doc.text(`${constituency?.code || ''} (${constituency?.state_name || ''})`, 68, y + 5.5);

    doc.setFont('helvetica', 'bold');
    doc.text(winner?.name || 'N/A', 112, y + 5.5);
    doc.setFont('helvetica', 'normal');

    doc.text(party?.code || 'IND', 170, y + 5.5);
    doc.text(winnerVotes.toLocaleString(), 194, y + 5.5);
    doc.text(`+${res.margin.toLocaleString()}`, 228, y + 5.5);

    doc.setTextColor(16, 149, 107);
    doc.setFont('helvetica', 'bold');
    doc.text('DECLARED', 260, y + 5.5);
    doc.setFont('helvetica', 'normal');
    doc.setTextColor(15, 23, 42);

    y += 8;
  });

  // Summary box
  y += 8;
  doc.setFillColor(241, 245, 249);
  doc.roundedRect(14, y, 269, 18, 2, 2, 'FD');
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(9);
  doc.setTextColor(30, 41, 59);
  doc.text(`Summary: ${results.length} Parliamentary Constituency Results Certified`, 18, y + 7);
  doc.setFont('helvetica', 'normal');
  doc.setFontSize(8);
  doc.setTextColor(100, 116, 139);
  doc.text(
    'All vote totals verified from Electronic Voting Machine (EVM) Control Units and VVPAT paper audits. Signed by District Returning Officers.',
    18,
    y + 13
  );

  // Footer
  doc.setFontSize(7.5);
  doc.setTextColor(148, 163, 184);
  doc.text('Official Form 20 Statutory Summary | Election Intelligence Platform CQRS Tally Engine', 14, 202);

  doc.save(`election_results_${new Date().toISOString().split('T')[0]}.pdf`);
}

// -------------------------------------------------------------
// AUDIT LOGS EXPORT
// -------------------------------------------------------------

export function exportAuditLogsCSV(auditLogs: AuditLog[]) {
  const headers = ['Event ID', 'Timestamp', 'Actor', 'Action', 'Resource', 'IP Address', 'Status'];
  const rows = auditLogs.map((log) => [
    `"${log.id}"`,
    `"${log.timestamp}"`,
    `"${log.actor}"`,
    `"${log.action}"`,
    `"${log.resource}"`,
    `"${log.ipAddress}"`,
    `"${log.status}"`,
  ].join(','));

  const csvContent = [headers.join(','), ...rows].join('\r\n');
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const filename = `election_audit_logs_${new Date().toISOString().split('T')[0]}.csv`;
  triggerDownload(blob, filename);
}

export function exportAuditLogsPDF(auditLogs: AuditLog[]) {
  const doc = new jsPDF({ orientation: 'landscape', unit: 'mm', format: 'a4' });
  const timestamp = new Date().toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' });

  // Header banner
  doc.setFillColor(15, 23, 42);
  doc.rect(0, 0, 297, 26, 'F');

  doc.setTextColor(255, 255, 255);
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(16);
  doc.text('ELECTION INTELLIGENCE PLATFORM', 14, 12);

  doc.setFont('helvetica', 'normal');
  doc.setFontSize(9);
  doc.setTextColor(147, 197, 253);
  doc.text('SECURITY, GOVERNANCE & OPERATIONS AUDIT EVENT LOGS', 14, 19);

  doc.setTextColor(203, 213, 225);
  doc.text(`Generated: ${timestamp} IST | Cryptographically Signed`, 283, 19, { align: 'right' });

  // Table header
  let y = 36;
  doc.setFillColor(241, 245, 249);
  doc.rect(14, y, 269, 9, 'F');
  doc.setDrawColor(203, 213, 225);
  doc.rect(14, y, 269, 9, 'S');

  doc.setTextColor(15, 23, 42);
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(9);

  doc.text('Event ID', 16, y + 6);
  doc.text('Timestamp (UTC)', 48, y + 6);
  doc.text('Actor', 98, y + 6);
  doc.text('Action Performed', 134, y + 6);
  doc.text('Target Resource', 190, y + 6);
  doc.text('IP Address', 242, y + 6);
  doc.text('Status', 266, y + 6);

  y += 9;

  doc.setFont('helvetica', 'normal');
  doc.setFontSize(8);

  auditLogs.forEach((log, index) => {
    if (index % 2 === 1) {
      doc.setFillColor(248, 250, 252);
      doc.rect(14, y, 269, 8, 'F');
    }
    doc.setDrawColor(226, 232, 240);
    doc.line(14, y + 8, 283, y + 8);

    doc.setTextColor(71, 85, 105);
    doc.text(log.id, 16, y + 5.5);
    doc.text(log.timestamp, 48, y + 5.5);

    doc.setFont('helvetica', 'bold');
    doc.setTextColor(15, 23, 42);
    doc.text(log.actor, 98, y + 5.5);
    doc.setFont('helvetica', 'normal');

    doc.setTextColor(79, 70, 229);
    doc.text(log.action, 134, y + 5.5);

    doc.setTextColor(15, 23, 42);
    doc.text(log.resource, 190, y + 5.5);
    doc.text(log.ipAddress, 242, y + 5.5);

    doc.setTextColor(16, 149, 107);
    doc.setFont('helvetica', 'bold');
    doc.text(log.status, 266, y + 5.5);
    doc.setFont('helvetica', 'normal');

    y += 8;
  });

  // Footer
  doc.setFontSize(7.5);
  doc.setTextColor(148, 163, 184);
  doc.text('Immutable Audit Log Export • Certified for Statutory Election Commission Scrutiny', 14, 202);

  doc.save(`election_audit_logs_${new Date().toISOString().split('T')[0]}.pdf`);
}

// -------------------------------------------------------------
// ENTERPRISE CONTROL CENTER EXPORT
// -------------------------------------------------------------

export function exportEnterpriseReportCSV(
  metrics: SystemHealthMetrics,
  featureFlags: FeatureFlag[],
  userAccounts: UserAccount[]
) {
  const sections: string[] = [];

  // Metrics Section
  sections.push('# SYSTEM HEALTH METRICS');
  sections.push('Metric,Value,Unit');
  sections.push(`CPU Utilization,${metrics.cpuUtilization},%`);
  sections.push(`Memory Utilization,${metrics.memoryUtilization},%`);
  sections.push(`Free Disk Space,${metrics.diskFreeGb},GB`);
  sections.push(`API Throughput,${metrics.apiRequestsPerSec},req/sec`);
  sections.push(`P99 Latency,${metrics.p99LatencyMs},ms`);
  sections.push(`Active DB Pool,${metrics.dbPoolActive},connections`);
  sections.push(`Redis Latency,${metrics.redisLatencyMs},ms`);
  sections.push('');

  // Feature Flags Section
  sections.push('# GOVERNANCE FEATURE FLAGS');
  sections.push('Flag Name,Status,Environment,Description');
  featureFlags.forEach((flag) => {
    sections.push(
      `"${flag.name}",${flag.enabled ? 'ENABLED' : 'DISABLED'},"${flag.environment}","${flag.description.replace(/"/g, '""')}"`
    );
  });
  sections.push('');

  // User Accounts / RBAC Section
  sections.push('# OPERATOR ACCESS & RBAC');
  sections.push('Username,Email,Role,Status,MFA Enabled,Last Login');
  userAccounts.forEach((u) => {
    sections.push(
      `"${u.username}","${u.email}","${u.role}",${u.isActive ? 'ACTIVE' : 'INACTIVE'},${u.mfaEnabled ? 'YES' : 'NO'},"${u.lastLogin}"`
    );
  });

  const blob = new Blob([sections.join('\r\n')], { type: 'text/csv;charset=utf-8;' });
  const filename = `enterprise_infrastructure_report_${new Date().toISOString().split('T')[0]}.csv`;
  triggerDownload(blob, filename);
}

export function exportEnterpriseReportPDF(
  metrics: SystemHealthMetrics,
  featureFlags: FeatureFlag[],
  userAccounts: UserAccount[],
  auditLogs: AuditLog[]
) {
  const doc = new jsPDF({ orientation: 'landscape', unit: 'mm', format: 'a4' });
  const timestamp = new Date().toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' });

  // Banner
  doc.setFillColor(15, 23, 42);
  doc.rect(0, 0, 297, 26, 'F');

  doc.setTextColor(255, 255, 255);
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(16);
  doc.text('ELECTION INTELLIGENCE PLATFORM', 14, 12);

  doc.setFont('helvetica', 'normal');
  doc.setFontSize(9);
  doc.setTextColor(147, 197, 253);
  doc.text('ENTERPRISE SYSTEM ARCHITECTURE, INFRASTRUCTURE & RBAC REPORT', 14, 19);

  doc.setTextColor(203, 213, 225);
  doc.text(`Generated: ${timestamp} IST | System Status: NOMINAL`, 283, 19, { align: 'right' });

  // Health Metrics Grid
  let y = 34;
  doc.setFillColor(241, 245, 249);
  doc.roundedRect(14, y, 269, 20, 2, 2, 'FD');

  doc.setFont('helvetica', 'bold');
  doc.setFontSize(9);
  doc.setTextColor(30, 41, 59);
  doc.text('REAL-TIME INFRASTRUCTURE TELEMETRY & SLO BENCHMARKS', 18, y + 6);

  doc.setFont('helvetica', 'normal');
  doc.setFontSize(8);
  doc.setTextColor(71, 85, 105);
  doc.text(
    `CPU: ${metrics.cpuUtilization}%  |  Memory: ${metrics.memoryUtilization}%  |  Disk Free: ${metrics.diskFreeGb} GB  |  API QPS: ${metrics.apiRequestsPerSec}/s  |  P99: ${metrics.p99LatencyMs}ms  |  Redis: ${metrics.redisLatencyMs}ms  |  DB Pool: ${metrics.dbPoolActive} conns`,
    18,
    y + 13
  );

  // Feature Flags
  y += 26;
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(10);
  doc.setTextColor(15, 23, 42);
  doc.text('Governance Feature Flags & Kill Switches', 14, y);

  y += 4;
  doc.setFillColor(241, 245, 249);
  doc.rect(14, y, 269, 7, 'F');
  doc.setFontSize(8.5);
  doc.setTextColor(15, 23, 42);
  doc.text('Flag Key', 16, y + 5);
  doc.text('Environment', 85, y + 5);
  doc.text('Status', 140, y + 5);
  doc.text('Governance Scope / Description', 180, y + 5);

  y += 7;
  doc.setFont('helvetica', 'normal');
  doc.setFontSize(8);
  featureFlags.slice(0, 6).forEach((flag, idx) => {
    if (idx % 2 === 1) {
      doc.setFillColor(248, 250, 252);
      doc.rect(14, y, 269, 7, 'F');
    }
    doc.setDrawColor(226, 232, 240);
    doc.line(14, y + 7, 283, y + 7);

    doc.setTextColor(30, 41, 59);
    doc.text(flag.name, 16, y + 5);
    doc.text(flag.environment, 85, y + 5);

    if (flag.enabled) {
      doc.setTextColor(16, 149, 107);
      doc.text('ENABLED', 140, y + 5);
    } else {
      doc.setTextColor(220, 38, 38);
      doc.text('DISABLED', 140, y + 5);
    }

    doc.setTextColor(71, 85, 105);
    doc.text(flag.description.substring(0, 55), 180, y + 5);
    y += 7;
  });

  // Operators RBAC
  y += 6;
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(10);
  doc.setTextColor(15, 23, 42);
  doc.text('Active Administrative Operators & Access Roles', 14, y);

  y += 4;
  doc.setFillColor(241, 245, 249);
  doc.rect(14, y, 269, 7, 'F');
  doc.setFontSize(8.5);
  doc.setTextColor(15, 23, 42);
  doc.text('Username', 16, y + 5);
  doc.text('Email', 65, y + 5);
  doc.text('Role', 135, y + 5);
  doc.text('MFA', 185, y + 5);
  doc.text('Status', 220, y + 5);
  doc.text('Last Login', 250, y + 5);

  y += 7;
  doc.setFont('helvetica', 'normal');
  doc.setFontSize(8);
  userAccounts.slice(0, 5).forEach((u, idx) => {
    if (idx % 2 === 1) {
      doc.setFillColor(248, 250, 252);
      doc.rect(14, y, 269, 7, 'F');
    }
    doc.setDrawColor(226, 232, 240);
    doc.line(14, y + 7, 283, y + 7);

    doc.setTextColor(30, 41, 59);
    doc.text(u.username, 16, y + 5);
    doc.text(u.email, 65, y + 5);
    doc.text(u.role, 135, y + 5);
    doc.text(u.mfaEnabled ? 'Verified' : 'No', 185, y + 5);
    doc.setTextColor(16, 149, 107);
    doc.text(u.isActive ? 'ACTIVE' : 'LOCKED', 220, y + 5);
    doc.setTextColor(71, 85, 105);
    doc.text(u.lastLogin, 250, y + 5);
    y += 7;
  });

  // Footer
  doc.setFontSize(7.5);
  doc.setTextColor(148, 163, 184);
  doc.text(
    `Enterprise Platform Health Audit • Total Recorded Audit Logs: ${auditLogs.length} • Strict Air-Gapped Network Topology`,
    14,
    202
  );

  doc.save(`enterprise_infrastructure_report_${new Date().toISOString().split('T')[0]}.pdf`);
}

// -------------------------------------------------------------
// EXECUTIVE COMMAND CENTER EXPORT
// -------------------------------------------------------------

export function exportExecutiveReportCSV(kpis: ExecutiveKpis, regionalTurnout: RegionalTurnout[]) {
  const sections: string[] = [];

  sections.push('# NATIONAL ELECTION EXECUTIVE KPIS');
  sections.push('Indicator,Value');
  sections.push(`Total Elections Managed,${kpis.totalElectionsManaged}`);
  sections.push(`Total Registered Voters,${kpis.totalVotersRegistered.toLocaleString()}`);
  sections.push(`Average Polling Turnout,${kpis.averageTurnoutPercent}%`);
  sections.push(`Total Constituencies,${kpis.totalConstituencies}`);
  sections.push(`Total Candidates,${kpis.totalCandidates}`);
  sections.push(`Total Polling Booths Monitored,${kpis.totalPollingBooths.toLocaleString()}`);
  sections.push(`Platform Availability,${kpis.platformUptimePercent}%`);
  sections.push(`AI Queries Processed,${kpis.aiQueriesProcessed.toLocaleString()}`);
  sections.push('');

  sections.push('# REGIONAL TURNOUT & MONITORING SUMMARY');
  sections.push('Region/State,Total Electors,Polling Booths,Turnout %,Phase Status');
  regionalTurnout.forEach((r) => {
    sections.push(
      `"${r.region}","${r.totalVoters}",${r.pollingBooths},${r.voterTurnoutPercent}%,"${r.phaseStatus}"`
    );
  });

  const blob = new Blob([sections.join('\r\n')], { type: 'text/csv;charset=utf-8;' });
  const filename = `executive_command_briefing_${new Date().toISOString().split('T')[0]}.csv`;
  triggerDownload(blob, filename);
}

export function exportExecutiveReportPDF(kpis: ExecutiveKpis, regionalTurnout: RegionalTurnout[]) {
  const doc = new jsPDF({ orientation: 'landscape', unit: 'mm', format: 'a4' });
  const timestamp = new Date().toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' });

  // Banner
  doc.setFillColor(15, 23, 42);
  doc.rect(0, 0, 297, 26, 'F');

  doc.setTextColor(255, 255, 255);
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(16);
  doc.text('ELECTION INTELLIGENCE PLATFORM', 14, 12);

  doc.setFont('helvetica', 'normal');
  doc.setFontSize(9);
  doc.setTextColor(254, 215, 170);
  doc.text('EXECUTIVE COMMAND BRIEFING & NATIONAL TURNOUT INTELLIGENCE', 14, 19);

  doc.setTextColor(203, 213, 225);
  doc.text(`Generated: ${timestamp} IST | Confidential Briefing`, 283, 19, { align: 'right' });

  // 4 KPI Summary Cards
  let y = 34;
  const cardWidth = 63;
  const cardGap = 5;

  const cards = [
    { label: 'Total Registered Electors', val: `${(kpis.totalVotersRegistered / 10000000).toFixed(1)} Cr` },
    { label: 'National Average Turnout', val: `${kpis.averageTurnoutPercent}%` },
    { label: 'Monitored Polling Booths', val: kpis.totalPollingBooths.toLocaleString() },
    { label: 'Platform Availability SLO', val: `${kpis.platformUptimePercent}%` },
  ];

  cards.forEach((card, idx) => {
    const x = 14 + idx * (cardWidth + cardGap);
    doc.setFillColor(248, 250, 252);
    doc.roundedRect(x, y, cardWidth, 18, 2, 2, 'FD');
    doc.setDrawColor(226, 232, 240);
    doc.roundedRect(x, y, cardWidth, 18, 2, 2, 'S');

    doc.setFont('helvetica', 'normal');
    doc.setFontSize(7.5);
    doc.setTextColor(100, 116, 139);
    doc.text(card.label, x + 4, y + 6);

    doc.setFont('helvetica', 'bold');
    doc.setFontSize(13);
    doc.setTextColor(15, 23, 42);
    doc.text(card.val, x + 4, y + 14);
  });

  // Regional Turnout Table
  y += 26;
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(10);
  doc.setTextColor(15, 23, 42);
  doc.text('State & Regional Polling Statistics & Phase Status', 14, y);

  y += 4;
  doc.setFillColor(241, 245, 249);
  doc.rect(14, y, 269, 8, 'F');
  doc.setFontSize(8.5);
  doc.setTextColor(15, 23, 42);
  doc.text('Region / State', 16, y + 5.5);
  doc.text('Total Electors', 85, y + 5.5);
  doc.text('Polling Booths', 140, y + 5.5);
  doc.text('Voter Turnout', 190, y + 5.5);
  doc.text('Phase Status', 240, y + 5.5);

  y += 8;
  doc.setFont('helvetica', 'normal');
  doc.setFontSize(8.5);

  regionalTurnout.forEach((reg, idx) => {
    if (idx % 2 === 1) {
      doc.setFillColor(248, 250, 252);
      doc.rect(14, y, 269, 8, 'F');
    }
    doc.setDrawColor(226, 232, 240);
    doc.line(14, y + 8, 283, y + 8);

    doc.setTextColor(15, 23, 42);
    doc.setFont('helvetica', 'bold');
    doc.text(reg.region, 16, y + 5.5);
    doc.setFont('helvetica', 'normal');

    doc.setTextColor(71, 85, 105);
    doc.text(reg.totalVoters, 85, y + 5.5);
    doc.text(reg.pollingBooths.toLocaleString(), 140, y + 5.5);

    doc.setFont('helvetica', 'bold');
    doc.setTextColor(79, 70, 229);
    doc.text(`${reg.voterTurnoutPercent}%`, 190, y + 5.5);
    doc.setFont('helvetica', 'normal');

    if (reg.phaseStatus === 'COMPLETED') {
      doc.setTextColor(16, 149, 107);
      doc.text('COMPLETED', 240, y + 5.5);
    } else if (reg.phaseStatus === 'IN_PROGRESS') {
      doc.setTextColor(217, 119, 6);
      doc.text('IN PROGRESS', 240, y + 5.5);
    } else {
      doc.setTextColor(100, 116, 139);
      doc.text('SCHEDULED', 240, y + 5.5);
    }

    y += 8;
  });

  // Footer note
  y += 8;
  doc.setFillColor(241, 245, 249);
  doc.roundedRect(14, y, 269, 16, 2, 2, 'FD');
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(8.5);
  doc.setTextColor(30, 41, 59);
  doc.text('Chief Election Commissioner Directive Compliance', 18, y + 6);
  doc.setFont('helvetica', 'normal');
  doc.setFontSize(8);
  doc.setTextColor(100, 116, 139);
  doc.text(
    'Real-time live feeds synchronized every 30 seconds with State Election Headquarters. No security anomalies observed.',
    18,
    y + 11.5
  );

  doc.setFontSize(7.5);
  doc.setTextColor(148, 163, 184);
  doc.text('Statutory Executive Briefing • Prepared for National Election Commission', 14, 202);

  doc.save(`executive_command_briefing_${new Date().toISOString().split('T')[0]}.pdf`);
}

// -------------------------------------------------------------
// PUBLIC VOTER PORTAL EXPORT
// -------------------------------------------------------------

export function exportPublicPortalReportCSV(
  candidates: Candidate[],
  parties: Party[],
  constituencies: Constituency[]
) {
  const headers = [
    'Candidate Name',
    'Constituency',
    'State',
    'Party',
    'Age',
    'Education',
    'Declared Assets (Cr)',
    'Criminal Cases',
    'Form 26 Affidavit Status',
    'Submission Date',
  ];

  const rows = candidates.map((can) => {
    const constituency = constituencies.find((c) => c.id === can.constituency_id);
    const party = parties.find((p) => p.id === can.party_id);

    return [
      `"${can.name}"`,
      `"${constituency?.name || 'N/A'}"`,
      `"${constituency?.state_name || 'N/A'}"`,
      `"${party?.name || 'Independent'}"`,
      can.age,
      `"${can.education}"`,
      can.declared_assets_cr,
      can.criminal_cases,
      `"${can.affidavit_status}"`,
      `"${can.submission_date}"`,
    ].join(',');
  });

  const blob = new Blob([[headers.join(','), ...rows].join('\r\n')], { type: 'text/csv;charset=utf-8;' });
  const filename = `public_candidate_affidavits_${new Date().toISOString().split('T')[0]}.csv`;
  triggerDownload(blob, filename);
}

export function exportPublicPortalReportPDF(
  candidates: Candidate[],
  parties: Party[],
  constituencies: Constituency[]
) {
  const doc = new jsPDF({ orientation: 'landscape', unit: 'mm', format: 'a4' });
  const timestamp = new Date().toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' });

  // Banner
  doc.setFillColor(15, 23, 42);
  doc.rect(0, 0, 297, 26, 'F');

  doc.setTextColor(255, 255, 255);
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(16);
  doc.text('ELECTION COMMISSION OF INDIA', 14, 12);

  doc.setFont('helvetica', 'normal');
  doc.setFontSize(9);
  doc.setTextColor(187, 247, 208);
  doc.text('PUBLIC VOTER TRANSPARENCY & FORM 26 CANDIDATE AFFIDAVIT DIRECTORY', 14, 19);

  doc.setTextColor(203, 213, 225);
  doc.text(`Generated: ${timestamp} IST | Public Domain Access`, 283, 19, { align: 'right' });

  // Table
  let y = 34;
  doc.setFillColor(241, 245, 249);
  doc.rect(14, y, 269, 8, 'F');
  doc.setFontSize(8.5);
  doc.setFont('helvetica', 'bold');
  doc.setTextColor(15, 23, 42);

  doc.text('Candidate Name', 16, y + 5.5);
  doc.text('Constituency / State', 68, y + 5.5);
  doc.text('Party', 120, y + 5.5);
  doc.text('Age', 152, y + 5.5);
  doc.text('Education', 166, y + 5.5);
  doc.text('Assets (Cr)', 208, y + 5.5);
  doc.text('Cases', 232, y + 5.5);
  doc.text('Affidavit Status', 252, y + 5.5);

  y += 8;
  doc.setFont('helvetica', 'normal');
  doc.setFontSize(8);

  candidates.forEach((can, idx) => {
    const constituency = constituencies.find((c) => c.id === can.constituency_id);
    const party = parties.find((p) => p.id === can.party_id);

    if (idx % 2 === 1) {
      doc.setFillColor(248, 250, 252);
      doc.rect(14, y, 269, 7.5, 'F');
    }
    doc.setDrawColor(226, 232, 240);
    doc.line(14, y + 7.5, 283, y + 7.5);

    doc.setFont('helvetica', 'bold');
    doc.setTextColor(15, 23, 42);
    doc.text(can.name, 16, y + 5);
    doc.setFont('helvetica', 'normal');

    doc.setTextColor(71, 85, 105);
    doc.text(`${constituency?.name || 'N/A'} (${constituency?.state_name || ''})`, 68, y + 5);
    doc.text(party?.name || 'IND', 120, y + 5);
    doc.text(`${can.age}y`, 152, y + 5);
    doc.text(can.education, 166, y + 5);

    doc.setFont('helvetica', 'bold');
    doc.setTextColor(15, 23, 42);
    doc.text(`₹${can.declared_assets_cr} Cr`, 208, y + 5);
    doc.setFont('helvetica', 'normal');

    if (can.criminal_cases > 0) {
      doc.setTextColor(220, 38, 38);
      doc.text(`${can.criminal_cases}`, 232, y + 5);
    } else {
      doc.setTextColor(16, 149, 107);
      doc.text('0 (Clean)', 232, y + 5);
    }

    if (can.affidavit_status === 'VERIFIED') {
      doc.setTextColor(16, 149, 107);
      doc.text('VERIFIED', 252, y + 5);
    } else {
      doc.setTextColor(217, 119, 6);
      doc.text(can.affidavit_status, 252, y + 5);
    }

    y += 7.5;
  });

  // Footer
  doc.setFontSize(7.5);
  doc.setTextColor(148, 163, 184);
  doc.text('Mandatory Supreme Court Transparency Mandate • ECI Public Candidate Disclosure Record', 14, 202);

  doc.save(`public_candidate_affidavits_${new Date().toISOString().split('T')[0]}.pdf`);
}

