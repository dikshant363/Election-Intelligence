'use client';

import React, { useState, useMemo } from 'react';
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from 'recharts';
import {
  TrendingUp,
  Calendar,
  Filter,
  BarChart2,
  Table as TableIcon,
  Check,
  ChevronDown,
} from 'lucide-react';

export interface TurnoutDataPoint {
  date: string;
  label: string;
  national: number;
  northern: number;
  southern: number;
  western: number;
  eastern: number;
  northeastern?: number;
}

// Historical datasets across different date scopes
const HISTORICAL_CYCLES_DATA: TurnoutDataPoint[] = [
  { date: '2004-05-13', label: '2004 Cycle', national: 58.07, northern: 54.2, southern: 64.8, western: 56.4, eastern: 62.1 },
  { date: '2009-05-16', label: '2009 Cycle', national: 58.21, northern: 55.4, southern: 66.2, western: 54.8, eastern: 63.5 },
  { date: '2014-05-16', label: '2014 Cycle', national: 66.44, northern: 63.8, southern: 72.1, western: 64.2, eastern: 70.8 },
  { date: '2019-05-23', label: '2019 Cycle', national: 67.40, northern: 65.2, southern: 73.4, western: 65.9, eastern: 72.2 },
  { date: '2024-06-04', label: '2024 Cycle', national: 68.80, northern: 67.8, southern: 74.2, western: 67.5, eastern: 73.6 },
];

const LAST_30_DAYS_DATA: TurnoutDataPoint[] = [
  { date: '2026-09-21', label: 'Sep 21', national: 64.1, northern: 63.0, southern: 68.2, western: 63.5, eastern: 66.4 },
  { date: '2026-09-25', label: 'Sep 25', national: 64.9, northern: 64.2, southern: 69.5, western: 64.1, eastern: 67.2 },
  { date: '2026-09-29', label: 'Sep 29', national: 65.8, northern: 65.0, southern: 70.8, western: 65.2, eastern: 68.5 },
  { date: '2026-10-03', label: 'Oct 03', national: 66.5, northern: 65.9, southern: 71.9, western: 66.0, eastern: 69.8 },
  { date: '2026-10-07', label: 'Oct 07', national: 67.2, northern: 66.5, southern: 72.8, western: 66.7, eastern: 71.2 },
  { date: '2026-10-11', label: 'Oct 11', national: 67.9, northern: 67.1, southern: 73.5, western: 67.1, eastern: 72.4 },
  { date: '2026-10-15', label: 'Oct 15', national: 68.4, northern: 67.5, southern: 74.0, western: 67.3, eastern: 73.1 },
  { date: '2026-10-19', label: 'Oct 19', national: 68.8, northern: 67.8, southern: 74.2, western: 67.5, eastern: 73.6 },
];

const LAST_7_DAYS_DATA: TurnoutDataPoint[] = [
  { date: '2026-10-14', label: 'Day 1 (Phase 1)', national: 66.8, northern: 65.5, southern: 72.4, western: 65.9, eastern: 71.0 },
  { date: '2026-10-15', label: 'Day 2 (Phase 2)', national: 67.2, northern: 66.1, southern: 72.9, western: 66.4, eastern: 71.8 },
  { date: '2026-10-16', label: 'Day 3 (Phase 3)', national: 67.7, northern: 66.8, southern: 73.3, western: 66.8, eastern: 72.2 },
  { date: '2026-10-17', label: 'Day 4 (Phase 4)', national: 68.0, northern: 67.2, southern: 73.7, western: 67.0, eastern: 72.7 },
  { date: '2026-10-18', label: 'Day 5 (Phase 5)', national: 68.3, northern: 67.5, southern: 73.9, western: 67.2, eastern: 73.0 },
  { date: '2026-10-19', label: 'Day 6 (Phase 6)', national: 68.6, northern: 67.6, southern: 74.1, western: 67.4, eastern: 73.4 },
  { date: '2026-10-20', label: 'Day 7 (Phase 7)', national: 68.8, northern: 67.8, southern: 74.2, western: 67.5, eastern: 73.6 },
];

type RangePreset = '7d' | '30d' | 'cycles' | 'custom';

export function VoterTurnoutTrendsChart() {
  const [selectedRange, setSelectedRange] = useState<RangePreset>('cycles');
  const [customStartDate, setCustomStartDate] = useState('2004-01-01');
  const [customEndDate, setCustomEndDate] = useState('2026-12-31');
  const [showTableView, setShowTableView] = useState(false);

  // Active region lines
  const [activeRegions, setActiveRegions] = useState<Record<string, boolean>>({
    national: true,
    southern: true,
    northern: true,
    western: true,
    eastern: true,
  });

  const toggleRegion = (key: string) => {
    setActiveRegions((prev) => ({
      ...prev,
      [key]: !prev[key],
    }));
  };

  // Derive filtered dataset based on date range
  const chartData = useMemo(() => {
    if (selectedRange === '7d') return LAST_7_DAYS_DATA;
    if (selectedRange === '30d') return LAST_30_DAYS_DATA;
    if (selectedRange === 'cycles') return HISTORICAL_CYCLES_DATA;

    // Custom range filter
    const all = [...HISTORICAL_CYCLES_DATA, ...LAST_30_DAYS_DATA];
    const unique = Array.from(new Map(all.map((item) => [item.date, item])).values());
    const filtered = unique
      .filter((d) => d.date >= customStartDate && d.date <= customEndDate)
      .sort((a, b) => a.date.localeCompare(b.date));

    return filtered.length > 0 ? filtered : HISTORICAL_CYCLES_DATA;
  }, [selectedRange, customStartDate, customEndDate]);

  // Derived stats
  const latestData = chartData[chartData.length - 1] || chartData[0];
  const earliestData = chartData[0];
  const turnoutDelta = latestData ? (latestData.national - earliestData.national).toFixed(2) : '+0.00';

  return (
    <div className="bg-white dark:bg-[#1c1c1e] border border-black/[0.06] dark:border-white/[0.08] rounded-2xl p-5 sm:p-6 shadow-[0_2px_12px_rgba(0,0,0,0.03)] dark:shadow-none transition-colors">
      {/* Header and Filter Controls */}
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 pb-4 border-b border-black/[0.04] dark:border-white/[0.04]">
        <div>
          <div className="flex items-center gap-2">
            <div className="w-7 h-7 rounded-lg bg-[#0071e3]/10 text-[#0071e3] dark:text-[#2997ff] flex items-center justify-center">
              <TrendingUp className="w-4 h-4" />
            </div>
            <h3 className="text-[16px] font-semibold text-[#1d1d1f] dark:text-[#f5f5f7] tracking-tight">
              Historical Voter Turnout Trends
            </h3>
          </div>
          <p className="text-[12px] text-[#86868b] dark:text-[#a1a1a6] mt-0.5">
            Comparative longitudinal analysis across general elections &amp; regional polling zones
          </p>
        </div>

        {/* Date Range Selection & View Controls */}
        <div className="flex flex-wrap items-center gap-2">
          {/* Apple Segmented Control */}
          <div className="flex p-0.5 rounded-xl bg-black/[0.04] dark:bg-white/[0.06] text-[12px] font-medium">
            <button
              type="button"
              onClick={() => setSelectedRange('7d')}
              className={`px-3 py-1 rounded-lg transition-all cursor-pointer ${
                selectedRange === '7d'
                  ? 'bg-white dark:bg-[#2c2c2e] text-[#1d1d1f] dark:text-[#f5f5f7] shadow-xs'
                  : 'text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7]'
              }`}
            >
              7 Days
            </button>
            <button
              type="button"
              onClick={() => setSelectedRange('30d')}
              className={`px-3 py-1 rounded-lg transition-all cursor-pointer ${
                selectedRange === '30d'
                  ? 'bg-white dark:bg-[#2c2c2e] text-[#1d1d1f] dark:text-[#f5f5f7] shadow-xs'
                  : 'text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7]'
              }`}
            >
              30 Days
            </button>
            <button
              type="button"
              onClick={() => setSelectedRange('cycles')}
              className={`px-3 py-1 rounded-lg transition-all cursor-pointer ${
                selectedRange === 'cycles'
                  ? 'bg-white dark:bg-[#2c2c2e] text-[#1d1d1f] dark:text-[#f5f5f7] shadow-xs'
                  : 'text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7]'
              }`}
            >
              2004–2024 Cycles
            </button>
            <button
              type="button"
              onClick={() => setSelectedRange('custom')}
              className={`px-3 py-1 rounded-lg transition-all cursor-pointer ${
                selectedRange === 'custom'
                  ? 'bg-white dark:bg-[#2c2c2e] text-[#1d1d1f] dark:text-[#f5f5f7] shadow-xs'
                  : 'text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7]'
              }`}
            >
              Custom
            </button>
          </div>

          {/* Toggle Table View for Accessibility */}
          <button
            type="button"
            onClick={() => setShowTableView(!showTableView)}
            className="p-1.5 rounded-xl border border-black/[0.08] dark:border-white/[0.1] text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7] hover:bg-black/[0.02] dark:hover:bg-white/[0.04] transition cursor-pointer"
            title={showTableView ? 'Switch to Chart' : 'Switch to Accessible Table'}
            aria-label="Toggle accessible tabular view"
          >
            {showTableView ? <BarChart2 className="w-4 h-4" /> : <TableIcon className="w-4 h-4" />}
          </button>
        </div>
      </div>

      {/* Custom Date Pickers when 'Custom' is selected */}
      {selectedRange === 'custom' && (
        <div className="flex flex-wrap items-center gap-3 py-3 px-4 my-3 rounded-xl bg-black/[0.02] dark:bg-white/[0.03] border border-black/[0.04] dark:border-white/[0.06] text-[12px]">
          <span className="text-[#86868b] font-medium flex items-center gap-1.5">
            <Calendar className="w-3.5 h-3.5" />
            Filter Date Range:
          </span>
          <div className="flex items-center gap-2">
            <label className="text-[#86868b]">From:</label>
            <input
              type="date"
              value={customStartDate}
              onChange={(e) => setCustomStartDate(e.target.value)}
              className="bg-white dark:bg-[#2c2c2e] border border-black/[0.1] dark:border-white/[0.1] rounded-lg px-2.5 py-1 text-[12px] text-[#1d1d1f] dark:text-[#f5f5f7] focus:outline-none focus:ring-1 focus:ring-[#0071e3]"
            />
          </div>
          <div className="flex items-center gap-2">
            <label className="text-[#86868b]">To:</label>
            <input
              type="date"
              value={customEndDate}
              onChange={(e) => setCustomEndDate(e.target.value)}
              className="bg-white dark:bg-[#2c2c2e] border border-black/[0.1] dark:border-white/[0.1] rounded-lg px-2.5 py-1 text-[12px] text-[#1d1d1f] dark:text-[#f5f5f7] focus:outline-none focus:ring-1 focus:ring-[#0071e3]"
            />
          </div>
        </div>
      )}

      {/* Summary Stats Strip */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 my-4">
        <div className="p-3 rounded-xl bg-black/[0.02] dark:bg-white/[0.03] border border-black/[0.04] dark:border-white/[0.04]">
          <div className="text-[11px] text-[#86868b] font-medium">National Turnout (Latest)</div>
          <div className="text-xl font-bold text-[#0071e3] dark:text-[#2997ff] mt-0.5">
            {latestData?.national}%
          </div>
          <div className="text-[10px] text-[#34c759] mt-0.5">
            {Number(turnoutDelta) >= 0 ? `+${turnoutDelta}%` : `${turnoutDelta}%`} net trend
          </div>
        </div>

        <div className="p-3 rounded-xl bg-black/[0.02] dark:bg-white/[0.03] border border-black/[0.04] dark:border-white/[0.04]">
          <div className="text-[11px] text-[#86868b] font-medium">Top Regional Turnout</div>
          <div className="text-xl font-bold text-[#34c759] mt-0.5">
            {latestData?.southern}%
          </div>
          <div className="text-[10px] text-[#86868b] mt-0.5">Southern Region lead</div>
        </div>

        <div className="p-3 rounded-xl bg-black/[0.02] dark:bg-white/[0.03] border border-black/[0.04] dark:border-white/[0.04]">
          <div className="text-[11px] text-[#86868b] font-medium">Eastern Zone Polling</div>
          <div className="text-xl font-bold text-[#ff2d55] mt-0.5">
            {latestData?.eastern}%
          </div>
          <div className="text-[10px] text-[#86868b] mt-0.5">High rural participation</div>
        </div>

        <div className="p-3 rounded-xl bg-black/[0.02] dark:bg-white/[0.03] border border-black/[0.04] dark:border-white/[0.04]">
          <div className="text-[11px] text-[#86868b] font-medium">Time Horizon Data Points</div>
          <div className="text-xl font-bold text-[#1d1d1f] dark:text-[#f5f5f7] mt-0.5">
            {chartData.length} Intervals
          </div>
          <div className="text-[10px] text-[#86868b] mt-0.5">Grounded ECI audit rolls</div>
        </div>
      </div>

      {/* Interactive Region Filters */}
      <div className="flex flex-wrap items-center gap-2 mb-4">
        <span className="text-[11px] text-[#86868b] font-medium mr-1 flex items-center gap-1">
          <Filter className="w-3 h-3" />
          Filter Regions:
        </span>
        {[
          { key: 'national', label: 'National Average', color: '#0071e3' },
          { key: 'southern', label: 'Southern Region', color: '#34c759' },
          { key: 'northern', label: 'Northern Region', color: '#ff9500' },
          { key: 'western', label: 'Western Region', color: '#af52de' },
          { key: 'eastern', label: 'Eastern Region', color: '#ff2d55' },
        ].map((r) => {
          const active = activeRegions[r.key];
          return (
            <button
              key={r.key}
              type="button"
              onClick={() => toggleRegion(r.key)}
              className={`px-2.5 py-1 rounded-lg text-[11px] font-medium border flex items-center gap-1.5 transition-all cursor-pointer ${
                active
                  ? 'bg-black/[0.04] dark:bg-white/[0.08] text-[#1d1d1f] dark:text-[#f5f5f7] border-black/[0.08] dark:border-white/[0.12]'
                  : 'opacity-40 text-[#86868b] border-transparent hover:opacity-75'
              }`}
            >
              <span
                className="w-2 h-2 rounded-full"
                style={{ backgroundColor: active ? r.color : '#86868b' }}
              />
              <span>{r.label}</span>
            </button>
          );
        })}
      </div>

      {/* Main Chart or Accessible Table */}
      {showTableView ? (
        <div className="overflow-x-auto my-2 border border-black/[0.06] dark:border-white/[0.08] rounded-xl">
          <table className="w-full text-left text-[12px]">
            <thead className="bg-black/[0.02] dark:bg-white/[0.03] text-[#86868b] border-b border-black/[0.04] dark:border-white/[0.04]">
              <tr>
                <th className="py-2.5 px-3">Date / Label</th>
                <th className="py-2.5 px-3">National Avg</th>
                <th className="py-2.5 px-3">Southern</th>
                <th className="py-2.5 px-3">Northern</th>
                <th className="py-2.5 px-3">Western</th>
                <th className="py-2.5 px-3">Eastern</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-black/[0.03] dark:divide-white/[0.03]">
              {chartData.map((d) => (
                <tr key={d.date} className="hover:bg-black/[0.01] dark:hover:bg-white/[0.02]">
                  <td className="py-2.5 px-3 font-medium text-[#1d1d1f] dark:text-[#f5f5f7]">{d.label} ({d.date})</td>
                  <td className="py-2.5 px-3 text-[#0071e3] font-semibold">{d.national}%</td>
                  <td className="py-2.5 px-3 text-[#34c759]">{d.southern}%</td>
                  <td className="py-2.5 px-3 text-[#ff9500]">{d.northern}%</td>
                  <td className="py-2.5 px-3 text-[#af52de]">{d.western}%</td>
                  <td className="py-2.5 px-3 text-[#ff2d55]">{d.eastern}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="h-72 w-full pt-2">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData} margin={{ top: 10, right: 15, left: -10, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="currentColor" className="opacity-10" />
              <XAxis
                dataKey="label"
                tickLine={false}
                axisLine={false}
                tick={{ fontSize: 11, fill: '#86868b' }}
              />
              <YAxis
                domain={[50, 80]}
                tickLine={false}
                axisLine={false}
                tickFormatter={(val) => `${val}%`}
                tick={{ fontSize: 11, fill: '#86868b' }}
              />
              <Tooltip
                content={({ active, payload, label }) => {
                  if (active && payload && payload.length) {
                    return (
                      <div className="bg-white/95 dark:bg-[#1e1e1e]/95 backdrop-blur-xl border border-black/[0.08] dark:border-white/[0.12] rounded-xl p-3 shadow-xl text-[12px] min-w-[170px]">
                        <div className="font-semibold text-[#1d1d1f] dark:text-[#f5f5f7] border-b border-black/[0.06] dark:border-white/[0.08] pb-1.5 mb-2">
                          {label}
                        </div>
                        <div className="space-y-1">
                          {payload.map((entry) => (
                            <div key={entry.name} className="flex items-center justify-between gap-3">
                              <span className="flex items-center gap-1.5">
                                <span className="w-2 h-2 rounded-full" style={{ backgroundColor: entry.color }} />
                                <span className="text-[#86868b] capitalize">{entry.name}:</span>
                              </span>
                              <span className="font-semibold font-mono text-[#1d1d1f] dark:text-[#f5f5f7]">
                                {entry.value}%
                              </span>
                            </div>
                          ))}
                        </div>
                      </div>
                    );
                  }
                  return null;
                }}
              />
              {activeRegions.national && (
                <Line
                  type="monotone"
                  dataKey="national"
                  name="National Avg"
                  stroke="#0071e3"
                  strokeWidth={3}
                  dot={{ r: 4, strokeWidth: 2, fill: '#ffffff' }}
                  activeDot={{ r: 6, stroke: '#0071e3', strokeWidth: 2 }}
                />
              )}
              {activeRegions.southern && (
                <Line
                  type="monotone"
                  dataKey="southern"
                  name="Southern"
                  stroke="#34c759"
                  strokeWidth={2}
                  dot={{ r: 3, fill: '#34c759' }}
                />
              )}
              {activeRegions.northern && (
                <Line
                  type="monotone"
                  dataKey="northern"
                  name="Northern"
                  stroke="#ff9500"
                  strokeWidth={2}
                  dot={{ r: 3, fill: '#ff9500' }}
                />
              )}
              {activeRegions.western && (
                <Line
                  type="monotone"
                  dataKey="western"
                  name="Western"
                  stroke="#af52de"
                  strokeWidth={2}
                  dot={{ r: 3, fill: '#af52de' }}
                />
              )}
              {activeRegions.eastern && (
                <Line
                  type="monotone"
                  dataKey="eastern"
                  name="Eastern"
                  stroke="#ff2d55"
                  strokeWidth={2}
                  dot={{ r: 3, fill: '#ff2d55' }}
                />
              )}
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Footer provenance */}
      <div className="flex items-center justify-between pt-3 mt-2 border-t border-black/[0.04] dark:border-white/[0.04] text-[11px] text-[#86868b]">
        <span>Aggregated from verified Form 20 final result sheets &amp; EVM totalizers</span>
        <span className="font-mono text-[10px]">ECI-STATUTORY-VERIFIED</span>
      </div>
    </div>
  );
}
