'use client';

import React, { useState } from 'react';
import {
  Search,
  Vote,
  ShieldCheck,
  MapPin,
  GraduationCap,
  IndianRupee,
  AlertTriangle,
  CheckCircle,
  ChevronRight,
} from 'lucide-react';
import { Candidate, Constituency, Election, Party, SearchHit } from '@/lib/types';

interface PublicPortalViewProps {
  elections: Election[];
  candidates: Candidate[];
  constituencies: Constituency[];
  parties: Party[];
  onSearch: (query: string) => SearchHit[];
}

export function PublicPortalView({
  candidates,
  constituencies,
  parties,
  onSearch,
}: PublicPortalViewProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedParty, setSelectedParty] = useState<string>('ALL');
  const [selectedConstituency, setSelectedConstituency] = useState<string>('ALL');

  const searchHits = searchQuery.trim() ? onSearch(searchQuery) : [];

  // Filtered candidate list for affidavit explorer
  const filteredCandidates = candidates.filter((c) => {
    if (selectedParty !== 'ALL' && c.party_id !== selectedParty) return false;
    if (selectedConstituency !== 'ALL' && c.constituency_id !== selectedConstituency) return false;
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase();
      const party = parties.find((p) => p.id === c.party_id);
      const con = constituencies.find((k) => k.id === c.constituency_id);
      const match =
        c.name.toLowerCase().includes(q) ||
        party?.code.toLowerCase().includes(q) ||
        con?.name.toLowerCase().includes(q);
      if (!match) return false;
    }
    return true;
  });

  return (
    <div className="p-6 sm:p-8 space-y-6 max-w-7xl mx-auto">
      {/* Apple Header */}
      <div>
        <h2 className="text-2xl sm:text-3xl font-bold text-[#1d1d1f] dark:text-[#f5f5f7] tracking-tight">
          Public Portal
        </h2>
        <p className="text-[13px] text-[#86868b] dark:text-[#a1a1a6] mt-1">
          Public-facing election search, candidate background checks, constituency mapping, and verified data transparency.
        </p>
      </div>

      {/* Search Box Banner (Apple Spotlight Search Card style) */}
      <div className="bg-white dark:bg-[#1c1c1e] border border-black/[0.06] dark:border-white/[0.08] rounded-3xl p-6 sm:p-8 shadow-[0_4px_20px_rgba(0,0,0,0.04)] dark:shadow-none transition-colors">
        <div className="max-w-2xl mx-auto text-center space-y-3">
          <h3 className="text-xl sm:text-2xl font-bold text-[#1d1d1f] dark:text-[#f5f5f7] tracking-tight">
            Search Elections, Candidates &amp; Constituencies
          </h3>
          <p className="text-[12px] text-[#86868b] dark:text-[#a1a1a6]">
            Real-time public database verified against statutory Election Commission gazettes
          </p>

          <div className="relative flex items-center pt-2">
            <Search className="w-4 h-4 text-[#86868b] absolute left-4 pointer-events-none" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search candidate name, constituency, or party... (e.g. Modi, Wayanad, Varanasi)"
              className="w-full bg-[#f5f5f7] dark:bg-black/60 border border-black/[0.06] dark:border-white/[0.08] rounded-2xl py-3 pl-11 pr-24 text-[13px] text-[#1d1d1f] dark:text-[#f5f5f7] placeholder-[#86868b] focus:outline-none focus:ring-2 focus:ring-[#0071e3]/40 dark:focus:ring-[#2997ff]/40 transition-all"
            />
            {searchQuery && (
              <button
                type="button"
                onClick={() => setSearchQuery('')}
                className="absolute right-20 text-[11px] text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7] px-2 py-1 cursor-pointer"
              >
                Clear
              </button>
            )}
            <button
              type="button"
              className="absolute right-1.5 top-3.5 bottom-1.5 px-4 bg-[#0071e3] hover:bg-[#0077ed] dark:bg-[#2997ff] dark:hover:bg-[#47a6ff] text-white font-medium text-[12px] rounded-xl transition-all cursor-pointer active:scale-95 shadow-sm"
            >
              Search
            </button>
          </div>
        </div>
      </div>

      {/* 3 Public Features Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        <div className="bg-white dark:bg-[#1c1c1e] border border-black/[0.06] dark:border-white/[0.08] rounded-2xl p-5 shadow-[0_2px_12px_rgba(0,0,0,0.03)] dark:shadow-none flex items-start gap-3.5 transition-colors">
          <div className="w-10 h-10 rounded-xl bg-[#0071e3]/10 dark:bg-[#2997ff]/15 text-[#0071e3] dark:text-[#2997ff] flex items-center justify-center shrink-0">
            <Vote className="w-5 h-5" />
          </div>
          <div>
            <h4 className="font-semibold text-[#1d1d1f] dark:text-[#f5f5f7] text-[14px]">General Election 2026</h4>
            <p className="text-[12px] text-[#86868b] dark:text-[#a1a1a6] mt-0.5">
              543 Constituencies · 968.8M Voters across 7 electoral phases.
            </p>
          </div>
        </div>

        <div className="bg-white dark:bg-[#1c1c1e] border border-black/[0.06] dark:border-white/[0.08] rounded-2xl p-5 shadow-[0_2px_12px_rgba(0,0,0,0.03)] dark:shadow-none flex items-start gap-3.5 transition-colors">
          <div className="w-10 h-10 rounded-xl bg-[#34c759]/10 text-[#34c759] dark:text-[#30d158] flex items-center justify-center shrink-0">
            <ShieldCheck className="w-5 h-5" />
          </div>
          <div>
            <h4 className="font-semibold text-[#1d1d1f] dark:text-[#f5f5f7] text-[14px]">Candidate Affidavits</h4>
            <p className="text-[12px] text-[#86868b] dark:text-[#a1a1a6] mt-0.5">
              8,420 Form 26 Asset &amp; Criminal Declarations indexed and audited.
            </p>
          </div>
        </div>

        <div className="bg-white dark:bg-[#1c1c1e] border border-black/[0.06] dark:border-white/[0.08] rounded-2xl p-5 shadow-[0_2px_12px_rgba(0,0,0,0.03)] dark:shadow-none flex items-start gap-3.5 transition-colors">
          <div className="w-10 h-10 rounded-xl bg-[#af52de]/10 text-[#af52de] dark:text-[#bf5af2] flex items-center justify-center shrink-0">
            <MapPin className="w-5 h-5" />
          </div>
          <div>
            <h4 className="font-semibold text-[#1d1d1f] dark:text-[#f5f5f7] text-[14px]">Constituency GIS Map</h4>
            <p className="text-[12px] text-[#86868b] dark:text-[#a1a1a6] mt-0.5">
              Delimitation boundaries &amp; Polling Booth GIS coordinates.
            </p>
          </div>
        </div>
      </div>

      {/* Dynamic Search Hits (When search is active) */}
      {searchHits.length > 0 && (
        <div className="bg-white dark:bg-[#1c1c1e] border border-black/[0.06] dark:border-white/[0.08] rounded-2xl p-5 shadow-[0_2px_12px_rgba(0,0,0,0.03)] dark:shadow-none transition-colors">
          <div className="flex items-center justify-between pb-3 border-b border-black/[0.04] dark:border-white/[0.04] mb-3">
            <h3 className="text-[13px] font-semibold text-[#1d1d1f] dark:text-[#f5f5f7] flex items-center gap-2">
              <Search className="w-3.5 h-3.5 text-[#0071e3] dark:text-[#2997ff]" />
              Found {searchHits.length} Result{searchHits.length > 1 ? 's' : ''} for &quot;{searchQuery}&quot;
            </h3>
            <span className="text-[11px] text-[#86868b] dark:text-[#a1a1a6]">Verified Search Index</span>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-2.5">
            {searchHits.map((hit) => (
              <div
                key={`${hit.entity_type}-${hit.id}`}
                className="p-3 rounded-xl bg-black/[0.02] dark:bg-white/[0.03] border border-black/[0.04] dark:border-white/[0.04] hover:bg-black/[0.04] dark:hover:bg-white/[0.06] transition-colors flex items-center justify-between"
              >
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-[13px] font-semibold text-[#1d1d1f] dark:text-[#f5f5f7]">{hit.title}</span>
                    <span className="text-[10px] uppercase font-mono px-1.5 py-0.2 rounded bg-black/[0.04] dark:bg-white/[0.06] text-[#86868b] dark:text-[#a1a1a6]">
                      {hit.entity_type}
                    </span>
                  </div>
                  <p className="text-[11px] text-[#86868b] dark:text-[#a1a1a6] mt-0.5">{hit.subtitle}</p>
                </div>
                <ChevronRight className="w-4 h-4 text-[#86868b]" />
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Candidate Affidavits Explorer */}
      <div className="bg-white dark:bg-[#1c1c1e] border border-black/[0.06] dark:border-white/[0.08] rounded-2xl p-5 sm:p-6 shadow-[0_2px_12px_rgba(0,0,0,0.03)] dark:shadow-none transition-colors">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-black/[0.04] dark:border-white/[0.04]">
          <div>
            <h3 className="text-[15px] font-semibold text-[#1d1d1f] dark:text-[#f5f5f7] flex items-center gap-2">
              <ShieldCheck className="w-4 h-4 text-[#34c759] dark:text-[#30d158]" />
              Candidate Form 26 Affidavits &amp; Disclosures
            </h3>
            <p className="text-[12px] text-[#86868b] dark:text-[#a1a1a6] mt-0.5">
              Verified statutory declarations of wealth, education, and judicial history
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-2">
            {/* Filter by Party */}
            <div className="flex items-center gap-1.5">
              <span className="text-[11px] text-[#86868b] dark:text-[#a1a1a6]">Party:</span>
              <select
                value={selectedParty}
                onChange={(e) => setSelectedParty(e.target.value)}
                className="text-[12px] bg-black/[0.03] dark:bg-white/[0.05] border border-black/[0.06] dark:border-white/[0.08] rounded-xl px-2 py-1 text-[#1d1d1f] dark:text-[#f5f5f7] focus:outline-none focus:ring-2 focus:ring-[#0071e3]/30"
              >
                <option value="ALL">All Parties</option>
                {parties.map((p) => (
                  <option key={p.id} value={p.id}>
                    {p.name} ({p.code})
                  </option>
                ))}
              </select>
            </div>

            {/* Filter by Constituency */}
            <div className="flex items-center gap-1.5">
              <span className="text-[11px] text-[#86868b] dark:text-[#a1a1a6]">Seat:</span>
              <select
                value={selectedConstituency}
                onChange={(e) => setSelectedConstituency(e.target.value)}
                className="text-[12px] bg-black/[0.03] dark:bg-white/[0.05] border border-black/[0.06] dark:border-white/[0.08] rounded-xl px-2 py-1 text-[#1d1d1f] dark:text-[#f5f5f7] focus:outline-none focus:ring-2 focus:ring-[#0071e3]/30"
              >
                <option value="ALL">All Constituencies</option>
                {constituencies.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.name} ({c.code})
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {/* Candidate Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mt-5">
          {filteredCandidates.map((cand) => {
            const party = parties.find((p) => p.id === cand.party_id);
            const constituency = constituencies.find((c) => c.id === cand.constituency_id);
            return (
              <div
                key={cand.id}
                className="p-4 rounded-xl bg-black/[0.02] dark:bg-white/[0.03] border border-black/[0.04] dark:border-white/[0.04] hover:border-black/[0.1] dark:hover:border-white/[0.1] transition-all flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-start justify-between gap-2 mb-2.5">
                    <div>
                      <h4 className="text-[14px] font-semibold text-[#1d1d1f] dark:text-[#f5f5f7]">{cand.name}</h4>
                      <p className="text-[11px] text-[#86868b] dark:text-[#a1a1a6] flex items-center gap-1 mt-0.5">
                        <MapPin className="w-3 h-3 text-[#86868b]" />
                        {constituency?.name} ({constituency?.code}), {constituency?.state_name}
                      </p>
                    </div>
                    <span
                      className="text-[11px] font-medium px-2 py-0.5 rounded-md text-white"
                      style={{ backgroundColor: party?.color || '#0071e3' }}
                    >
                      {party?.code || 'IND'}
                    </span>
                  </div>

                  <div className="space-y-2 py-2.5 border-y border-black/[0.04] dark:border-white/[0.04] text-[12px]">
                    <div className="flex items-center justify-between">
                      <span className="text-[#86868b] dark:text-[#a1a1a6] flex items-center gap-1.5">
                        <GraduationCap className="w-3.5 h-3.5 text-[#0071e3] dark:text-[#2997ff]" />
                        Education
                      </span>
                      <span className="text-[#1d1d1f] dark:text-[#f5f5f7] font-medium truncate max-w-[160px]">
                        {cand.education}
                      </span>
                    </div>

                    <div className="flex items-center justify-between">
                      <span className="text-[#86868b] dark:text-[#a1a1a6] flex items-center gap-1.5">
                        <IndianRupee className="w-3.5 h-3.5 text-[#34c759] dark:text-[#30d158]" />
                        Declared Assets
                      </span>
                      <span className="text-[#34c759] dark:text-[#30d158] font-semibold font-mono">
                        ₹{cand.declared_assets_cr.toFixed(2)} Cr
                      </span>
                    </div>

                    <div className="flex items-center justify-between">
                      <span className="text-[#86868b] dark:text-[#a1a1a6] flex items-center gap-1.5">
                        <AlertTriangle
                          className={`w-3.5 h-3.5 ${
                            cand.criminal_cases > 0 ? 'text-[#ff9500]' : 'text-[#86868b]'
                          }`}
                        />
                        Criminal Cases
                      </span>
                      <span
                        className={`font-semibold font-mono ${
                          cand.criminal_cases > 0 ? 'text-[#ff9500]' : 'text-[#86868b]'
                        }`}
                      >
                        {cand.criminal_cases}
                      </span>
                    </div>
                  </div>
                </div>

                <div className="mt-3 pt-2 flex items-center justify-between text-[11px]">
                  <span className="flex items-center gap-1 text-[#34c759] dark:text-[#30d158] font-medium">
                    <CheckCircle className="w-3 h-3" />
                    Verified
                  </span>
                  <span className="text-[#86868b] dark:text-[#a1a1a6] font-mono text-[10px]">
                    Filed {cand.submission_date}
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

