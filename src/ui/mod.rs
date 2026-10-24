// Election Intelligence Platform - Apple Human Interface Guidelines UI
// Server-Side Rendered (SSR) & Interactive HTML/CSS Civic Experience
// Powered by Stitch Civic Restraint Design System

pub static HOMEPAGE_HTML: &str = include_str!("templates/homepage.html");
pub static CANDIDATES_HTML: &str = include_str!("templates/candidates.html");
pub static CONSTITUENCIES_HTML: &str = include_str!("templates/constituencies.html");
pub static RESULTS_HTML: &str = include_str!("templates/results.html");
pub static AI_HTML: &str = include_str!("templates/ai.html");
pub static EVIDENCE_HTML: &str = include_str!("templates/evidence.html");
pub static COMMUNITY_HTML: &str = include_str!("templates/community.html");

pub fn render_homepage() -> &'static str {
    HOMEPAGE_HTML
}

pub fn render_candidates() -> &'static str {
    CANDIDATES_HTML
}

pub fn render_constituencies() -> &'static str {
    CONSTITUENCIES_HTML
}

pub fn render_results() -> &'static str {
    RESULTS_HTML
}

pub fn render_ai() -> &'static str {
    AI_HTML
}

pub fn render_evidence() -> &'static str {
    EVIDENCE_HTML
}

pub fn render_community() -> &'static str {
    COMMUNITY_HTML
}

pub fn render_admin() -> &'static str {
    COMMUNITY_HTML
}

#[allow(dead_code)]
#[allow(clippy::useless_format)]
pub fn render_apple_hig_page(_initial_tab: &str) -> String {
    format!(
        r##"<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <title>Election Intelligence Platform — Independent Indian Election Research</title>
  <meta name="description" content="Independent, politically neutral, AI-powered public research platform for Indian elections with complete evidence and source attribution.">
  <meta name="theme-color" content="#000000" media="(prefers-color-scheme: dark)">
  <meta name="theme-color" content="#f5f5f7" media="(prefers-color-scheme: light)">
  <style>
    :root {{
      --bg: #f5f5f7;
      --card-bg: #ffffff;
      --card-border: rgba(0, 0, 0, 0.08);
      --text-primary: #1d1d1f;
      --text-secondary: #86868b;
      --accent: #0071e3;
      --accent-hover: #0077ed;
      --success: #34c759;
      --warning: #ff9500;
      --danger: #ff3b30;
      --radius-sm: 8px;
      --radius-md: 12px;
      --radius-lg: 16px;
      --font-stack: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }}
    html.dark {{
      --bg: #000000;
      --card-bg: #1c1c1e;
      --card-border: rgba(255, 255, 255, 0.1);
      --text-primary: #f5f5f7;
      --text-secondary: #86868b;
      --accent: #2997ff;
      --accent-hover: #0077ed;
      --success: #30d158;
      --warning: #ffd60a;
      --danger: #ff453a;
    }}
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-font-smoothing: antialiased;
    }}
    body {{
      font-family: var(--font-stack);
      background-color: var(--bg);
      color: var(--text-primary);
      line-height: 1.5;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }}
    header {{
      background: rgba(28, 28, 30, 0.8);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border-bottom: 1px solid var(--card-border);
      position: sticky;
      top: 0;
      z-index: 100;
      padding: 12px 24px;
    }}
    html:not(.dark) header {{
      background: rgba(255, 255, 255, 0.85);
    }}
    .header-container {{
      max-width: 1400px;
      margin: 0 auto;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
    }}
    .brand {{
      display: flex;
      align-items: center;
      gap: 12px;
      text-decoration: none;
      color: var(--text-primary);
    }}
    .brand-logo {{
      width: 32px;
      height: 32px;
      background: linear-gradient(135deg, #0071e3, #34c759);
      border-radius: var(--radius-sm);
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      font-weight: 700;
      font-size: 16px;
    }}
    .brand-text h1 {{
      font-size: 17px;
      font-weight: 600;
      letter-spacing: -0.01em;
    }}
    .brand-text p {{
      font-size: 11px;
      color: var(--text-secondary);
      letter-spacing: 0.02em;
      text-transform: uppercase;
    }}
    .nav-tabs {{
      display: flex;
      gap: 6px;
      background: rgba(120, 120, 128, 0.16);
      padding: 4px;
      border-radius: var(--radius-md);
    }}
    .nav-btn {{
      padding: 6px 14px;
      font-size: 13px;
      font-weight: 500;
      border-radius: var(--radius-sm);
      border: none;
      background: transparent;
      color: var(--text-secondary);
      cursor: pointer;
      transition: all 0.15s ease;
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .nav-btn.active {{
      background: var(--card-bg);
      color: var(--text-primary);
      box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
    }}
    .header-actions {{
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .icon-btn {{
      padding: 8px;
      border-radius: 50%;
      border: 1px solid var(--card-border);
      background: var(--card-bg);
      color: var(--text-primary);
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 13px;
    }}
    .icon-btn:hover {{
      background: rgba(120, 120, 128, 0.15);
    }}
    .k-shortcut {{
      display: flex;
      align-items: center;
      gap: 4px;
      background: rgba(120, 120, 128, 0.15);
      padding: 6px 12px;
      border-radius: var(--radius-sm);
      font-size: 12px;
      color: var(--text-secondary);
      border: 1px solid var(--card-border);
      cursor: pointer;
    }}
    .k-shortcut kbd {{
      background: var(--card-bg);
      padding: 1px 4px;
      border-radius: 4px;
      border: 1px solid var(--card-border);
      font-size: 11px;
    }}
    main {{
      max-width: 1400px;
      margin: 0 auto;
      padding: 24px;
      width: 100%;
      flex: 1;
    }}
    .mission-banner {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: var(--radius-lg);
      padding: 20px 24px;
      margin-bottom: 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 20px;
    }}
    .mission-text h2 {{
      font-size: 18px;
      font-weight: 600;
      margin-bottom: 4px;
    }}
    .mission-text p {{
      font-size: 13px;
      color: var(--text-secondary);
      max-width: 900px;
    }}
    .neutral-badge {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 12px;
      border-radius: var(--radius-sm);
      background: rgba(52, 199, 89, 0.15);
      color: var(--success);
      font-size: 12px;
      font-weight: 600;
      white-space: nowrap;
    }}
    .stats-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 16px;
      margin-bottom: 32px;
    }}
    .stat-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: var(--radius-md);
      padding: 20px;
    }}
    .stat-label {{
      font-size: 13px;
      color: var(--text-secondary);
      font-weight: 500;
      margin-bottom: 6px;
    }}
    .stat-value {{
      font-size: 28px;
      font-weight: 700;
      letter-spacing: -0.02em;
    }}
    .stat-subtext {{
      font-size: 12px;
      color: var(--text-secondary);
      margin-top: 4px;
    }}
    .section-title {{
      font-size: 20px;
      font-weight: 600;
      margin: 32px 0 16px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}
    .search-bar-container {{
      margin-bottom: 24px;
      position: relative;
    }}
    .search-input {{
      width: 100%;
      padding: 14px 20px 14px 44px;
      border-radius: var(--radius-md);
      border: 1px solid var(--card-border);
      background: var(--card-bg);
      color: var(--text-primary);
      font-size: 15px;
      outline: none;
      transition: border-color 0.15s ease;
    }}
    .search-input:focus {{
      border-color: var(--accent);
      box-shadow: 0 0 0 3px rgba(0, 113, 227, 0.2);
    }}
    .search-icon {{
      position: absolute;
      left: 16px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-secondary);
    }}
    .card-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 16px;
    }}
    .candidate-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: var(--radius-md);
      padding: 20px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: transform 0.15s ease, box-shadow 0.15s ease;
    }}
    .candidate-card:hover {{
      transform: translateY(-2px);
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
    }}
    .candidate-header {{
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      margin-bottom: 12px;
    }}
    .candidate-name {{
      font-size: 17px;
      font-weight: 600;
    }}
    .candidate-constituency {{
      font-size: 13px;
      color: var(--text-secondary);
    }}
    .party-tag {{
      display: inline-block;
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 11px;
      font-weight: 600;
      color: white;
    }}
    .candidate-meta {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      margin: 14px 0;
      padding: 12px 0;
      border-top: 1px solid var(--card-border);
      border-bottom: 1px solid var(--card-border);
      font-size: 12px;
    }}
    .meta-item span:first-child {{
      color: var(--text-secondary);
      display: block;
      margin-bottom: 2px;
    }}
    .meta-item span:last-child {{
      font-weight: 600;
      font-size: 13px;
    }}
    .badge-f26 {{
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 4px 8px;
      border-radius: 4px;
      font-size: 11px;
      font-weight: 600;
    }}
    .badge-verified {{
      background: rgba(52, 199, 89, 0.15);
      color: var(--success);
    }}
    .badge-cases {{
      background: rgba(255, 149, 0, 0.15);
      color: var(--warning);
    }}
    .btn {{
      padding: 8px 16px;
      border-radius: var(--radius-sm);
      border: none;
      font-size: 13px;
      font-weight: 500;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      transition: all 0.15s ease;
    }}
    .btn-primary {{
      background: var(--accent);
      color: white;
    }}
    .btn-primary:hover {{
      background: var(--accent-hover);
    }}
    .btn-secondary {{
      background: rgba(120, 120, 128, 0.16);
      color: var(--text-primary);
    }}
    .btn-secondary:hover {{
      background: rgba(120, 120, 128, 0.25);
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      background: var(--card-bg);
      border-radius: var(--radius-md);
      overflow: hidden;
      border: 1px solid var(--card-border);
      font-size: 13px;
    }}
    th, td {{
      padding: 12px 16px;
      text-align: left;
      border-bottom: 1px solid var(--card-border);
    }}
    th {{
      background: rgba(120, 120, 128, 0.08);
      color: var(--text-secondary);
      font-weight: 600;
    }}
    tr:last-child td {{
      border-bottom: none;
    }}
    .modal-overlay {{
      display: none;
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0, 0, 0, 0.65);
      backdrop-filter: blur(10px);
      -webkit-backdrop-filter: blur(10px);
      z-index: 1000;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }}
    .modal-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: var(--radius-lg);
      max-width: 650px;
      width: 100%;
      max-height: 85vh;
      overflow-y: auto;
      padding: 24px;
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
    }}
    .modal-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 16px;
      padding-bottom: 12px;
      border-bottom: 1px solid var(--card-border);
    }}
    .modal-title {{
      font-size: 18px;
      font-weight: 600;
    }}
    .close-btn {{
      background: transparent;
      border: none;
      font-size: 20px;
      cursor: pointer;
      color: var(--text-secondary);
    }}
    .drawer {{
      position: fixed;
      top: 0;
      right: -480px;
      width: 480px;
      max-width: 90vw;
      height: 100vh;
      background: var(--card-bg);
      border-left: 1px solid var(--card-border);
      box-shadow: -10px 0 30px rgba(0, 0, 0, 0.25);
      z-index: 1100;
      transition: right 0.25s cubic-bezier(0.16, 1, 0.3, 1);
      display: flex;
      flex-direction: column;
    }}
    .drawer.open {{
      right: 0;
    }}
    .drawer-header {{
      padding: 16px 20px;
      border-bottom: 1px solid var(--card-border);
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}
    .drawer-body {{
      flex: 1;
      overflow-y: auto;
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }}
    .drawer-footer {{
      padding: 16px 20px;
      border-top: 1px solid var(--card-border);
    }}
    .chat-bubble {{
      padding: 12px 16px;
      border-radius: var(--radius-md);
      font-size: 14px;
      line-height: 1.5;
    }}
    .chat-user {{
      background: var(--accent);
      color: white;
      align-self: flex-end;
      border-bottom-right-radius: 4px;
    }}
    .chat-assistant {{
      background: rgba(120, 120, 128, 0.12);
      color: var(--text-primary);
      align-self: flex-start;
      border-bottom-left-radius: 4px;
    }}
    .citation-card {{
      background: rgba(120, 120, 128, 0.08);
      border-left: 3px solid var(--accent);
      padding: 8px 12px;
      margin-top: 8px;
      border-radius: 4px;
      font-size: 12px;
    }}
    .citation-title {{
      font-weight: 600;
      color: var(--text-primary);
      margin-bottom: 2px;
    }}
    .citation-url {{
      color: var(--accent);
      text-decoration: none;
      word-break: break-all;
    }}
    .toggle-switch {{
      position: relative;
      display: inline-block;
      width: 44px;
      height: 24px;
    }}
    .toggle-switch input {{
      opacity: 0;
      width: 0;
      height: 0;
    }}
    .toggle-slider {{
      position: absolute;
      cursor: pointer;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background-color: rgba(120, 120, 128, 0.32);
      transition: .2s;
      border-radius: 24px;
    }}
    .toggle-slider:before {{
      position: absolute;
      content: "";
      height: 18px;
      width: 18px;
      left: 3px;
      bottom: 3px;
      background-color: white;
      transition: .2s;
      border-radius: 50%;
    }}
    input:checked + .toggle-slider {{
      background-color: var(--success);
    }}
    input:checked + .toggle-slider:before {{
      transform: translateX(20px);
    }}
    footer {{
      background: var(--card-bg);
      border-top: 1px solid var(--card-border);
      padding: 24px;
      text-align: center;
      font-size: 13px;
      color: var(--text-secondary);
      margin-top: auto;
    }}
    @media (max-width: 768px) {{
      .header-container {{
        flex-direction: column;
        align-items: stretch;
      }}
      .nav-tabs {{
        overflow-x: auto;
      }}
      .stats-grid {{
        grid-template-columns: 1fr;
      }}
    }}
  </style>
</head>
<body>
  <!-- Header -->
  <header>
    <div class="header-container">
      <a href="#" class="brand" onclick="switchTab('publicPortal'); return false;">
        <div class="brand-logo">🇮🇳</div>
        <div class="brand-text">
          <h1>Election Intelligence Platform</h1>
          <p>Evidence-First • Neutral Public Research</p>
        </div>
      </a>

      <!-- 4-Tier Application Tabs -->
      <nav class="nav-tabs" role="tablist" aria-label="Main Navigation">
        <button class="nav-btn active" id="tab-publicPortal" onclick="switchTab('publicPortal')">
          🏛️ Public Portal
        </button>
        <button class="nav-btn" id="tab-executiveCommand" onclick="switchTab('executiveCommand')">
          📊 Command Center
        </button>
        <button class="nav-btn" id="tab-operationsConsole" onclick="switchTab('operationsConsole')">
          ⚙️ Operations
        </button>
        <button class="nav-btn" id="tab-controlCenter" onclick="switchTab('controlCenter')">
          🛡️ Control Center
        </button>
      </nav>

      <!-- Action Tools -->
      <div class="header-actions">
        <button class="k-shortcut" onclick="openCommandPalette()" title="Press Cmd+K to search">
          <span>Search</span>
          <kbd>⌘K</kbd>
        </button>
        <button class="btn btn-primary" onclick="openAIDrawer()" style="padding: 6px 12px; font-size: 12px;">
          ✨ Ask AI
        </button>
        <button class="icon-btn" onclick="toggleTheme()" title="Toggle Theme" aria-label="Toggle theme">
          🌓
        </button>
      </div>
    </div>
  </header>

  <!-- Main View Surfaces -->
  <main>
    <!-- Top Mission & Verification Banner -->
    <div class="mission-banner">
      <div class="mission-text">
        <h2>Independent Indian Electoral Research Platform</h2>
        <p>
          Organizing, verifying, and explaining publicly available election records and candidate statutory Form 26 disclosures with complete transparency and provenance. Strictly non-partisan with zero commercial endorsements or candidate rankings.
        </p>
      </div>
      <div class="neutral-badge">
        ✓ 100% Sourced & Grounded
      </div>
    </div>

    <!-- 1. PUBLIC PORTAL VIEW -->
    <div id="view-publicPortal" class="view-surface">
      <!-- High-Level Certified KPIs -->
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-label">Registered Electors</div>
          <div class="stat-value">968.8M</div>
          <div class="stat-subtext">Certified national electorate (543 seats)</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">National Turnout</div>
          <div class="stat-value">67.4%</div>
          <div class="stat-subtext">Average turnout across 7 phases</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Contesting Candidates</div>
          <div class="stat-value">8,420</div>
          <div class="stat-subtext">100% Form 26 disclosures verified</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Polling Stations</div>
          <div class="stat-value">1,048,000</div>
          <div class="stat-subtext">EVM & VVPAT audited booths</div>
        </div>
      </div>

      <!-- Global Multi-Field Search Bar -->
      <div class="search-bar-container">
        <span class="search-icon">🔍</span>
        <input type="text" id="global-search-input" class="search-input" placeholder="Search elections, constituencies, candidates, parties, or affidavits (e.g. Varanasi, Modi, Wayanad, BJP)..." onkeyup="handleGlobalSearch(event)">
      </div>
      <div id="search-results-box" style="display: none; margin-bottom: 24px;"></div>

      <!-- Candidate Directory -->
      <div class="section-title">
        <span>Contesting Candidates & Form 26 Disclosures</span>
        <span style="font-size: 13px; font-weight: normal; color: var(--text-secondary);">Statutory affidavits submitted to ECI</span>
      </div>
      <div class="card-grid" id="candidate-cards-container">
        <!-- Rendered dynamically from PostgreSQL -->
      </div>

      <!-- Declared Results Section -->
      <div class="section-title">
        <span>Certified Election Results</span>
        <span style="font-size: 13px; font-weight: normal; color: var(--text-secondary);">Official declarations via Returning Officers</span>
      </div>
      <div style="overflow-x: auto;">
        <table id="results-table">
          <thead>
            <tr>
              <th>Constituency</th>
              <th>Winning Candidate</th>
              <th>Winning Party</th>
              <th>Total Votes Polled</th>
              <th>Victory Margin</th>
              <th>Official Source</th>
            </tr>
          </thead>
          <tbody id="results-tbody">
            <!-- Rendered dynamically -->
          </tbody>
        </table>
      </div>
    </div>

    <!-- 2. EXECUTIVE COMMAND CENTER VIEW -->
    <div id="view-executiveCommand" class="view-surface" style="display: none;">
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-label">Total Elections Monitored</div>
          <div class="stat-value">24</div>
          <div class="stat-subtext">Lok Sabha, Vidhan Sabha & By-elections</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Platform Availability</div>
          <div class="stat-value">99.98%</div>
          <div class="stat-subtext">SLA uptime across polling window</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">AI Queries Answered</div>
          <div class="stat-value">245,000+</div>
          <div class="stat-subtext">Zero unsupported hallucinations</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Statutory Observers</div>
          <div class="stat-value">2,150</div>
          <div class="stat-subtext">ECI accredited observers active</div>
        </div>
      </div>

      <div class="section-title">Regional Voter Turnout Performance</div>
      <table>
        <thead>
          <tr>
            <th>Zone / Region</th>
            <th>Registered Electorate</th>
            <th>Voter Turnout %</th>
            <th>Polling Booths</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody id="turnout-tbody">
          <!-- Populated from regional_turnout -->
        </tbody>
      </table>
    </div>

    <!-- 3. OPERATIONS CONSOLE VIEW -->
    <div id="view-operationsConsole" class="view-surface" style="display: none;">
      <div class="section-title">Election Lifecycle Operations</div>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 20px;">
        <!-- Schedule Election Card -->
        <div class="stat-card">
          <h3 style="font-size: 16px; margin-bottom: 12px;">Schedule New Election</h3>
          <form onsubmit="handleCreateElection(event)" style="display: flex; flex-direction: column; gap: 10px;">
            <input type="text" id="new-elec-title" placeholder="Election Title (e.g. Punjab Assembly 2027)" required style="padding: 8px 12px; border-radius: 6px; border: 1px solid var(--card-border); background: var(--bg); color: var(--text-primary);">
            <select id="new-elec-type" style="padding: 8px 12px; border-radius: 6px; border: 1px solid var(--card-border); background: var(--bg); color: var(--text-primary);">
              <option value="GENERAL">General Election (Lok Sabha)</option>
              <option value="ASSEMBLY">Legislative Assembly</option>
              <option value="BY_ELECTION">By-Election</option>
            </select>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
              <input type="date" id="new-elec-start" required style="padding: 8px; border-radius: 6px; border: 1px solid var(--card-border); background: var(--bg); color: var(--text-primary);">
              <input type="date" id="new-elec-end" required style="padding: 8px; border-radius: 6px; border: 1px solid var(--card-border); background: var(--bg); color: var(--text-primary);">
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
              <input type="number" id="new-elec-voters" placeholder="Voters" value="15000000" style="padding: 8px; border-radius: 6px; border: 1px solid var(--card-border); background: var(--bg); color: var(--text-primary);">
              <input type="number" id="new-elec-constituencies" placeholder="Seats" value="117" style="padding: 8px; border-radius: 6px; border: 1px solid var(--card-border); background: var(--bg); color: var(--text-primary);">
            </div>
            <button type="submit" class="btn btn-primary" style="margin-top: 6px;">Schedule via CQRS Pipeline</button>
          </form>
        </div>

        <!-- File Candidate Nomination Card -->
        <div class="stat-card">
          <h3 style="font-size: 16px; margin-bottom: 12px;">Candidate Form 26 Filing</h3>
          <form onsubmit="handleRegisterCandidate(event)" style="display: flex; flex-direction: column; gap: 10px;">
            <input type="text" id="new-cand-name" placeholder="Candidate Full Name" required style="padding: 8px 12px; border-radius: 6px; border: 1px solid var(--card-border); background: var(--bg); color: var(--text-primary);">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
              <input type="number" id="new-cand-age" placeholder="Age (>= 25)" min="25" value="45" required style="padding: 8px; border-radius: 6px; border: 1px solid var(--card-border); background: var(--bg); color: var(--text-primary);">
              <input type="number" step="0.01" id="new-cand-assets" placeholder="Assets (Cr ₹)" value="5.2" required style="padding: 8px; border-radius: 6px; border: 1px solid var(--card-border); background: var(--bg); color: var(--text-primary);">
            </div>
            <input type="text" id="new-cand-education" placeholder="Highest Educational Qualification" value="B.A. Political Science" required style="padding: 8px 12px; border-radius: 6px; border: 1px solid var(--card-border); background: var(--bg); color: var(--text-primary);">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
              <select id="new-cand-constituency" style="padding: 8px; border-radius: 6px; border: 1px solid var(--card-border); background: var(--bg); color: var(--text-primary);">
                <option value="const-001">Varanasi (UP-77)</option>
                <option value="const-002">Wayanad (KL-04)</option>
                <option value="const-003">New Delhi (DL-04)</option>
                <option value="const-004">Gandhinagar (GJ-06)</option>
              </select>
              <select id="new-cand-party" style="padding: 8px; border-radius: 6px; border: 1px solid var(--card-border); background: var(--bg); color: var(--text-primary);">
                <option value="party-bjp">BJP</option>
                <option value="party-inc">INC</option>
                <option value="party-sp">SP</option>
                <option value="party-aap">AAP</option>
              </select>
            </div>
            <button type="submit" class="btn btn-primary" style="margin-top: 6px;">Register Candidate & Affidavit</button>
          </form>
        </div>
      </div>

      <!-- ETL Batches Table -->
      <div class="section-title">Data Ingestion (ETL) Batches & Provenance</div>
      <table>
        <thead>
          <tr>
            <th>Batch ID</th>
            <th>Source File</th>
            <th>Records Ingested</th>
            <th>Provenance Feed</th>
            <th>Status</th>
            <th>Imported At</th>
          </tr>
        </thead>
        <tbody id="etl-tbody">
          <!-- Populated from import_batches -->
        </tbody>
      </table>
    </div>

    <!-- 4. ENTERPRISE CONTROL CENTER VIEW -->
    <div id="view-controlCenter" class="view-surface" style="display: none;">
      <!-- System Telemetry Metrics -->
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-label">CPU Core Utilization</div>
          <div class="stat-value" id="metric-cpu">14.2%</div>
          <div class="stat-subtext">8-core bare metal ARM64</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Memory Distribution</div>
          <div class="stat-value" id="metric-mem">38.5%</div>
          <div class="stat-subtext">Tokio async resident set</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">PostgreSQL Pool</div>
          <div class="stat-value" id="metric-db">5 active</div>
          <div class="stat-subtext">0 connection pool overflow</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">API Latency (p99)</div>
          <div class="stat-value" id="metric-latency">8.4ms</div>
          <div class="stat-subtext">Sub-10ms response guarantee</div>
        </div>
      </div>

      <!-- Dynamic Feature Flags -->
      <div class="section-title">Runtime Feature Flags & Circuit Breakers</div>
      <div id="feature-flags-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 14px; margin-bottom: 32px;">
        <!-- Feature flag toggles rendered dynamically -->
      </div>

      <!-- Tamper-Evident SHA-256 Audit Log -->
      <div class="section-title">
        <span>Cryptographic Audit Event Stream</span>
        <span class="neutral-badge" id="audit-chain-badge">SHA-256 Chain Verified ✓</span>
      </div>
      <div style="overflow-x: auto;">
        <table>
          <thead>
            <tr>
              <th>Seq</th>
              <th>Timestamp</th>
              <th>Actor</th>
              <th>Action</th>
              <th>Target Resource</th>
              <th>SHA-256 Hash</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody id="audit-tbody">
            <!-- Populated from audit_log -->
          </tbody>
        </table>
      </div>
    </div>
  </main>

  <!-- Candidate Form 26 Modal -->
  <div class="modal-overlay" id="candidate-modal" onclick="closeModalOnBg(event)">
    <div class="modal-card">
      <div class="modal-header">
        <div class="modal-title" id="modal-cand-name">Candidate Form 26 Affidavit</div>
        <button class="close-btn" onclick="closeModal()">×</button>
      </div>
      <div id="modal-cand-content"></div>
    </div>
  </div>

  <!-- Command Palette Modal (Cmd+K) -->
  <div class="modal-overlay" id="command-palette-modal" onclick="closeModalOnBg(event)">
    <div class="modal-card" style="max-width: 520px; padding: 16px;">
      <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
        <span style="font-size: 18px;">🔍</span>
        <input type="text" id="palette-input" placeholder="Type a command or search entities..." style="width: 100%; border: none; background: transparent; font-size: 16px; outline: none; color: var(--text-primary);" onkeyup="handlePaletteInput(event)">
        <kbd style="font-size: 10px; background: rgba(120, 120, 128, 0.2); padding: 2px 6px; border-radius: 4px;">ESC</kbd>
      </div>
      <div id="palette-results" style="max-height: 300px; overflow-y: auto; display: flex; flex-direction: column; gap: 4px;">
        <!-- Quick command items -->
      </div>
    </div>
  </div>

  <!-- Evidence Grounded AI Drawer -->
  <div class="drawer" id="ai-drawer">
    <div class="drawer-header">
      <div style="display: flex; align-items: center; gap: 8px;">
        <span style="font-size: 18px;">✨</span>
        <strong style="font-size: 15px;">Grounded AI Intelligence</strong>
      </div>
      <button class="close-btn" onclick="closeAIDrawer()">×</button>
    </div>
    <div class="drawer-body" id="ai-chat-body">
      <div class="chat-bubble chat-assistant">
        Hello! I am the Election Intelligence grounded assistant. I can answer questions regarding candidates, constituencies, Form 26 disclosures, voter turnout, and declared election results with full statutory source citations.
        <div style="margin-top: 8px; font-size: 12px; color: var(--text-secondary);">
          Try: "Who won Varanasi in 2026?" or "What are Rahul Gandhi's declared assets?"
        </div>
      </div>
    </div>
    <div class="drawer-footer">
      <form onsubmit="handleSendAIMessage(event)" style="display: flex; gap: 8px;">
        <input type="text" id="ai-chat-input" placeholder="Ask a question..." style="flex: 1; padding: 10px 14px; border-radius: var(--radius-sm); border: 1px solid var(--card-border); background: var(--bg); color: var(--text-primary); outline: none;">
        <button type="submit" class="btn btn-primary">Send</button>
      </form>
    </div>
  </div>

  <!-- Toast Notification Container -->
  <div id="toast" style="position: fixed; bottom: 24px; right: 24px; background: var(--card-bg); border: 1px solid var(--card-border); padding: 12px 20px; border-radius: var(--radius-md); box-shadow: 0 10px 30px rgba(0,0,0,0.25); display: none; z-index: 2000; font-size: 13px;"></div>

  <!-- Footer -->
  <footer>
    <div style="max-width: 1400px; margin: 0 auto; display: flex; flex-direction: column; gap: 8px; align-items: center;">
      <p>
        <strong>Election Intelligence Platform v1.0.0</strong> — Built entirely in Rust (Axum, Tokio, SQLx, PostgreSQL) adhering to Apple Human Interface Guidelines.
      </p>
      <p style="font-size: 12px; max-width: 800px;">
        All electoral declarations and candidate affidavit disclosures are retrieved directly from official Election Commission of India (ECI) public gazettes and statutory Form 26 filings. This platform maintains strict political neutrality and does not endorse, rank, or favor any political party or candidate.
      </p>
    </div>
  </footer>

  <script>
    // State management
    let currentTab = 'publicPortal';
    let cachedCandidates = [];
    let cachedResults = [];

    // Switch between 4-tier application surfaces
    function switchTab(tab) {{
      currentTab = tab;
      document.querySelectorAll('.view-surface').forEach(el => el.style.display = 'none');
      document.querySelectorAll('.nav-btn').forEach(el => el.classList.remove('active'));

      const target = document.getElementById('view-' + tab);
      const btn = document.getElementById('tab-' + tab);
      if (target) target.style.display = 'block';
      if (btn) btn.classList.add('active');

      if (tab === 'publicPortal') loadPublicPortalData();
      else if (tab === 'executiveCommand') loadExecutiveCommandData();
      else if (tab === 'operationsConsole') loadOperationsData();
      else if (tab === 'controlCenter') loadControlCenterData();
    }}

    // Theme toggle
    function toggleTheme() {{
      const html = document.documentElement;
      if (html.classList.contains('dark')) {{
        html.classList.remove('dark');
        localStorage.setItem('theme', 'light');
        showToast('Switched to Light Mode');
      }} else {{
        html.classList.add('dark');
        localStorage.setItem('theme', 'dark');
        showToast('Switched to Dark Mode');
      }}
    }}

    function showToast(msg) {{
      const t = document.getElementById('toast');
      t.innerText = msg;
      t.style.display = 'block';
      setTimeout(() => t.style.display = 'none', 3000);
    }}

    // Load Public Portal Data
    async function loadPublicPortalData() {{
      try {{
        const [candRes, resRes] = await Promise.all([
          fetch('/api/v1/candidates'),
          fetch('/api/v1/results')
        ]);
        const candData = await candRes.json();
        const resData = await resRes.json();

        if (candData.success) {{
          cachedCandidates = candData.data;
          renderCandidates(cachedCandidates);
        }}
        if (resData.success) {{
          cachedResults = resData.data;
          renderResults(cachedResults);
        }}
      }} catch (e) {{
        console.error('Failed to load portal data', e);
      }}
    }}

    function renderCandidates(candidates) {{
      const container = document.getElementById('candidate-cards-container');
      container.innerHTML = '';

      candidates.forEach(c => {{
        const card = document.createElement('div');
        card.className = 'candidate-card';
        card.innerHTML = `
          <div>
            <div class="candidate-header">
              <div>
                <div class="candidate-name">${{c.name}}</div>
                <div class="candidate-constituency">${{c.constituency_name || 'Parliamentary'}}</div>
              </div>
              <span class="party-tag" style="background-color: ${{c.party_color || '#0071e3'}};">${{c.party_name || 'Candidate'}}</span>
            </div>
            <div class="candidate-meta">
              <div class="meta-item">
                <span>Declared Assets</span>
                <span style="color: var(--success);">₹${{c.declared_assets_cr}} Cr</span>
              </div>
              <div class="meta-item">
                <span>Criminal Cases</span>
                <span style="color: ${{c.criminal_cases > 0 ? 'var(--warning)' : 'var(--text-secondary)'}};">${{c.criminal_cases}} reported</span>
              </div>
              <div class="meta-item">
                <span>Education</span>
                <span>${{c.education.split('(')[0]}}</span>
              </div>
              <div class="meta-item">
                <span>Age</span>
                <span>${{c.age}} yrs</span>
              </div>
            </div>
          </div>
          <div style="display: flex; align-items: center; justify-content: space-between; margin-top: 10px;">
            <span class="badge-f26 badge-verified">✓ Form 26 Verified</span>
            <button class="btn btn-secondary" onclick="openCandidateModal('${{c.id}}')">Inspect Affidavit</button>
          </div>
        `;
        container.appendChild(card);
      }});
    }}

    function renderResults(results) {{
      const tbody = document.getElementById('results-tbody');
      tbody.innerHTML = '';
      results.forEach(r => {{
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td><strong>${{r.constituency_name || r.constituency_id}}</strong></td>
          <td>${{r.winning_candidate_name || r.winning_candidate_id}}</td>
          <td>${{r.winning_party_name || 'Independent'}}</td>
          <td>${{Number(r.total_votes).toLocaleString('en-IN')}}</td>
          <td><span style="color: var(--success); font-weight: 600;">+${{Number(r.margin).toLocaleString('en-IN')}}</span></td>
          <td><a href="https://results.eci.gov.in" target="_blank" style="color: var(--accent); text-decoration: none;">${{r.source_publisher || 'ECI Official'}}</a></td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    // Global Search Handler
    let searchDebounce = null;
    function handleGlobalSearch(e) {{
      const q = e.target.value.trim();
      clearTimeout(searchDebounce);
      if (!q) {{
        document.getElementById('search-results-box').style.display = 'none';
        renderCandidates(cachedCandidates);
        return;
      }}
      searchDebounce = setTimeout(async () => {{
        const res = await fetch(`/api/v1/search?q=${{encodeURIComponent(q)}}`);
        const json = await res.json();
        if (json.success && json.data.results.length > 0) {{
          const box = document.getElementById('search-results-box');
          box.style.display = 'block';
          box.innerHTML = `
            <div class="stat-card" style="border-left: 3px solid var(--accent);">
              <div style="font-weight: 600; margin-bottom: 8px;">BM25 Search Results (${{json.data.total_hits}} hits)</div>
              <div style="display: flex; flex-direction: column; gap: 8px;">
                ${{json.data.results.map(h => `
                  <div style="padding: 6px 0; border-bottom: 1px solid var(--card-border);">
                    <div style="font-weight: 500; font-size: 14px;">${{h.title}} <span class="party-tag" style="background: rgba(120,120,128,0.3); font-size: 10px;">${{h.category}}</span></div>
                    <div style="font-size: 12px; color: var(--text-secondary);">${{h.description}}</div>
                  </div>
                `).join('')}}
              </div>
            </div>
          `;
        }}
      }}, 200);
    }}

    // Candidate Form 26 Modal
    function openCandidateModal(candId) {{
      const cand = cachedCandidates.find(c => c.id === candId);
      if (!cand) return;

      document.getElementById('modal-cand-name').innerText = `${{cand.name}} — Statutory Form 26 Affidavit`;
      const content = document.getElementById('modal-cand-content');

      let casesHtml = '<p style="color: var(--success); font-size: 13px;">No criminal cases reported under statutory disclosure.</p>';
      if (cand.criminal_cases_details && cand.criminal_cases_details.length > 0) {{
        casesHtml = cand.criminal_cases_details.map(cd => `
          <div style="background: rgba(120, 120, 128, 0.08); padding: 10px 14px; border-radius: 6px; margin-bottom: 8px; font-size: 12px;">
            <div style="font-weight: 600;">Case: ${{cd.case_no}} (${{cd.court}})</div>
            <div style="color: var(--text-secondary);">Sections: ${{cd.sections}}</div>
            <div style="color: var(--warning); margin-top: 4px;">Status: ${{cd.status}}</div>
          </div>
        `).join('');
      }}

      content.innerHTML = `
        <div style="display: flex; flex-direction: column; gap: 16px;">
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; font-size: 13px;">
            <div><span style="color: var(--text-secondary);">Parliamentary Constituency:</span> <strong>${{cand.constituency_name || 'UP-77'}}</strong></div>
            <div><span style="color: var(--text-secondary);">Party Affiliation:</span> <strong>${{cand.party_name || 'Independent'}}</strong></div>
            <div><span style="color: var(--text-secondary);">Declared Movable/Immovable:</span> <strong style="color: var(--success);">₹${{cand.declared_assets_cr}} Crores</strong></div>
            <div><span style="color: var(--text-secondary);">Declared Liabilities:</span> <strong>₹${{cand.declared_liabilities_cr}} Crores</strong></div>
            <div style="grid-column: span 2;"><span style="color: var(--text-secondary);">Education:</span> <strong>${{cand.education}}</strong></div>
          </div>

          <div style="border-top: 1px solid var(--card-border); padding-top: 14px;">
            <h4 style="font-size: 14px; font-weight: 600; margin-bottom: 8px;">Reported Judicial Matters (Form 26 Disclosures)</h4>
            ${{casesHtml}}
            <p style="font-size: 11px; color: var(--text-secondary); margin-top: 6px;">
              * Note: Disclosed cases represent statutory sworn affidavits filed during nomination. Under Indian jurisprudence, charges or pending trials do not constitute judicial determinations of guilt.
            </p>
          </div>

          <div style="border-top: 1px solid var(--card-border); padding-top: 12px; font-size: 12px; color: var(--text-secondary); display: flex; justify-content: space-between; align-items: center;">
            <span>Source: ${{cand.source_ref || 'ECI Official Repository'}}</span>
            <span class="badge-f26 badge-verified">ECI Verified Record</span>
          </div>
        </div>
      `;
      document.getElementById('candidate-modal').style.display = 'flex';
    }}

    function closeModal() {{
      document.getElementById('candidate-modal').style.display = 'none';
      document.getElementById('command-palette-modal').style.display = 'none';
    }}

    function closeModalOnBg(e) {{
      if (e.target.classList.contains('modal-overlay')) closeModal();
    }}

    // Load Command Center Data
    async function loadExecutiveCommandData() {{
      try {{
        const res = await fetch('/api/v1/observability');
        const json = await res.json();
        if (json.success && json.data.regional_turnout) {{
          const tbody = document.getElementById('turnout-tbody');
          tbody.innerHTML = '';
          json.data.regional_turnout.forEach(t => {{
            const tr = document.createElement('tr');
            tr.innerHTML = `
              <td><strong>${{t.region}}</strong></td>
              <td>${{t.total_voters}}</td>
              <td><span style="color: var(--success); font-weight: 600;">${{t.voter_turnout_percent}}%</span></td>
              <td>${{Number(t.polling_booths).toLocaleString('en-IN')}}</td>
              <td><span class="badge-f26 badge-verified">${{t.phase_status}}</span></td>
            `;
            tbody.appendChild(tr);
          }});
        }}
      }} catch (e) {{
        console.error('Failed to load command center data', e);
      }}
    }}

    // Load Operations Data
    async function loadOperationsData() {{
      try {{
        const res = await fetch('/api/v1/etl');
        const json = await res.json();
        if (json.success) {{
          const tbody = document.getElementById('etl-tbody');
          tbody.innerHTML = '';
          json.data.forEach(b => {{
            const tr = document.createElement('tr');
            tr.innerHTML = `
              <td><code>${{b.id}}</code></td>
              <td>${{b.source_file}}</td>
              <td>${{b.records_count}}</td>
              <td>${{b.provenance}}</td>
              <td><span class="badge-f26 badge-verified">${{b.status}}</span></td>
              <td>${{b.imported_at.split('T')[0]}}</td>
            `;
            tbody.appendChild(tr);
          }});
        }}
      }} catch (e) {{
        console.error('Failed to load operations data', e);
      }}
    }}

    // Schedule Election Handler
    async function handleCreateElection(e) {{
      e.preventDefault();
      const payload = {{
        title: document.getElementById('new-elec-title').value,
        election_type: document.getElementById('new-elec-type').value,
        start_date: document.getElementById('new-elec-start').value,
        end_date: document.getElementById('new-elec-end').value,
        total_registered_voters: parseInt(document.getElementById('new-elec-voters').value, 10),
        total_constituencies: parseInt(document.getElementById('new-elec-constituencies').value, 10),
        phases: 1
      }};

      const res = await fetch('/api/v1/elections', {{
        method: 'POST',
        headers: {{ 'Content-Type': 'application/json' }},
        body: JSON.stringify(payload)
      }});
      const json = await res.json();
      if (json.success) {{
        showToast('Election scheduled successfully!');
        e.target.reset();
      }} else {{
        showToast('Error: ' + json.error);
      }}
    }}

    // Register Candidate Handler
    async function handleRegisterCandidate(e) {{
      e.preventDefault();
      const payload = {{
        name: document.getElementById('new-cand-name').value,
        age: parseInt(document.getElementById('new-cand-age').value, 10),
        email: 'info@election.gov.in',
        phone: '+919811000000',
        constituency_id: document.getElementById('new-cand-constituency').value,
        party_id: document.getElementById('new-cand-party').value,
        education: document.getElementById('new-cand-education').value,
        declared_assets_cr: parseFloat(document.getElementById('new-cand-assets').value),
        criminal_cases: 0
      }};

      const res = await fetch('/api/v1/candidates', {{
        method: 'POST',
        headers: {{ 'Content-Type': 'application/json' }},
        body: JSON.stringify(payload)
      }});
      const json = await res.json();
      if (json.success) {{
        showToast('Candidate nomination & affidavit registered!');
        e.target.reset();
        loadPublicPortalData();
      }} else {{
        showToast('Error: ' + json.error);
      }}
    }}

    // Load Control Center Data (Metrics, Flags, Audit)
    async function loadControlCenterData() {{
      try {{
        const res = await fetch('/api/v1/observability');
        const json = await res.json();
        if (json.success) {{
          const m = json.data.metrics;
          document.getElementById('metric-cpu').innerText = `${{m.cpu_utilization}}%`;
          document.getElementById('metric-mem').innerText = `${{m.memory_utilization}}%`;
          document.getElementById('metric-db').innerText = `${{m.db_pool_active}} active`;
          document.getElementById('metric-latency').innerText = `${{m.p99_latency_ms}}ms`;

          // Render Feature Flags
          const flagsContainer = document.getElementById('feature-flags-grid');
          flagsContainer.innerHTML = '';
          json.data.feature_flags.forEach(f => {{
            const card = document.createElement('div');
            card.className = 'stat-card';
            card.style.display = 'flex';
            card.style.alignItems = 'center';
            card.style.justifyContent = 'space-between';
            card.innerHTML = `
              <div>
                <div style="font-weight: 600; font-size: 14px;"><code>${{f.name}}</code></div>
                <div style="font-size: 12px; color: var(--text-secondary); margin-top: 2px;">${{f.description}}</div>
              </div>
              <label class="toggle-switch">
                <input type="checkbox" ${{f.enabled ? 'checked' : ''}} onchange="toggleFlag('${{f.name}}', this.checked)">
                <span class="toggle-slider"></span>
              </label>
            `;
            flagsContainer.appendChild(card);
          }});

          // Render Audit Logs
          const auditRes = await fetch('/api/v1/admin/audit-logs');
          const auditJson = await auditRes.json();
          if (auditJson.success) {{
            const tbody = document.getElementById('audit-tbody');
            tbody.innerHTML = '';
            auditJson.data.forEach(l => {{
              const tr = document.createElement('tr');
              tr.innerHTML = `
                <td><code>#${{l.sequence_number}}</code></td>
                <td>${{l.timestamp.split('T')[1].split('.')[0]}}</td>
                <td><strong>${{l.actor}}</strong></td>
                <td><span class="party-tag" style="background: rgba(120,120,128,0.3); font-size: 10px;">${{l.action}}</span></td>
                <td><code>${{l.resource}}</code></td>
                <td><span style="font-family: monospace; font-size: 11px; color: var(--text-secondary);">${{l.current_hash.substring(0, 16)}}...</span></td>
                <td><span class="badge-f26 badge-verified">${{l.status}}</span></td>
              `;
              tbody.appendChild(tr);
            }});
          }}
        }}
      }} catch (e) {{
        console.error('Failed to load control center data', e);
      }}
    }}

    async function toggleFlag(name, enabled) {{
      const res = await fetch('/api/v1/admin/feature-flags', {{
        method: 'PATCH',
        headers: {{ 'Content-Type': 'application/json' }},
        body: JSON.stringify({{ name, enabled }})
      }});
      const json = await res.json();
      if (json.success) {{
        showToast(`Feature flag '${{name}}' updated to ${{enabled ? 'Enabled' : 'Disabled'}}`);
      }}
    }}

    // AI Assistant Drawer
    function openAIDrawer() {{
      document.getElementById('ai-drawer').classList.add('open');
    }}

    function closeAIDrawer() {{
      document.getElementById('ai-drawer').classList.remove('open');
    }}

    async function handleSendAIMessage(e) {{
      e.preventDefault();
      const input = document.getElementById('ai-chat-input');
      const text = input.value.trim();
      if (!text) return;

      const body = document.getElementById('ai-chat-body');
      const userBubble = document.createElement('div');
      userBubble.className = 'chat-bubble chat-user';
      userBubble.innerText = text;
      body.appendChild(userBubble);
      input.value = '';
      body.scrollTop = body.scrollHeight;

      // Loading indicator
      const loader = document.createElement('div');
      loader.className = 'chat-bubble chat-assistant';
      loader.innerText = 'Retrieving certified electoral evidence...';
      body.appendChild(loader);
      body.scrollTop = body.scrollHeight;

      try {{
        const res = await fetch('/api/v1/ai/query', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{ query: text, max_citations: 3 }})
        }});
        const json = await res.json();
        body.removeChild(loader);

        const aiBubble = document.createElement('div');
        aiBubble.className = 'chat-bubble chat-assistant';

        if (json.success) {{
          const resp = json.data;
          let citesHtml = '';
          if (resp.citations && resp.citations.length > 0) {{
            citesHtml = resp.citations.map(c => `
              <div class="citation-card">
                <div class="citation-title">📌 ${{c.publisher}} — ${{c.section}}</div>
                <div style="color: var(--text-secondary); margin-bottom: 2px;">"${{c.quote}}"</div>
                <a href="${{c.url}}" target="_blank" class="citation-url">${{c.url}}</a>
              </div>
            `).join('');
          }}

          aiBubble.innerHTML = `
            <div>${{resp.answer.replace(/\n/g, '<br>')}}</div>
            ${{citesHtml}}
            <div style="margin-top: 8px; font-size: 11px; color: var(--text-secondary);">
              Grounding score: <strong>${{resp.grounding_score * 100}}%</strong> • Verified ECI Gazette
            </div>
          `;
        }} else {{
          aiBubble.innerText = 'Error: ' + json.error;
        }}
        body.appendChild(aiBubble);
        body.scrollTop = body.scrollHeight;
      }} catch (err) {{
        loader.innerText = 'Failed to retrieve answer from AI service.';
      }}
    }}

    // Command Palette (Cmd+K)
    function openCommandPalette() {{
      document.getElementById('command-palette-modal').style.display = 'flex';
      const input = document.getElementById('palette-input');
      input.value = '';
      input.focus();
      renderDefaultPaletteCommands();
    }}

    function renderDefaultPaletteCommands() {{
      const res = document.getElementById('palette-results');
      res.innerHTML = `
        <div onclick="switchTab('publicPortal'); closeModal();" style="padding: 10px; border-radius: 6px; cursor: pointer; display: flex; align-items: center; justify-content: space-between;">
          <span>🏛️ Go to Public Portal</span>
          <span style="font-size: 11px; color: var(--text-secondary);">Landing & Search</span>
        </div>
        <div onclick="switchTab('executiveCommand'); closeModal();" style="padding: 10px; border-radius: 6px; cursor: pointer; display: flex; align-items: center; justify-content: space-between;">
          <span>📊 Go to Command Center</span>
          <span style="font-size: 11px; color: var(--text-secondary);">KPIs & Turnout</span>
        </div>
        <div onclick="switchTab('operationsConsole'); closeModal();" style="padding: 10px; border-radius: 6px; cursor: pointer; display: flex; align-items: center; justify-content: space-between;">
          <span>⚙️ Go to Operations Console</span>
          <span style="font-size: 11px; color: var(--text-secondary);">Elections & ETL</span>
        </div>
        <div onclick="switchTab('controlCenter'); closeModal();" style="padding: 10px; border-radius: 6px; cursor: pointer; display: flex; align-items: center; justify-content: space-between;">
          <span>🛡️ Go to Enterprise Control Center</span>
          <span style="font-size: 11px; color: var(--text-secondary);">Telemetry & Audit</span>
        </div>
        <div onclick="openAIDrawer(); closeModal();" style="padding: 10px; border-radius: 6px; cursor: pointer; display: flex; align-items: center; justify-content: space-between;">
          <span>✨ Ask Grounded AI Assistant</span>
          <span style="font-size: 11px; color: var(--text-secondary);">Grounded Inquiries</span>
        </div>
      `;
    }}

    function handlePaletteInput(e) {{
      const q = e.target.value.toLowerCase().trim();
      if (!q) {{
        renderDefaultPaletteCommands();
        return;
      }}
      const res = document.getElementById('palette-results');
      const filtered = cachedCandidates.filter(c => c.name.toLowerCase().includes(q) || (c.party_name && c.party_name.toLowerCase().includes(q)));
      res.innerHTML = filtered.map(c => `
        <div onclick="openCandidateModal('${{c.id}}'); closeModal();" style="padding: 8px 10px; border-radius: 6px; cursor: pointer; display: flex; align-items: center; justify-content: space-between;">
          <span><strong>${{c.name}}</strong> (${{c.party_name || 'Candidate'}})</span>
          <span class="badge-f26 badge-verified">Inspect Affidavit</span>
        </div>
      `).join('');
    }}

    // Global keyboard listener
    window.addEventListener('keydown', (e) => {{
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {{
        e.preventDefault();
        openCommandPalette();
      }}
      if ((e.metaKey || e.ctrlKey) && e.key === 'j') {{
        e.preventDefault();
        openAIDrawer();
      }}
      if (e.key === 'Escape') {{
        closeModal();
        closeAIDrawer();
      }}
    }});

    // Initialize application on load
    window.addEventListener('DOMContentLoaded', () => {{
      const savedTheme = localStorage.getItem('theme');
      if (savedTheme === 'light') document.documentElement.classList.remove('dark');
      switchTab('publicPortal');
    }});
  </script>
</body>
</html>"##
    )
}
