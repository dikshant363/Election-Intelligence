'use client';

import React from 'react';
import {
  Vote,
  Users,
  TrendingUp,
  Award,
  MapPin,
  CheckCircle2,
  Layers,
} from 'lucide-react';
import { MetricCard } from './MetricCard';
import { VoterTurnoutTrendsChart } from './VoterTurnoutTrendsChart';
import { ExecutiveKpis, RegionalTurnout } from '@/lib/types';

interface ExecutiveCommandCenterViewProps {
  kpis: ExecutiveKpis;
  regionalTurnout: RegionalTurnout[];
}

export function ExecutiveCommandCenterView({
  kpis,
  regionalTurnout,
}: ExecutiveCommandCenterViewProps) {
  return (
    <div className="p-6 sm:p-8 space-y-6 max-w-7xl mx-auto">
      {/* Apple Header */}
      <div>
        <h2 className="text-2xl sm:text-3xl font-bold text-[#1d1d1f] dark:text-[#f5f5f7] tracking-tight">
          Executive Command Center
        </h2>
        <p className="text-[13px] text-[#86868b] dark:text-[#a1a1a6] mt-1">
          High-level strategic intelligence, national turnout metrics, regional insights, and platform SLAs.
        </p>
      </div>

      {/* Strategic KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard
          title="Elections Managed"
          value={`${kpis.totalElectionsManaged}`}
          subtitle="Lok Sabha & State Assemblies"
          icon={Vote}
          iconColorClass="text-[#0071e3] dark:text-[#2997ff] bg-[#0071e3]/10 dark:bg-[#2997ff]/15"
          badgeText="Active"
          badgeColorClass="text-[#0071e3] dark:text-[#2997ff] bg-[#0071e3]/10"
        />
        <MetricCard
          title="Registered Voters"
          value="968.8M"
          subtitle="National Electoral Roll"
          icon={Users}
          iconColorClass="text-[#34c759] dark:text-[#30d158] bg-[#34c759]/10 dark:bg-[#30d158]/15"
          badgeText="+2.4%"
          badgeColorClass="text-[#34c759] dark:text-[#30d158] bg-[#34c759]/10"
        />
        <MetricCard
          title="Average Voter Turnout"
          value={`${kpis.averageTurnoutPercent}%`}
          subtitle="National Average Turnout"
          icon={TrendingUp}
          iconColorClass="text-[#ff9500] dark:text-[#ff9f0a] bg-[#ff9500]/10 dark:bg-[#ff9f0a]/15"
          badgeText="Record High"
          badgeColorClass="text-[#ff9500] dark:text-[#ff9f0a] bg-[#ff9500]/10"
        />
        <MetricCard
          title="Platform Uptime SLA"
          value={`${kpis.platformUptimePercent}%`}
          subtitle="Zero downtime past 90 days"
          icon={Award}
          iconColorClass="text-[#af52de] dark:text-[#bf5af2] bg-[#af52de]/10 dark:bg-[#bf5af2]/15"
          badgeText="99.98% SLO"
          badgeColorClass="text-[#34c759] dark:text-[#30d158] bg-[#34c759]/10"
        />
      </div>

      {/* Historical Voter Turnout Trends (Recharts Line Chart with Date Range Filter) */}
      <VoterTurnoutTrendsChart />

      {/* Regional Insights & National Turnout Visualizations */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
        {/* Regional Turnout Table */}
        <div className="lg:col-span-2 bg-white dark:bg-[#1c1c1e] border border-black/[0.06] dark:border-white/[0.08] rounded-2xl p-5 sm:p-6 shadow-[0_2px_12px_rgba(0,0,0,0.03)] dark:shadow-none transition-colors">
          <div className="flex items-center justify-between pb-4 border-b border-black/[0.04] dark:border-white/[0.04]">
            <div>
              <h3 className="text-[15px] font-semibold text-[#1d1d1f] dark:text-[#f5f5f7] flex items-center gap-2">
                <MapPin className="w-4 h-4 text-[#0071e3] dark:text-[#2997ff]" />
                Regional Turnout &amp; Polling Station Performance
              </h3>
              <p className="text-[12px] text-[#86868b] dark:text-[#a1a1a6] mt-0.5">
                Constituency aggregation across all 5 geographical zones
              </p>
            </div>
            <span className="text-[11px] font-medium text-[#86868b] dark:text-[#a1a1a6]">
              {kpis.totalPollingBooths.toLocaleString()} Total Booths
            </span>
          </div>

          <div className="overflow-x-auto mt-3">
            <table className="w-full text-left">
              <thead className="text-[11px] uppercase tracking-wider text-[#86868b] dark:text-[#a1a1a6] border-b border-black/[0.04] dark:border-white/[0.04]">
                <tr>
                  <th className="py-2.5 px-3 font-semibold">Electoral Region</th>
                  <th className="py-2.5 px-3 font-semibold">Polling Booths</th>
                  <th className="py-2.5 px-3 font-semibold">Registered Voters</th>
                  <th className="py-2.5 px-3 font-semibold">Voter Turnout %</th>
                  <th className="py-2.5 px-3 font-semibold">Phase Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-black/[0.03] dark:divide-white/[0.03] text-[13px]">
                {regionalTurnout.map((row) => (
                  <tr key={row.region} className="hover:bg-black/[0.02] dark:hover:bg-white/[0.02] transition-colors">
                    <td className="py-3 px-3 font-semibold text-[#1d1d1f] dark:text-[#f5f5f7] whitespace-nowrap">
                      {row.region}
                    </td>
                    <td className="py-3 px-3 text-[#86868b] dark:text-[#a1a1a6] font-mono text-[12px] whitespace-nowrap">
                      {row.pollingBooths.toLocaleString()}
                    </td>
                    <td className="py-3 px-3 text-[#86868b] dark:text-[#a1a1a6] font-mono text-[12px] whitespace-nowrap">
                      {row.totalVoters}
                    </td>
                    <td className="py-3 px-3 whitespace-nowrap">
                      <div className="flex items-center gap-2">
                        <span className="font-semibold text-[#34c759] dark:text-[#30d158] font-mono text-[12px]">
                          {row.voterTurnoutPercent}%
                        </span>
                        <div className="w-20 bg-black/[0.06] dark:bg-white/[0.1] rounded-full h-1.5 overflow-hidden">
                          <div
                            className="bg-[#34c759] dark:bg-[#30d158] h-1.5 rounded-full"
                            style={{ width: `${row.voterTurnoutPercent}%` }}
                          />
                        </div>
                      </div>
                    </td>
                    <td className="py-3 px-3 whitespace-nowrap">
                      <span className="text-[11px] font-medium text-[#34c759] dark:text-[#30d158] bg-[#34c759]/10 px-2 py-0.5 rounded-full">
                        {row.phaseStatus}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Strategic Intelligence Summary Card */}
        <div className="bg-white dark:bg-[#1c1c1e] border border-black/[0.06] dark:border-white/[0.08] rounded-2xl p-5 sm:p-6 shadow-[0_2px_12px_rgba(0,0,0,0.03)] dark:shadow-none flex flex-col justify-between transition-colors">
          <div>
            <h3 className="text-[15px] font-semibold text-[#1d1d1f] dark:text-[#f5f5f7] flex items-center gap-2 pb-4 border-b border-black/[0.04] dark:border-white/[0.04]">
              <Layers className="w-4 h-4 text-[#0071e3] dark:text-[#2997ff]" />
              National Highlights
            </h3>

            <div className="space-y-3 mt-4">
              <div className="p-3 rounded-xl bg-black/[0.02] dark:bg-white/[0.03] border border-black/[0.04] dark:border-white/[0.04]">
                <div className="text-[11px] text-[#86868b] dark:text-[#a1a1a6] font-medium">Total Constituencies</div>
                <div className="text-lg font-bold text-[#1d1d1f] dark:text-[#f5f5f7] mt-0.5">
                  {kpis.totalConstituencies} Lok Sabha Seats
                </div>
                <div className="text-[11px] text-[#86868b] dark:text-[#a1a1a6] mt-0.5">
                  Single-member plurality system across 28 states &amp; 8 UTs.
                </div>
              </div>

              <div className="p-3 rounded-xl bg-black/[0.02] dark:bg-white/[0.03] border border-black/[0.04] dark:border-white/[0.04]">
                <div className="text-[11px] text-[#86868b] dark:text-[#a1a1a6] font-medium">Candidate Nominations</div>
                <div className="text-lg font-bold text-[#1d1d1f] dark:text-[#f5f5f7] mt-0.5">
                  {kpis.totalCandidates.toLocaleString()} Candidates
                </div>
                <div className="text-[11px] text-[#86868b] dark:text-[#a1a1a6] mt-0.5">
                  Average of 15.5 candidates per parliamentary seat.
                </div>
              </div>

              <div className="p-3 rounded-xl bg-black/[0.02] dark:bg-white/[0.03] border border-black/[0.04] dark:border-white/[0.04]">
                <div className="text-[11px] text-[#86868b] dark:text-[#a1a1a6] font-medium">Intelligence Inquiries</div>
                <div className="text-lg font-bold text-[#0071e3] dark:text-[#2997ff] mt-0.5">
                  {kpis.aiQueriesProcessed.toLocaleString()} Queries
                </div>
                <div className="text-[11px] text-[#86868b] dark:text-[#a1a1a6] mt-0.5">
                  Statutory compliance and turnout analytics.
                </div>
              </div>
            </div>
          </div>

          <div className="pt-3 mt-4 border-t border-black/[0.04] dark:border-white/[0.04] flex items-center justify-between text-[11px] text-[#86868b] dark:text-[#a1a1a6]">
            <span className="flex items-center gap-1.5">
              <CheckCircle2 className="w-3.5 h-3.5 text-[#34c759] dark:text-[#30d158]" />
              Real-time audit chain valid
            </span>
            <span className="font-mono text-[10px]">ECI-SYNCED</span>
          </div>
        </div>
      </div>
    </div>
  );
}

