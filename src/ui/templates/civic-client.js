// Election Intelligence Platform - Civic Client Interaction Engine
// Implements Apple HIG interactions: Command Palette (⌘K), Grounded AI Assistant (⌘J), Theme Toggle, and Live Search

(function () {
  'use strict';

  // 1. Theme Management (Dark / Light)
  function initTheme() {
    const savedTheme = localStorage.getItem('civic_theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }

    document.querySelectorAll('button[aria-label="Theme toggle"], button:has(.material-symbols-outlined:contains("mode"))').forEach(btn => {
      btn.addEventListener('click', () => {
        const isDark = document.documentElement.classList.toggle('dark');
        localStorage.setItem('civic_theme', isDark ? 'dark' : 'light');
        const icon = btn.querySelector('.material-symbols-outlined');
        if (icon) {
          icon.textContent = isDark ? 'dark_mode' : 'light_mode';
        }
      });
    });
  }

  // 2. Command Palette (⌘K) & Search
  function createCommandPalette() {
    if (document.getElementById('civic-command-palette')) return;

    const overlay = document.createElement('div');
    overlay.id = 'civic-command-palette';
    overlay.style.display = 'none';
    overlay.className = 'fixed inset-0 z-50 bg-black/60 backdrop-blur-md flex items-start justify-center pt-20 px-4 animate-in fade-in duration-150';
    overlay.innerHTML = `
      <div class="bg-surface-card dark:bg-[#1c1c1e] w-full max-w-2xl rounded-2xl shadow-2xl border border-black/[0.08] dark:border-white/[0.12] overflow-hidden flex flex-col max-h-[80vh]">
        <div class="flex items-center px-4 py-3 border-b border-border-subtle dark:border-white/[0.08] gap-3">
          <span class="material-symbols-outlined text-outline">search</span>
          <input id="civic-palette-input" type="text" placeholder="Search elections, candidates, constituencies, affidavits..." class="w-full bg-transparent font-body-md text-on-surface dark:text-[#f5f5f7] placeholder:text-outline focus:outline-none text-base" />
          <kbd class="px-2 py-0.5 rounded text-xs bg-surface-subtle dark:bg-[#2c2c2e] text-archive-slate font-mono font-medium">ESC</kbd>
        </div>
        <div id="civic-palette-results" class="p-3 overflow-y-auto divide-y divide-border-subtle/50 dark:divide-white/[0.04]">
          <div class="p-6 text-center text-sm text-archive-slate">Type at least 2 characters to search across verified election records.</div>
        </div>
        <div class="px-4 py-2.5 bg-surface-subtle dark:bg-[#2c2c2e]/50 border-t border-border-subtle dark:border-white/[0.08] flex items-center justify-between text-xs text-archive-slate">
          <div class="flex items-center gap-3">
            <span><kbd class="font-mono bg-surface-card dark:bg-[#1c1c1e] px-1 rounded">↑↓</kbd> Navigate</span>
            <span><kbd class="font-mono bg-surface-card dark:bg-[#1c1c1e] px-1 rounded">↵</kbd> Select</span>
          </div>
          <span class="text-[11px] font-medium text-status-verified flex items-center gap-1"><span class="w-1.5 h-1.5 rounded-full bg-status-verified"></span> Verified BM25 Index</span>
        </div>
      </div>
    `;

    document.body.appendChild(overlay);

    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) closePalette();
    });

    const input = document.getElementById('civic-palette-input');
    let debounceTimer;

    input.addEventListener('input', (e) => {
      clearTimeout(debounceTimer);
      const query = e.target.value.trim();
      if (query.length < 2) {
        document.getElementById('civic-palette-results').innerHTML = `
          <div class="p-6 text-center text-sm text-archive-slate">Type at least 2 characters to search across verified election records.</div>
        `;
        return;
      }
      debounceTimer = setTimeout(() => executeSearch(query), 150);
    });

    input.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') closePalette();
    });
  }

  async function executeSearch(query) {
    const resultsContainer = document.getElementById('civic-palette-results');
    resultsContainer.innerHTML = `<div class="p-4 text-center text-sm text-archive-slate animate-pulse">Querying BM25 in-process index...</div>`;

    try {
      const res = await fetch(`/api/v1/search?q=${encodeURIComponent(query)}`);
      const json = await res.json();
      if (!json.success || !json.data.results || json.data.results.length === 0) {
        resultsContainer.innerHTML = `
          <div class="p-6 text-center text-sm text-archive-slate">No verified electoral records found for "${query}".</div>
        `;
        return;
      }

      resultsContainer.innerHTML = json.data.results.map(r => `
        <a href="${getTargetUrl(r)}" class="block p-3 rounded-xl hover:bg-surface-subtle dark:hover:bg-white/[0.04] transition-colors group">
          <div class="flex items-center justify-between">
            <span class="font-semibold text-sm text-primary dark:text-[#5e9eff] group-hover:underline">${escapeHtml(r.title)}</span>
            <span class="text-[10px] uppercase font-mono px-2 py-0.5 rounded-full bg-primary-fixed/30 dark:bg-primary-container text-primary dark:text-primary-fixed font-bold">${escapeHtml(r.category)}</span>
          </div>
          <p class="text-xs text-on-surface-variant dark:text-[#a1a1a6] mt-1 line-clamp-2">${escapeHtml(r.description)}</p>
          <div class="flex items-center gap-3 mt-1.5 text-[10px] text-archive-slate font-mono">
            <span>Score: ${r.score.toFixed(2)}</span>
            <span>ID: ${escapeHtml(r.id)}</span>
          </div>
        </a>
      `).join('');
    } catch (err) {
      resultsContainer.innerHTML = `<div class="p-4 text-center text-xs text-error">Error connecting to search service: ${err.message}</div>`;
    }
  }

  function getTargetUrl(item) {
    if (item.category === 'candidate') return `/candidates?id=${item.id}`;
    if (item.category === 'constituency') return `/constituencies?id=${item.id}`;
    if (item.category === 'party') return `/candidates?party=${item.id}`;
    return `/#${item.id}`;
  }

  function openPalette() {
    createCommandPalette();
    const overlay = document.getElementById('civic-command-palette');
    overlay.style.display = 'flex';
    const input = document.getElementById('civic-palette-input');
    input.focus();
    input.select();
  }

  function closePalette() {
    const overlay = document.getElementById('civic-command-palette');
    if (overlay) overlay.style.display = 'none';
  }

  // 3. Grounded AI Query Interactivity
  function initAiForms() {
    const aiInputs = document.querySelectorAll('input[placeholder*="Ask"], input[placeholder*="research question"], textarea[placeholder*="Ask"]');
    aiInputs.forEach(input => {
      const parent = input.closest('form') || input.parentElement;
      const submitBtn = parent.querySelector('button[type="submit"], button:has(.material-symbols-outlined)');
      
      const runQuery = async () => {
        const q = input.value.trim();
        if (!q) return;

        // Find or create response container
        let resContainer = document.getElementById('ai-response-stream');
        if (!resContainer) {
          resContainer = document.createElement('div');
          resContainer.id = 'ai-response-stream';
          resContainer.className = 'mt-6 p-6 rounded-2xl bg-surface-card dark:bg-[#1e1e1e] border border-border-subtle dark:border-white/[0.08] shadow-sm';
          input.closest('.max-w-4xl, .max-w-3xl, main')?.appendChild(resContainer);
        }

        resContainer.innerHTML = `
          <div class="flex items-center gap-3 text-sm text-primary dark:text-[#5e9eff]">
            <span class="w-4 h-4 border-2 border-primary border-t-transparent rounded-full animate-spin"></span>
            <span>Retrieving statutory Form 26 evidence passages and ECI declarations...</span>
          </div>
        `;

        try {
          const res = await fetch('/api/v1/ai/query', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: q, session_id: 'web-session-' + Date.now() })
          });
          const data = await res.json();
          if (data.success && data.data) {
            renderAiAnswer(resContainer, data.data);
          } else {
            resContainer.innerHTML = `<div class="text-sm text-error">Query failed: ${data.error?.message || 'Unknown error'}</div>`;
          }
        } catch (e) {
          resContainer.innerHTML = `<div class="text-sm text-error">Connection error: ${e.message}</div>`;
        }
      };

      if (submitBtn) {
        submitBtn.addEventListener('click', (e) => {
          e.preventDefault();
          runQuery();
        });
      }

      input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          runQuery();
        }
      });
    });
  }

  function renderAiAnswer(container, aiData) {
    const citationsHtml = aiData.citations.map(c => `
      <div class="p-3.5 rounded-xl bg-surface-subtle dark:bg-white/[0.04] border border-border-subtle dark:border-white/[0.08] text-xs">
        <div class="flex items-center justify-between mb-1.5">
          <span class="font-semibold text-primary dark:text-[#5e9eff] flex items-center gap-1.5">
            <span class="material-symbols-outlined text-[14px]">verified</span>
            ${escapeHtml(c.publisher)}
          </span>
          <span class="font-mono text-[10px] text-archive-slate">${escapeHtml(c.section)}</span>
        </div>
        <p class="text-on-surface-variant dark:text-[#d1d1d6] italic mb-2">"${escapeHtml(c.quote)}"</p>
        <a href="${escapeHtml(c.url)}" target="_blank" rel="noopener noreferrer" class="text-[11px] text-secondary dark:text-[#64d2ff] hover:underline flex items-center gap-1">
          <span>Official Gazette Filing</span>
          <span class="material-symbols-outlined text-[12px]">open_in_new</span>
        </a>
      </div>
    `).join('');

    container.innerHTML = `
      <div class="space-y-4">
        <div class="flex items-center justify-between pb-3 border-b border-border-subtle dark:border-white/[0.08]">
          <div class="flex items-center gap-2 text-xs font-semibold text-status-verified">
            <span class="w-2 h-2 rounded-full bg-status-verified"></span>
            <span>Grounded Response (Verification Score: ${(aiData.grounding_score * 100).toFixed(1)}%)</span>
          </div>
          <span class="text-[10px] font-mono text-archive-slate">${escapeHtml(aiData.model_used)}</span>
        </div>

        <div class="font-body-md text-on-surface dark:text-[#f5f5f7] leading-relaxed whitespace-pre-line text-sm">
          ${escapeHtml(aiData.answer)}
        </div>

        ${aiData.citations.length > 0 ? `
          <div class="pt-3 border-t border-border-subtle dark:border-white/[0.08]">
            <h4 class="text-xs font-semibold text-archive-slate uppercase tracking-wider mb-2.5">Statutory Citations (${aiData.citations.length})</h4>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-2.5">
              ${citationsHtml}
            </div>
          </div>
        ` : ''}

        <div class="p-3 rounded-lg bg-surface-subtle dark:bg-white/[0.03] text-[11px] text-archive-slate leading-normal">
          <strong>Non-Partisan Charter Guarantee:</strong> ${escapeHtml(aiData.disclaimer)}
        </div>
      </div>
    `;
  }

  // 4. Global Keyboard Shortcuts
  function initKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
      // ⌘K or Ctrl+K for Search
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        openPalette();
      }
      // ⌘J or Ctrl+J for AI Assistant
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'j') {
        e.preventDefault();
        window.location.href = '/ai';
      }
      // ESC closes open palette or modals
      if (e.key === 'Escape') {
        closePalette();
      }
    });

    // Wire up on-page search inputs to open palette or search directly
    document.querySelectorAll('input[placeholder*="Search elections"]').forEach(input => {
      input.addEventListener('focus', () => {
        openPalette();
      });
    });
  }

  function escapeHtml(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  // DOM Ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      initTheme();
      initKeyboardShortcuts();
      initAiForms();
    });
  } else {
    initTheme();
    initKeyboardShortcuts();
    initAiForms();
  }
})();
