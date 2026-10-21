'use client';

import React from 'react';
import {
  Search,
  Bell,
  Sparkles,
  Menu,
  Sun,
  Moon,
  Volume2,
  VolumeX,
} from 'lucide-react';
import { ControlInterface } from '@/lib/types';
import { getVoiceOverState, toggleVoiceOverState, subscribeVoiceOver } from '@/lib/voiceOver';
import { ConnectionStatusIndicator } from './ConnectionStatusIndicator';

interface HeaderProps {
  currentInterface: ControlInterface;
  onOpenCommandPalette: () => void;
  onOpenAIAssistant: () => void;
  onOpenNotifications: () => void;
  unreadCount?: number;
  onToggleMobileSidebar?: () => void;
  theme: 'dark' | 'light';
  onToggleTheme: () => void;
}

export function Header({
  currentInterface,
  onOpenCommandPalette,
  onOpenAIAssistant,
  onOpenNotifications,
  unreadCount = 3,
  onToggleMobileSidebar,
  theme,
  onToggleTheme,
}: HeaderProps) {
  const titles: Record<ControlInterface, { title: string; category: string }> = {
    enterpriseControlCenter: {
      title: 'Enterprise Control Center',
      category: 'Infrastructure & Governance',
    },
    executiveCommandCenter: {
      title: 'Executive Command Center',
      category: 'National KPIs & Analytics',
    },
    operationsConsole: {
      title: 'Operations Console',
      category: 'Election Management & ETL',
    },
    publicPortal: {
      title: 'Public Portal',
      category: 'Citizen Data & Transparency',
    },
  };

  const current = titles[currentInterface];

  const [voiceOverEnabled, setVoiceOverEnabled] = React.useState(false);

  React.useEffect(() => {
    setVoiceOverEnabled(getVoiceOverState());
    return subscribeVoiceOver((enabled) => setVoiceOverEnabled(enabled));
  }, []);

  const handleToggleVoiceOver = () => {
    const next = toggleVoiceOverState();
    setVoiceOverEnabled(next);
  };

  return (
    <header className="h-14 px-6 bg-white/70 dark:bg-[#161617]/70 backdrop-blur-2xl border-b border-black/[0.08] dark:border-white/[0.08] flex items-center justify-between sticky top-0 z-30 transition-colors">
      {/* Mobile menu toggle & Breadcrumbs */}
      <div className="flex items-center gap-3">
        {onToggleMobileSidebar && (
          <button
            onClick={onToggleMobileSidebar}
            className="md:hidden p-1.5 rounded-lg text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7] hover:bg-black/[0.05] dark:hover:bg-white/[0.08] transition-colors"
            aria-label="Toggle menu"
          >
            <Menu className="w-4 h-4" />
          </button>
        )}
        <div className="flex items-center gap-2.5">
          <h2 className="text-[15px] font-semibold text-[#1d1d1f] dark:text-[#f5f5f7] tracking-tight">
            {current.title}
          </h2>
          <span className="text-black/20 dark:text-white/20 text-xs">/</span>
          <span className="text-[12px] font-medium text-[#86868b] dark:text-[#a1a1a6] hidden sm:inline">
            {current.category}
          </span>
        </div>
      </div>

      {/* Middle & Right Actions */}
      <div className="flex items-center gap-2 sm:gap-2.5">
        {/* Quick Search & Commands (macOS Spotlight style) */}
        <button
          onClick={onOpenCommandPalette}
          className="hidden sm:flex items-center gap-2.5 px-3 py-1.5 rounded-xl bg-black/[0.04] dark:bg-white/[0.06] hover:bg-black/[0.07] dark:hover:bg-white/[0.1] text-[#86868b] dark:text-[#a1a1a6] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7] transition-all cursor-pointer"
        >
          <Search className="w-3.5 h-3.5 text-[#86868b]" />
          <span className="text-[12px] font-normal">Search &amp; Commands</span>
          <kbd className="px-1.5 py-0.5 text-[10px] font-medium bg-black/[0.06] dark:bg-white/[0.1] text-[#1d1d1f] dark:text-[#f5f5f7] rounded-md tracking-wider">
            ⌘K
          </kbd>
        </button>

        {/* Backend Connection Status Tracker (Heartbeat & WebSocket with subtle Offline state) */}
        <ConnectionStatusIndicator />

        {/* Voice-over Audio Updates Toggle (Web Speech API) */}
        <button
          type="button"
          onClick={handleToggleVoiceOver}
          aria-label={voiceOverEnabled ? 'Voice-over audio updates enabled' : 'Voice-over audio updates disabled'}
          aria-pressed={voiceOverEnabled}
          title={voiceOverEnabled ? 'Voice-over: Enabled (Web Speech updates for ETL & alerts)' : 'Voice-over: Disabled (Click to enable audio status updates)'}
          className={`p-2 rounded-xl transition-all cursor-pointer active:scale-95 flex items-center gap-1.5 ${
            voiceOverEnabled
              ? 'text-[#0071e3] dark:text-[#2997ff] bg-[#0071e3]/10 dark:bg-[#2997ff]/15 ring-1 ring-[#0071e3]/30'
              : 'text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7] hover:bg-black/[0.05] dark:hover:bg-white/[0.08]'
          }`}
        >
          {voiceOverEnabled ? (
            <>
              <Volume2 className="w-4 h-4 animate-pulse" />
              <span className="text-[11px] font-semibold hidden xl:inline">Voice-over</span>
            </>
          ) : (
            <VolumeX className="w-4 h-4" />
          )}
        </button>

        {/* Theme Toggle (Apple style control) */}
        <button
          type="button"
          onClick={onToggleTheme}
          aria-label={theme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
          className="p-2 rounded-xl text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7] hover:bg-black/[0.05] dark:hover:bg-white/[0.08] transition-all cursor-pointer active:scale-95"
          title={theme === 'dark' ? 'Light Mode' : 'Dark Mode'}
        >
          {theme === 'dark' ? (
            <Sun className="w-4 h-4 text-[#ff9f0a] transition-transform duration-200" />
          ) : (
            <Moon className="w-4 h-4 text-[#0071e3] transition-transform duration-200" />
          )}
        </button>

        {/* AI Intelligence Assistant (Apple Intelligence subtle shimmer button) */}
        <button
          type="button"
          onClick={onOpenAIAssistant}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-[#0071e3] hover:bg-[#0077ed] dark:bg-[#2997ff] dark:hover:bg-[#47a6ff] text-white text-[12px] font-medium shadow-sm transition-all cursor-pointer active:scale-95"
        >
          <Sparkles className="w-3.5 h-3.5" />
          <span>Intelligence</span>
        </button>

        {/* Notifications Icon with Badge (iOS style badge) */}
        <button
          type="button"
          onClick={onOpenNotifications}
          className="relative p-2 rounded-xl text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7] hover:bg-black/[0.05] dark:hover:bg-white/[0.08] transition-all cursor-pointer active:scale-95"
          aria-label="View notifications"
        >
          <Bell className="w-4 h-4" />
          {unreadCount > 0 && (
            <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-[#ff3b30] ring-2 ring-white dark:ring-[#161617]" />
          )}
        </button>
      </div>
    </header>
  );
}
