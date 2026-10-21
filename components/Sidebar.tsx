'use client';

import React from 'react';
import {
  Vote,
  LayoutDashboard,
  BarChart3,
  SlidersHorizontal,
  Globe,
  Radio,
} from 'lucide-react';
import { ControlInterface } from '@/lib/types';

interface SidebarProps {
  currentInterface: ControlInterface;
  onSelectInterface: (interfaceId: ControlInterface) => void;
  onOpenPalette: () => void;
}

export function Sidebar({
  currentInterface,
  onSelectInterface,
}: SidebarProps) {
  const navItems = [
    {
      id: 'enterpriseControlCenter' as ControlInterface,
      title: 'Enterprise Control',
      subtitle: 'Infrastructure & Security',
      icon: LayoutDashboard,
      color: 'text-[#0071e3] dark:text-[#2997ff]',
      bg: 'bg-[#0071e3]/10 dark:bg-[#2997ff]/15',
    },
    {
      id: 'executiveCommandCenter' as ControlInterface,
      title: 'Executive Command',
      subtitle: 'Strategic KPIs & Turnout',
      icon: BarChart3,
      color: 'text-[#ff9500] dark:text-[#ff9f0a]',
      bg: 'bg-[#ff9500]/10 dark:bg-[#ff9f0a]/15',
    },
    {
      id: 'operationsConsole' as ControlInterface,
      title: 'Operations Console',
      subtitle: 'Elections, Results & ETL',
      icon: SlidersHorizontal,
      color: 'text-[#5856d6] dark:text-[#5e5ce6]',
      bg: 'bg-[#5856d6]/10 dark:bg-[#5e5ce6]/15',
    },
    {
      id: 'publicPortal' as ControlInterface,
      title: 'Public Portal',
      subtitle: 'Transparency & Affidavits',
      icon: Globe,
      color: 'text-[#34c759] dark:text-[#30d158]',
      bg: 'bg-[#34c759]/10 dark:bg-[#30d158]/15',
    },
  ];

  return (
    <aside className="w-64 bg-[#f5f5f7]/70 dark:bg-[#161617]/75 backdrop-blur-2xl border-r border-black/[0.08] dark:border-white/[0.08] flex flex-col justify-between shrink-0 h-screen sticky top-0 select-none transition-colors">
      <div>
        {/* Apple macOS style App Title Header */}
        <div className="px-4 py-4 flex items-center gap-2.5 border-b border-black/[0.04] dark:border-white/[0.04]">
          <div className="w-8 h-8 rounded-xl bg-[#0071e3] dark:bg-[#2997ff] flex items-center justify-center text-white shadow-sm">
            <Vote className="w-4 h-4" />
          </div>
          <div>
            <h1 className="font-semibold text-[#1d1d1f] dark:text-[#f5f5f7] text-[13px] leading-tight">
              Election Intelligence
            </h1>
            <p className="text-[11px] text-[#86868b] dark:text-[#a1a1a6]">
              Commission Platform
            </p>
          </div>
        </div>

        {/* Section Label */}
        <div className="px-4 pt-5 pb-1.5 text-[11px] font-semibold tracking-wider text-[#86868b] dark:text-[#a1a1a6] uppercase">
          Workspaces
        </div>

        {/* Navigation List in macOS sidebar item style */}
        <nav className="px-2.5 space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isSelected = currentInterface === item.id;
            return (
              <button
                key={item.id}
                type="button"
                onClick={() => onSelectInterface(item.id)}
                className={`w-full text-left px-2.5 py-2 rounded-xl transition-all flex items-center gap-2.5 group cursor-pointer ${
                  isSelected
                    ? 'bg-[#0071e3] text-white shadow-sm font-semibold'
                    : 'text-[#1d1d1f] dark:text-[#f5f5f7] hover:bg-black/[0.05] dark:hover:bg-white/[0.08] font-normal'
                }`}
              >
                <div
                  className={`w-7 h-7 rounded-lg flex items-center justify-center shrink-0 transition-colors ${
                    isSelected
                      ? 'bg-white/20 text-white'
                      : `${item.bg} ${item.color}`
                  }`}
                >
                  <Icon className="w-4 h-4" />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="text-[13px] truncate leading-tight">
                    {item.title}
                  </div>
                  <div
                    className={`text-[11px] truncate mt-0.5 ${
                      isSelected
                        ? 'text-white/80'
                        : 'text-[#86868b] dark:text-[#a1a1a6]'
                    }`}
                  >
                    {item.subtitle}
                  </div>
                </div>
              </button>
            );
          })}
        </nav>

        {/* Telemetry Status (quiet Apple card) */}
        <div className="mx-3 mt-6 p-3 rounded-2xl bg-white/60 dark:bg-white/[0.04] border border-black/[0.04] dark:border-white/[0.06] shadow-sm">
          <div className="flex items-center gap-2 mb-1">
            <Radio className="w-3.5 h-3.5 text-[#34c759] dark:text-[#30d158] animate-pulse" />
            <span className="text-[12px] font-semibold text-[#1d1d1f] dark:text-[#f5f5f7]">
              Live Telemetry
            </span>
          </div>
          <p className="text-[11px] text-[#86868b] dark:text-[#a1a1a6] leading-relaxed">
            543 Constituencies synchronized via Event Bus.
          </p>
        </div>
      </div>

      {/* User Profile Footer */}
      <div className="p-3 border-t border-black/[0.06] dark:border-white/[0.06] bg-white/40 dark:bg-black/20">
        <div className="flex items-center justify-between px-1">
          <div className="flex items-center gap-2.5 min-w-0">
            <div className="w-7 h-7 rounded-full bg-[#0071e3]/10 dark:bg-[#2997ff]/20 text-[#0071e3] dark:text-[#2997ff] flex items-center justify-center font-semibold text-[11px]">
              EC
            </div>
            <div className="truncate">
              <div className="text-[12px] font-semibold text-[#1d1d1f] dark:text-[#f5f5f7] truncate">
                Super Administrator
              </div>
              <div className="text-[10px] text-[#86868b] dark:text-[#a1a1a6] truncate">
                ECI Security Tier 1
              </div>
            </div>
          </div>
          <div className="w-1.5 h-1.5 rounded-full bg-[#34c759] dark:bg-[#30d158]" />
        </div>
      </div>
    </aside>
  );
}
