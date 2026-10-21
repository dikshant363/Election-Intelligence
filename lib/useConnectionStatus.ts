'use client';

import { useState, useEffect, useRef, useCallback } from 'react';
import { announceCriticalAlert, announceOperation } from '@/lib/voiceOver';

export type ConnectionStatus = 'connected' | 'reconnecting' | 'offline';

export interface ConnectionState {
  status: ConnectionStatus;
  latencyMs: number | null;
  lastHeartbeat: Date | null;
  isSimulatedOffline: boolean;
  retryCount: number;
}

const HEARTBEAT_INTERVAL_MS = 8000;
const HEARTBEAT_TIMEOUT_MS = 3500;

export function useConnectionStatus() {
  const [connection, setConnection] = useState<ConnectionState>({
    status: 'connected',
    latencyMs: 24,
    lastHeartbeat: new Date(),
    isSimulatedOffline: false,
    retryCount: 0,
  });

  const isSimulatedOfflineRef = useRef(false);
  const prevStatusRef = useRef<ConnectionStatus>('connected');

  const checkHeartbeat = useCallback(async () => {
    if (isSimulatedOfflineRef.current) {
      setConnection((prev) => ({
        ...prev,
        status: 'offline',
        latencyMs: null,
      }));
      return;
    }

    if (typeof navigator !== 'undefined' && !navigator.onLine) {
      setConnection((prev) => ({
        ...prev,
        status: 'offline',
        latencyMs: null,
        retryCount: prev.retryCount + 1,
      }));
      return;
    }

    const startTime = performance.now();
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), HEARTBEAT_TIMEOUT_MS);

    try {
      const response = await fetch('/api/v1/health', {
        method: 'GET',
        cache: 'no-store',
        signal: controller.signal,
      });

      clearTimeout(timeoutId);
      const elapsed = Math.round(performance.now() - startTime);

      if (response.ok) {
        setConnection({
          status: 'connected',
          latencyMs: elapsed,
          lastHeartbeat: new Date(),
          isSimulatedOffline: false,
          retryCount: 0,
        });

        if (prevStatusRef.current === 'offline') {
          announceOperation('Backend services connection restored. Heartbeat active.');
        }
        prevStatusRef.current = 'connected';
      } else {
        throw new Error(`HTTP error ${response.status}`);
      }
    } catch (err) {
      clearTimeout(timeoutId);

      setConnection((prev) => {
        const nextRetry = prev.retryCount + 1;
        const newStatus: ConnectionStatus = nextRetry >= 2 ? 'offline' : 'reconnecting';

        if (newStatus === 'offline' && prevStatusRef.current !== 'offline') {
          announceCriticalAlert('Backend connection lost. Heartbeat failed.', 'warning');
        }
        prevStatusRef.current = newStatus;

        return {
          ...prev,
          status: newStatus,
          latencyMs: null,
          retryCount: nextRetry,
        };
      });
    }
  }, []);

  const toggleSimulateOffline = useCallback(() => {
    const next = !isSimulatedOfflineRef.current;
    isSimulatedOfflineRef.current = next;

    setConnection((prev) => {
      const newStatus: ConnectionStatus = next ? 'offline' : 'connected';
      if (newStatus === 'offline') {
        announceCriticalAlert('Simulated backend heartbeat failure. System is now offline.', 'warning');
      } else {
        announceOperation('Reconnected to backend services.');
      }
      prevStatusRef.current = newStatus;
      return {
        ...prev,
        isSimulatedOffline: next,
        status: newStatus,
        latencyMs: next ? null : 22,
        lastHeartbeat: next ? prev.lastHeartbeat : new Date(),
      };
    });

    if (!next) {
      checkHeartbeat();
    }
  }, [checkHeartbeat]);

  useEffect(() => {
    // Initial check
    checkHeartbeat();

    // Heartbeat polling loop
    const intervalId = setInterval(checkHeartbeat, HEARTBEAT_INTERVAL_MS);

    // Browser online/offline event handlers
    const handleOnline = () => {
      if (!isSimulatedOfflineRef.current) {
        checkHeartbeat();
      }
    };

    const handleOffline = () => {
      setConnection((prev) => ({
        ...prev,
        status: 'offline',
        latencyMs: null,
      }));
      announceCriticalAlert('Network connectivity lost. Operating in offline mode.', 'warning');
    };

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      clearInterval(intervalId);
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, [checkHeartbeat]);

  return {
    ...connection,
    reconnect: checkHeartbeat,
    toggleSimulateOffline,
  };
}
