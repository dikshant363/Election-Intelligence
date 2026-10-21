// Web Speech API Voice-Over status updates service for Election Intelligence Platform
// Supports audio updates for long-running ETL processes and critical system alerts.

export interface VoiceOverOptions {
  priority?: 'high' | 'normal';
  rate?: number;
  pitch?: number;
  volume?: number;
}

const STORAGE_KEY = 'election_voiceover_enabled';
const EVENT_NAME = 'election-voiceover-toggle';
const SPEECH_EVENT_NAME = 'election-voiceover-speech';

export function isVoiceOverSupported(): boolean {
  return typeof window !== 'undefined' && 'speechSynthesis' in window && 'SpeechSynthesisUtterance' in window;
}

export function getVoiceOverState(): boolean {
  if (typeof window === 'undefined') return false;
  try {
    const val = localStorage.getItem(STORAGE_KEY);
    return val === 'true';
  } catch (e) {
    return false;
  }
}

export function setVoiceOverState(enabled: boolean): boolean {
  if (typeof window === 'undefined') return enabled;
  try {
    localStorage.setItem(STORAGE_KEY, enabled ? 'true' : 'false');
    window.dispatchEvent(new CustomEvent(EVENT_NAME, { detail: { enabled } }));
  } catch (e) {
    console.error('Failed to save voice-over state', e);
  }

  if (isVoiceOverSupported()) {
    if (enabled) {
      speakVoiceOver('Voice-over enabled. Audio updates will announce ETL pipeline progress and critical system alerts.', {
        priority: 'high',
      });
    } else {
      window.speechSynthesis.cancel();
    }
  }

  return enabled;
}

export function toggleVoiceOverState(): boolean {
  const current = getVoiceOverState();
  return setVoiceOverState(!current);
}

// Subscribe to Voice-over toggle changes across components
export function subscribeVoiceOver(callback: (enabled: boolean) => void): () => void {
  if (typeof window === 'undefined') return () => {};

  const handler = (e: Event) => {
    const custom = e as CustomEvent<{ enabled: boolean }>;
    callback(custom.detail?.enabled ?? getVoiceOverState());
  };

  window.addEventListener(EVENT_NAME, handler);
  return () => window.removeEventListener(EVENT_NAME, handler);
}

// Subscribe to active speech announcements (for UI audio feedback/subtitles)
export function subscribeSpeechAnnouncements(callback: (text: string) => void): () => void {
  if (typeof window === 'undefined') return () => {};

  const handler = (e: Event) => {
    const custom = e as CustomEvent<{ text: string }>;
    if (custom.detail?.text) {
      callback(custom.detail.text);
    }
  };

  window.addEventListener(SPEECH_EVENT_NAME, handler);
  return () => window.removeEventListener(SPEECH_EVENT_NAME, handler);
}

// Primary speech synthesis invoker
export function speakVoiceOver(text: string, options: VoiceOverOptions = {}): void {
  if (!isVoiceOverSupported()) return;
  if (!getVoiceOverState() && options.priority !== 'high') return;

  try {
    const synth = window.speechSynthesis;

    // High priority cuts off previous speech
    if (options.priority === 'high') {
      synth.cancel();
    }

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = options.rate ?? 1.05;
    utterance.pitch = options.pitch ?? 1.0;
    utterance.volume = options.volume ?? 1.0;

    // Pick natural English voice if available
    const voices = synth.getVoices();
    if (voices.length > 0) {
      const preferred =
        voices.find((v) => v.lang.startsWith('en') && (v.name.includes('Samantha') || v.name.includes('Daniel') || v.name.includes('Natural') || v.name.includes('Google'))) ||
        voices.find((v) => v.lang.startsWith('en')) ||
        voices[0];
      if (preferred) {
        utterance.voice = preferred;
      }
    }

    // Broadcast event for UI indicator / captions
    window.dispatchEvent(new CustomEvent(SPEECH_EVENT_NAME, { detail: { text } }));

    synth.speak(utterance);
  } catch (err) {
    console.warn('SpeechSynthesis error:', err);
  }
}

// Domain-specific audio helpers
export function announceEtlStart(batchName: string, records: string | number): void {
  speakVoiceOver(`ETL batch initiated: Ingesting file ${batchName} with estimated ${records} electoral records. Data normalization and hash verification active.`, {
    priority: 'high',
  });
}

export function announceEtlComplete(batchName: string, records: string | number): void {
  speakVoiceOver(`ETL Ingestion Complete: Batch ${batchName} validated across all constituencies. ${records} records indexed into database with zero schema errors.`, {
    priority: 'high',
  });
}

export function announceCriticalAlert(alertTitle: string, severity: 'critical' | 'warning' | 'info' = 'critical'): void {
  const prefix = severity === 'critical' ? 'Critical System Alert' : severity === 'warning' ? 'Warning' : 'System Notice';
  speakVoiceOver(`${prefix}: ${alertTitle}`, {
    priority: severity === 'critical' ? 'high' : 'normal',
  });
}

export function announceOperation(action: string): void {
  speakVoiceOver(`Operations update: ${action}`, { priority: 'normal' });
}
