'use client';

import React, { useState, useEffect } from 'react';
import {
  Search,
  X,
  Activity,
  Flag,
  Bot,
  Shield,
  Users,
  Trash2,
  RefreshCw,
  Upload,
  BarChart,
  Globe,
  ArrowRight,
  ShieldCheck,
} from 'lucide-react';
import { ControlInterface } from '@/lib/types';

interface CommandPaletteDialogProps {
  isOpen: boolean;
  onClose: () => void;
  onSelectInterface: (interfaceId: ControlInterface) => void;
  onTriggerAction: (actionKey: string) => void;
}

export function CommandPaletteDialog({
  isOpen,
  onClose,
  onSelectInterface,
  onTriggerAction,
}: CommandPaletteDialogProps) {
  const [filter, setFilter] = useState('');

  // Handle ESC and Cmd+K
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        if (isOpen) {
          onClose();
        }
      }
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const commands = [
    {
      title: 'View System Telemetry & Health',
      category: 'Enterprise Control',
      icon: Activity,
      targetInterface: 'enterpriseControlCenter' as ControlInterface,
    },
    {
      title: 'Manage Feature Flags',
      category: 'Enterprise Control',
      icon: Flag,
      targetInterface: 'enterpriseControlCenter' as ControlInterface,
    },
    {
      title: 'AI Model Routing & Prompts',
      category: 'AI Control',
      icon: Bot,
      targetInterface: 'enterpriseControlCenter' as ControlInterface,
      action: 'ai_config',
    },
    {
      title: 'Security Audit Logs',
      category: 'Security Governance',
      icon: Shield,
      targetInterface: 'enterpriseControlCenter' as ControlInterface,
    },
    {
      title: 'User Accounts & Roles (RBAC)',
      category: 'Security Governance',
      icon: Users,
      targetInterface: 'enterpriseControlCenter' as ControlInterface,
    },
    {
      title: 'Flush Cache (Redis & Memory)',
      category: 'Operations',
      icon: Trash2,
      targetInterface: 'operationsConsole' as ControlInterface,
      action: 'flush_cache',
    },
    {
      title: 'Reindex Search Engine (SAL)',
      category: 'Operations',
      icon: RefreshCw,
      targetInterface: 'operationsConsole' as ControlInterface,
      action: 'reindex_search',
    },
    {
      title: 'Ingest Election Data (ETL)',
      category: 'Operations Console',
      icon: Upload,
      targetInterface: 'operationsConsole' as ControlInterface,
    },
    {
      title: 'Automated Storage Checksum Validation',
      category: 'Operations & Storage',
      icon: ShieldCheck,
      targetInterface: 'operationsConsole' as ControlInterface,
      action: 'validate_checksums',
    },
    {
      title: 'Executive KPIs & Turnout Analytics',
      category: 'Executive Command',
      icon: BarChart,
      targetInterface: 'executiveCommandCenter' as ControlInterface,
    },
    {
      title: 'Public Portal Information',
      category: 'Public Portal',
      icon: Globe,
      targetInterface: 'publicPortal' as ControlInterface,
    },
  ];

  const filtered = commands.filter((cmd) => {
    const q = filter.toLowerCase().trim();
    return (
      cmd.title.toLowerCase().includes(q) ||
      cmd.category.toLowerCase().includes(q)
    );
  });

  const handleCommandClick = (cmd: (typeof commands)[0]) => {
    onSelectInterface(cmd.targetInterface);
    if (cmd.action) {
      onTriggerAction(cmd.action);
    }
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/35 dark:bg-black/60 backdrop-blur-md flex items-start justify-center pt-24 p-4">
      <div className="bg-white/90 dark:bg-[#1e1e1e]/90 backdrop-blur-3xl border border-black/[0.1] dark:border-white/[0.14] rounded-2xl w-full max-w-xl shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-150 transition-colors">
        {/* Spotlight Search Bar */}
        <div className="relative flex items-center px-4 py-3.5 border-b border-black/[0.06] dark:border-white/[0.08]">
          <Search className="w-5 h-5 text-[#86868b] dark:text-[#a1a1a6] shrink-0 mr-3" />
          <input
            type="text"
            autoFocus
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            placeholder="Spotlight Search commands, telemetry & modules..."
            className="w-full bg-transparent text-[15px] text-[#1d1d1f] dark:text-[#f5f5f7] placeholder-[#86868b] dark:placeholder-[#6e6e73] focus:outline-none"
          />
          <button
            type="button"
            onClick={onClose}
            className="p-1 rounded-lg text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7] hover:bg-black/[0.04] dark:hover:bg-white/[0.08] transition"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Command List */}
        <div className="max-h-80 overflow-y-auto p-2 space-y-0.5">
          {filtered.length === 0 ? (
            <div className="py-12 text-center text-[13px] text-[#86868b] dark:text-[#a1a1a6]">
              No matching modules or actions found.
            </div>
          ) : (
            filtered.map((cmd) => {
              const Icon = cmd.icon;
              return (
                <button
                  key={cmd.title}
                  type="button"
                  onClick={() => handleCommandClick(cmd)}
                  className="w-full px-3 py-2.5 rounded-xl hover:bg-black/[0.04] dark:hover:bg-white/[0.07] active:bg-[#0071e3] group transition-all flex items-center justify-between text-left cursor-pointer"
                >
                  <span className="flex items-center gap-3">
                    <span className="w-8 h-8 rounded-lg bg-black/[0.04] dark:bg-white/[0.08] group-hover:bg-[#0071e3]/10 dark:group-hover:bg-[#2997ff]/20 text-[#0071e3] dark:text-[#2997ff] flex items-center justify-center transition-colors">
                      <Icon className="w-4 h-4" />
                    </span>
                    <span className="block">
                      <span className="text-[13px] font-medium text-[#1d1d1f] dark:text-[#f5f5f7] group-hover:text-[#0071e3] dark:group-hover:text-[#2997ff] transition-colors block">
                        {cmd.title}
                      </span>
                      <span className="text-[11px] text-[#86868b] dark:text-[#a1a1a6] block">
                        {cmd.category}
                      </span>
                    </span>
                  </span>
                  <ArrowRight className="w-3.5 h-3.5 text-[#86868b] group-hover:text-[#1d1d1f] dark:group-hover:text-white group-hover:translate-x-0.5 transition-all shrink-0" />
                </button>
              );
            })
          )}
        </div>

        {/* Footer info */}
        <div className="px-4 py-2 bg-black/[0.02] dark:bg-white/[0.03] border-t border-black/[0.06] dark:border-white/[0.08] flex items-center justify-between text-[11px] text-[#86868b] dark:text-[#a1a1a6]">
          <span className="flex items-center gap-2">
            <span>National Election Command Pipeline</span>
          </span>
          <span className="flex items-center gap-2 font-mono text-[10px]">
            <span className="px-1.5 py-0.5 rounded bg-black/[0.05] dark:bg-white/[0.08]">⌘K</span>
            <span className="px-1.5 py-0.5 rounded bg-black/[0.05] dark:bg-white/[0.08]">esc</span>
          </span>
        </div>
      </div>
    </div>
  );
}
