'use client';

import React from 'react';
import { Bell, X, CheckCircle2, AlertTriangle, Info } from 'lucide-react';

interface NotificationItem {
  id: string;
  title: string;
  message: string;
  time: string;
  type: 'success' | 'warning' | 'info';
  read: boolean;
}

interface NotificationsModalProps {
  isOpen: boolean;
  onClose: () => void;
  notifications: NotificationItem[];
  onMarkAllAsRead: () => void;
}

export function NotificationsModal({
  isOpen,
  onClose,
  notifications,
  onMarkAllAsRead,
}: NotificationsModalProps) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 bg-black/35 dark:bg-black/60 backdrop-blur-md flex items-start justify-center pt-24 p-4">
      <div className="bg-white/90 dark:bg-[#1e1e1e]/90 backdrop-blur-3xl border border-black/[0.08] dark:border-white/[0.12] rounded-2xl w-full max-w-md shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-150 transition-colors">
        <div className="px-5 py-3.5 border-b border-black/[0.06] dark:border-white/[0.08] flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Bell className="w-4 h-4 text-[#0071e3] dark:text-[#2997ff]" />
            <h3 className="text-[14px] font-semibold text-[#1d1d1f] dark:text-[#f5f5f7]">Notifications</h3>
          </div>
          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={onMarkAllAsRead}
              className="text-[12px] text-[#0071e3] dark:text-[#2997ff] hover:opacity-80 font-medium cursor-pointer transition"
            >
              Mark all read
            </button>
            <button
              type="button"
              onClick={onClose}
              className="p-1 rounded-lg text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7] hover:bg-black/[0.04] dark:hover:bg-white/[0.08] transition"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>

        <div className="max-h-80 overflow-y-auto p-2 space-y-1.5">
          {notifications.map((n) => (
            <div
              key={n.id}
              className={`p-3 rounded-xl border transition-all flex items-start gap-3 ${
                n.read
                  ? 'opacity-60 bg-transparent border-transparent'
                  : 'bg-black/[0.02] dark:bg-white/[0.04] border-black/[0.04] dark:border-white/[0.06]'
              }`}
            >
              <div
                className={`w-6 h-6 rounded-lg shrink-0 mt-0.5 flex items-center justify-center ${
                  n.type === 'success'
                    ? 'bg-[#34c759]/10 text-[#34c759]'
                    : n.type === 'warning'
                    ? 'bg-[#ff9500]/10 text-[#ff9500]'
                    : 'bg-[#0071e3]/10 text-[#0071e3]'
                }`}
              >
                {n.type === 'success' ? (
                  <CheckCircle2 className="w-3.5 h-3.5" />
                ) : n.type === 'warning' ? (
                  <AlertTriangle className="w-3.5 h-3.5" />
                ) : (
                  <Info className="w-3.5 h-3.5" />
                )}
              </div>
              <div className="flex-1 min-w-0">
                <div className="text-[13px] font-medium text-[#1d1d1f] dark:text-[#f5f5f7] flex items-center justify-between">
                  <span>{n.title}</span>
                  <span className="text-[11px] text-[#86868b] font-normal">{n.time}</span>
                </div>
                <p className="text-[12px] text-[#86868b] dark:text-[#a1a1a6] mt-0.5 leading-snug">{n.message}</p>
              </div>
            </div>
          ))}
        </div>

        <div className="px-4 py-2.5 bg-black/[0.02] dark:bg-white/[0.03] border-t border-black/[0.06] dark:border-white/[0.08] text-center">
          <span className="text-[11px] text-[#86868b]">
            Real-time event bus subscriptions active
          </span>
        </div>
      </div>
    </div>
  );
}
