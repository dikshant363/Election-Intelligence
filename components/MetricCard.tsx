'use client';

import React from 'react';
import { LucideIcon } from 'lucide-react';

interface MetricCardProps {
  title: string;
  value: string;
  subtitle: string;
  icon: LucideIcon;
  iconColorClass?: string;
  badgeText?: string;
  badgeColorClass?: string;
}

export function MetricCard({
  title,
  value,
  subtitle,
  icon: Icon,
  iconColorClass = 'text-[#0071e3] dark:text-[#2997ff] bg-[#0071e3]/10 dark:bg-[#2997ff]/15',
  badgeText,
  badgeColorClass = 'text-[#34c759] dark:text-[#30d158] bg-[#34c759]/10',
}: MetricCardProps) {
  return (
    <div className="bg-white dark:bg-[#1c1c1e] border border-black/[0.06] dark:border-white/[0.08] rounded-2xl p-4 sm:p-5 shadow-[0_2px_12px_rgba(0,0,0,0.03)] dark:shadow-none hover:border-black/[0.12] dark:hover:border-white/[0.15] transition-all flex flex-col justify-between">
      <div>
        <div className="flex items-center justify-between mb-3">
          <div className={`p-2 rounded-xl ${iconColorClass}`}>
            <Icon className="w-4 h-4" />
          </div>
          {badgeText && (
            <span
              className={`text-[11px] font-medium px-2 py-0.5 rounded-full ${badgeColorClass}`}
            >
              {badgeText}
            </span>
          )}
        </div>
        <div className="text-2xl sm:text-[28px] font-bold tracking-tight text-[#1d1d1f] dark:text-[#f5f5f7] mb-1">
          {value}
        </div>
        <div className="text-[13px] font-medium text-[#86868b] dark:text-[#a1a1a6]">
          {title}
        </div>
      </div>
      <div className="text-[11px] text-[#86868b] dark:text-[#a1a1a6] pt-3 border-t border-black/[0.04] dark:border-white/[0.04] mt-3 flex items-center justify-between">
        <span>{subtitle}</span>
      </div>
    </div>
  );
}

