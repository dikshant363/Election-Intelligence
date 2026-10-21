import {
  AuditLog,
  Candidate,
  Constituency,
  Election,
  ElectionResult,
  ETLBatch,
  ExecutiveKpis,
  FeatureFlag,
  Party,
  PollingBooth,
  RegionalTurnout,
  SystemHealthMetrics,
  UserAccount,
  SearchHit,
} from './types';

// Seed Initial Data
export const initialHealthMetrics: SystemHealthMetrics = {
  cpuUtilization: 14.2,
  memoryUtilization: 38.5,
  diskFreeGb: 57.0,
  dbPoolActive: 5,
  dbPoolOverflow: 0,
  redisLatencyMs: 1.2,
  apiRequestsPerSec: 1420,
  p99LatencyMs: 8.4,
};

export const initialExecutiveKpis: ExecutiveKpis = {
  totalElectionsManaged: 24,
  totalVotersRegistered: 968800000,
  averageTurnoutPercent: 67.4,
  totalConstituencies: 543,
  totalCandidates: 8420,
  totalPollingBooths: 1048000,
  aiQueriesProcessed: 245000,
  platformUptimePercent: 99.98,
};

export const initialFeatureFlags: FeatureFlag[] = [
  {
    name: 'enable_rag',
    enabled: true,
    description: 'Enable RAG pipeline for AI queries and legal cite synthesis',
    environment: 'all',
  },
  {
    name: 'enable_websockets',
    enabled: true,
    description: 'Enable real-time WebSocket subscriptions for vote counts',
    environment: 'all',
  },
  {
    name: 'enable_sse',
    enabled: true,
    description: 'Enable Server-Sent Events streaming for telemetry alerts',
    environment: 'all',
  },
  {
    name: 'enable_background_workers',
    enabled: true,
    description: 'Enable async task execution workers for ETL batch processing',
    environment: 'all',
  },
  {
    name: 'enable_chaos_testing',
    enabled: false,
    description: 'Enable resilience chaos testing hooks & circuit breaker simulation',
    environment: 'staging',
  },
  {
    name: 'enable_mfa',
    enabled: true,
    description: 'Enforce Multi-Factor Authentication for all administrative sessions',
    environment: 'production',
  },
  {
    name: 'enable_spatial_gis',
    enabled: true,
    description: 'High-resolution geospatial boundary polygon rendering for booths',
    environment: 'all',
  },
];

export const initialAuditLogs: AuditLog[] = [
  {
    id: 'aud-9901',
    timestamp: '2026-07-23T17:22:00Z',
    actor: 'superadmin',
    action: 'UPDATE_FEATURE_FLAG',
    resource: 'feature_flags/enable_rag',
    status: 'SUCCESS',
    ipAddress: '127.0.0.1',
  },
  {
    id: 'aud-9902',
    timestamp: '2026-07-23T16:50:00Z',
    actor: 'ops_lead',
    action: 'INGEST_ELECTION_DATA',
    resource: 'etl/batch-8841',
    status: 'SUCCESS',
    ipAddress: '10.0.4.12',
  },
  {
    id: 'aud-9903',
    timestamp: '2026-07-23T15:30:00Z',
    actor: 'system',
    action: 'ROTATE_JWT_SECRET',
    resource: 'security/jwt',
    status: 'SUCCESS',
    ipAddress: '127.0.0.1',
  },
  {
    id: 'aud-9904',
    timestamp: '2026-07-23T14:15:30Z',
    actor: 'ai_eng',
    action: 'DEPLOY_MODEL_GATEWAY',
    resource: 'ai/gemini-2.5-flash',
    status: 'SUCCESS',
    ipAddress: '192.168.1.45',
  },
  {
    id: 'aud-9905',
    timestamp: '2026-07-23T12:05:10Z',
    actor: 'ops_lead',
    action: 'DECLARE_RESULT',
    resource: 'results/varanasi-2026',
    status: 'SUCCESS',
    ipAddress: '10.0.4.12',
  },
];

export const initialUserAccounts: UserAccount[] = [
  {
    id: 'usr-001',
    username: 'superadmin',
    email: 'admin@civiclens.in',
    role: 'Super Administrator',
    isActive: true,
    mfaEnabled: true,
    lastLogin: '2026-07-23T17:30:00Z',
  },
  {
    id: 'usr-002',
    username: 'ops_lead',
    email: 'ops@civiclens.in',
    role: 'Election Administrator',
    isActive: true,
    mfaEnabled: true,
    lastLogin: '2026-07-23T16:45:00Z',
  },
  {
    id: 'usr-003',
    username: 'ai_eng',
    email: 'ai@civiclens.in',
    role: 'Platform Administrator',
    isActive: true,
    mfaEnabled: true,
    lastLogin: '2026-07-23T15:10:00Z',
  },
  {
    id: 'usr-004',
    username: 'eci_observer',
    email: 'observer@eci.gov.in',
    role: 'Statutory Observer',
    isActive: true,
    mfaEnabled: true,
    lastLogin: '2026-07-23T11:20:00Z',
  },
];

export const initialParties: Party[] = [
  {
    id: 'party-bjp',
    name: 'Bharatiya Janata Party',
    code: 'BJP',
    symbol: 'Lotus',
    color: '#FF9933',
    founded_year: 1980,
    seats_contested: 440,
    seats_won: 282,
  },
  {
    id: 'party-inc',
    name: 'Indian National Congress',
    code: 'INC',
    symbol: 'Hand',
    color: '#19AAED',
    founded_year: 1885,
    seats_contested: 328,
    seats_won: 114,
  },
  {
    id: 'party-sp',
    name: 'Samajwadi Party',
    code: 'SP',
    symbol: 'Bicycle',
    color: '#E31B23',
    founded_year: 1992,
    seats_contested: 71,
    seats_won: 37,
  },
  {
    id: 'party-aitc',
    name: 'All India Trinamool Congress',
    code: 'AITC',
    symbol: 'Twin Flowers',
    color: '#20C997',
    founded_year: 1998,
    seats_contested: 48,
    seats_won: 29,
  },
  {
    id: 'party-dmk',
    name: 'Dravida Munnetra Kazhagam',
    code: 'DMK',
    symbol: 'Rising Sun',
    color: '#D63384',
    founded_year: 1949,
    seats_contested: 22,
    seats_won: 22,
  },
  {
    id: 'party-aap',
    name: 'Aam Aadmi Party',
    code: 'AAP',
    symbol: 'Broom',
    color: '#0D6EFD',
    founded_year: 2012,
    seats_contested: 23,
    seats_won: 3,
  },
];

export const initialConstituencies: Constituency[] = [
  {
    id: 'const-001',
    name: 'Varanasi',
    code: 'UP-77',
    state_code: 'IN-UP',
    state_name: 'Uttar Pradesh',
    constituency_type: 'PARLIAMENTARY',
    total_voters: 1856200,
    total_booths: 1920,
    reserved_category: 'GENERAL',
    phase: 7,
  },
  {
    id: 'const-002',
    name: 'Wayanad',
    code: 'KL-04',
    state_code: 'IN-KL',
    state_name: 'Kerala',
    constituency_type: 'PARLIAMENTARY',
    total_voters: 1462000,
    total_booths: 1420,
    reserved_category: 'GENERAL',
    phase: 2,
  },
  {
    id: 'const-003',
    name: 'New Delhi',
    code: 'DL-04',
    state_code: 'IN-DL',
    state_name: 'Delhi NCR',
    constituency_type: 'PARLIAMENTARY',
    total_voters: 1615000,
    total_booths: 1650,
    reserved_category: 'GENERAL',
    phase: 6,
  },
  {
    id: 'const-004',
    name: 'Gandhinagar',
    code: 'GJ-06',
    state_code: 'IN-GJ',
    state_name: 'Gujarat',
    constituency_type: 'PARLIAMENTARY',
    total_voters: 1945000,
    total_booths: 1980,
    reserved_category: 'GENERAL',
    phase: 3,
  },
  {
    id: 'const-005',
    name: 'Bangalore South',
    code: 'KA-26',
    state_code: 'IN-KA',
    state_name: 'Karnataka',
    constituency_type: 'PARLIAMENTARY',
    total_voters: 2210000,
    total_booths: 2150,
    reserved_category: 'GENERAL',
    phase: 2,
  },
  {
    id: 'const-006',
    name: 'Mumbai South',
    code: 'MH-31',
    state_code: 'IN-MH',
    state_name: 'Maharashtra',
    constituency_type: 'PARLIAMENTARY',
    total_voters: 1540000,
    total_booths: 1580,
    reserved_category: 'GENERAL',
    phase: 5,
  },
  {
    id: 'const-007',
    name: 'Diamond Harbour',
    code: 'WB-21',
    state_code: 'IN-WB',
    state_name: 'West Bengal',
    constituency_type: 'PARLIAMENTARY',
    total_voters: 1720000,
    total_booths: 1810,
    reserved_category: 'GENERAL',
    phase: 7,
  },
  {
    id: 'const-008',
    name: 'Chennai Central',
    code: 'TN-04',
    state_code: 'IN-TN',
    state_name: 'Tamil Nadu',
    constituency_type: 'PARLIAMENTARY',
    total_voters: 1380000,
    total_booths: 1400,
    reserved_category: 'GENERAL',
    phase: 1,
  },
];

export const initialElections: Election[] = [
  {
    id: 'elec-2026-gen',
    title: 'General Election 2026 (19th Lok Sabha)',
    election_type: 'GENERAL',
    start_date: '2026-04-19',
    end_date: '2026-06-04',
    status: 'ACTIVE',
    total_registered_voters: 968800000,
    turnout_percentage: 67.4,
    total_constituencies: 543,
    phases: 7,
  },
  {
    id: 'elec-2026-dl-asm',
    title: 'Delhi Legislative Assembly Election 2026',
    election_type: 'ASSEMBLY',
    start_date: '2026-02-08',
    end_date: '2026-02-15',
    status: 'COMPLETED',
    total_registered_voters: 15200000,
    turnout_percentage: 63.8,
    total_constituencies: 70,
    phases: 1,
  },
  {
    id: 'elec-2026-wb-asm',
    title: 'West Bengal State Assembly Election 2026',
    election_type: 'ASSEMBLY',
    start_date: '2026-03-27',
    end_date: '2026-04-29',
    status: 'SCHEDULED',
    total_registered_voters: 73500000,
    turnout_percentage: 0,
    total_constituencies: 294,
    phases: 8,
  },
  {
    id: 'elec-2026-by-up',
    title: 'Uttar Pradesh Parliamentary By-Election 2026',
    election_type: 'BY_ELECTION',
    start_date: '2026-07-10',
    end_date: '2026-07-14',
    status: 'SCHEDULED',
    total_registered_voters: 1890000,
    turnout_percentage: 0,
    total_constituencies: 1,
    phases: 1,
  },
];

export const initialCandidates: Candidate[] = [
  {
    id: 'cand-001',
    name: 'Narendra Modi',
    age: 75,
    email: 'pmo@nic.in',
    phone: '+919811000001',
    constituency_id: 'const-001',
    party_id: 'party-bjp',
    education: 'M.A. Political Science (Gujarat Univ)',
    declared_assets_cr: 3.02,
    criminal_cases: 0,
    affidavit_status: 'VERIFIED',
    submission_date: '2026-04-10',
  },
  {
    id: 'cand-002',
    name: 'Ajay Rai',
    age: 56,
    email: 'ajay.rai@inc.org',
    phone: '+919811000002',
    constituency_id: 'const-001',
    party_id: 'party-inc',
    education: 'Graduate (Varanasi)',
    declared_assets_cr: 2.85,
    criminal_cases: 2,
    affidavit_status: 'VERIFIED',
    submission_date: '2026-04-11',
  },
  {
    id: 'cand-003',
    name: 'Rahul Gandhi',
    age: 55,
    email: 'rg@inc.org',
    phone: '+919811000003',
    constituency_id: 'const-002',
    party_id: 'party-inc',
    education: 'M.Phil Development Studies (Trinity College)',
    declared_assets_cr: 20.4,
    criminal_cases: 1,
    affidavit_status: 'VERIFIED',
    submission_date: '2026-04-05',
  },
  {
    id: 'cand-004',
    name: 'K. Surendran',
    age: 54,
    email: 'k.surendran@bjp.org',
    phone: '+919811000004',
    constituency_id: 'const-002',
    party_id: 'party-bjp',
    education: 'B.Sc. Chemistry',
    declared_assets_cr: 0.65,
    criminal_cases: 4,
    affidavit_status: 'VERIFIED',
    submission_date: '2026-04-06',
  },
  {
    id: 'cand-005',
    name: 'Bansuri Swaraj',
    age: 42,
    email: 'bansuri@bjp.org',
    phone: '+919811000005',
    constituency_id: 'const-003',
    party_id: 'party-bjp',
    education: 'Barrister-at-Law (Inns of Court, Oxford)',
    declared_assets_cr: 19.3,
    criminal_cases: 0,
    affidavit_status: 'VERIFIED',
    submission_date: '2026-04-15',
  },
  {
    id: 'cand-006',
    name: 'Somnath Bharti',
    age: 51,
    email: 'somnath@aamaadmiparty.org',
    phone: '+919811000006',
    constituency_id: 'const-003',
    party_id: 'party-aap',
    education: 'LL.B. (Delhi University), M.Sc. (IIT Delhi)',
    declared_assets_cr: 4.8,
    criminal_cases: 1,
    affidavit_status: 'VERIFIED',
    submission_date: '2026-04-14',
  },
  {
    id: 'cand-007',
    name: 'Amit Shah',
    age: 61,
    email: 'amit.shah@bjp.org',
    phone: '+919811000007',
    constituency_id: 'const-004',
    party_id: 'party-bjp',
    education: 'B.Sc. Biochemistry (CU Shah Science College)',
    declared_assets_cr: 65.5,
    criminal_cases: 0,
    affidavit_status: 'VERIFIED',
    submission_date: '2026-04-12',
  },
  {
    id: 'cand-008',
    name: 'Tejasvi Surya',
    age: 35,
    email: 'tejasvi@bjp.org',
    phone: '+919811000008',
    constituency_id: 'const-005',
    party_id: 'party-bjp',
    education: 'LL.B. (Bangalore Institute of Legal Studies)',
    declared_assets_cr: 4.1,
    criminal_cases: 0,
    affidavit_status: 'VERIFIED',
    submission_date: '2026-04-08',
  },
  {
    id: 'cand-009',
    name: 'Abhishek Banerjee',
    age: 38,
    email: 'abhishek@aitc.org',
    phone: '+919811000009',
    constituency_id: 'const-007',
    party_id: 'party-aitc',
    education: 'MBA (Indian Institute of Planning and Management)',
    declared_assets_cr: 15.2,
    criminal_cases: 0,
    affidavit_status: 'VERIFIED',
    submission_date: '2026-04-18',
  },
  {
    id: 'cand-010',
    name: 'Dayanidhi Maran',
    age: 59,
    email: 'd.maran@dmk.org',
    phone: '+919811000010',
    constituency_id: 'const-008',
    party_id: 'party-dmk',
    education: 'B.A. Economics (Loyola College, Chennai)',
    declared_assets_cr: 38.6,
    criminal_cases: 0,
    affidavit_status: 'VERIFIED',
    submission_date: '2026-03-25',
  },
];

export const initialElectionResults: ElectionResult[] = [
  {
    result_key: 'res-varanasi-2026',
    election_id: 'elec-2026-gen',
    constituency_id: 'const-001',
    winning_candidate_id: 'cand-001',
    total_votes: 1124500,
    candidate_votes: {
      'cand-001': 612970,
      'cand-002': 460457,
    },
    margin: 152513,
    is_declared: true,
    declaration_time: '2026-06-04T18:30:00Z',
  },
  {
    result_key: 'res-wayanad-2026',
    election_id: 'elec-2026-gen',
    constituency_id: 'const-002',
    winning_candidate_id: 'cand-003',
    total_votes: 1045200,
    candidate_votes: {
      'cand-003': 647445,
      'cand-004': 283000,
    },
    margin: 364445,
    is_declared: true,
    declaration_time: '2026-06-04T17:45:00Z',
  },
  {
    result_key: 'res-newdelhi-2026',
    election_id: 'elec-2026-gen',
    constituency_id: 'const-003',
    winning_candidate_id: 'cand-005',
    total_votes: 895000,
    candidate_votes: {
      'cand-005': 483120,
      'cand-006': 404880,
    },
    margin: 78240,
    is_declared: true,
    declaration_time: '2026-06-04T19:15:00Z',
  },
];

export const initialRegionalTurnout: RegionalTurnout[] = [
  {
    region: 'Northern Zone',
    pollingBooths: 260000,
    voterTurnoutPercent: 68.2,
    phaseStatus: 'COMPLETED',
    totalVoters: '245.2M',
  },
  {
    region: 'Southern Zone',
    pollingBooths: 240000,
    voterTurnoutPercent: 71.5,
    phaseStatus: 'COMPLETED',
    totalVoters: '215.8M',
  },
  {
    region: 'Eastern Zone',
    pollingBooths: 220000,
    voterTurnoutPercent: 65.8,
    phaseStatus: 'COMPLETED',
    totalVoters: '198.4M',
  },
  {
    region: 'Western Zone',
    pollingBooths: 210000,
    voterTurnoutPercent: 66.1,
    phaseStatus: 'COMPLETED',
    totalVoters: '189.6M',
  },
  {
    region: 'Central Zone',
    pollingBooths: 118000,
    voterTurnoutPercent: 64.9,
    phaseStatus: 'COMPLETED',
    totalVoters: '119.8M',
  },
];

export const initialETLBatches: ETLBatch[] = [
  {
    id: 'Batch-8841',
    sourceFile: 'general_election_2026_results.csv',
    recordsCount: '543 seats',
    provenance: 'ECI Official Feed',
    status: 'LOADED',
    importedAt: '2026-07-23 16:50',
  },
  {
    id: 'Batch-8840',
    sourceFile: 'candidate_affidavits_2026.json',
    recordsCount: '8,420 records',
    provenance: 'MyNeta Ingestion',
    status: 'LOADED',
    importedAt: '2026-07-23 15:20',
  },
  {
    id: 'Batch-8839',
    sourceFile: 'booth_turnout_phase1.csv',
    recordsCount: '260,000 booths',
    provenance: 'Chief Electoral Officer',
    status: 'LOADED',
    importedAt: '2026-07-23 13:40',
  },
  {
    id: 'Batch-8838',
    sourceFile: 'gis_constituency_boundaries_v3.geojson',
    recordsCount: '543 polygons',
    provenance: 'Survey of India / ECI GIS',
    status: 'LOADED',
    importedAt: '2026-07-22 18:00',
  },
];

// In-Memory Global Singleton State
class ElectionPlatformStore {
  healthMetrics: SystemHealthMetrics = { ...initialHealthMetrics };
  kpis: ExecutiveKpis = { ...initialExecutiveKpis };
  featureFlags: FeatureFlag[] = [...initialFeatureFlags];
  auditLogs: AuditLog[] = [...initialAuditLogs];
  userAccounts: UserAccount[] = [...initialUserAccounts];
  elections: Election[] = [...initialElections];
  constituencies: Constituency[] = [...initialConstituencies];
  parties: Party[] = [...initialParties];
  candidates: Candidate[] = [...initialCandidates];
  results: ElectionResult[] = [...initialElectionResults];
  regionalTurnout: RegionalTurnout[] = [...initialRegionalTurnout];
  etlBatches: ETLBatch[] = [...initialETLBatches];

  toggleFeatureFlag(flagName: string): FeatureFlag[] {
    this.featureFlags = this.featureFlags.map((flag) =>
      flag.name === flagName ? { ...flag, enabled: !flag.enabled } : flag
    );
    this.addAuditLog('superadmin', 'UPDATE_FEATURE_FLAG', `feature_flags/${flagName}`);
    return this.featureFlags;
  }

  addElection(election: Omit<Election, 'id'>): Election {
    const id = `elec-${Date.now().toString(36)}`;
    const newElection: Election = { ...election, id };
    this.elections.unshift(newElection);
    this.kpis.totalElectionsManaged += 1;
    this.addAuditLog('superadmin', 'SCHEDULE_ELECTION', `elections/${id}`);
    return newElection;
  }

  addCandidate(candidate: Omit<Candidate, 'id' | 'submission_date'>): Candidate {
    const id = `cand-${Date.now().toString(36)}`;
    const newCandidate: Candidate = {
      ...candidate,
      id,
      submission_date: new Date().toISOString().split('T')[0],
    };
    this.candidates.push(newCandidate);
    this.kpis.totalCandidates += 1;
    this.addAuditLog('ops_lead', 'REGISTER_CANDIDATE', `candidates/${id}`);
    return newCandidate;
  }

  declareResult(result: ElectionResult): ElectionResult {
    const existingIndex = this.results.findIndex(
      (r) => r.constituency_id === result.constituency_id && r.election_id === result.election_id
    );
    if (existingIndex >= 0) {
      this.results[existingIndex] = result;
    } else {
      this.results.push(result);
    }
    this.addAuditLog('ops_lead', 'DECLARE_RESULT', `results/${result.result_key}`);
    return result;
  }

  addETLBatch(file: string, records: string, provenance: string): ETLBatch {
    const newBatch: ETLBatch = {
      id: `Batch-${8842 + this.etlBatches.length}`,
      sourceFile: file,
      recordsCount: records,
      provenance,
      status: 'LOADED',
      importedAt: new Date().toISOString().replace('T', ' ').substring(0, 16),
    };
    this.etlBatches.unshift(newBatch);
    this.addAuditLog('ops_lead', 'INGEST_ELECTION_DATA', `etl/${newBatch.id}`);
    return newBatch;
  }

  addAuditLog(actor: string, action: string, resource: string, status = 'SUCCESS') {
    const log: AuditLog = {
      id: `aud-${Date.now().toString(36)}`,
      timestamp: new Date().toISOString(),
      actor,
      action,
      resource,
      status,
      ipAddress: '127.0.0.1',
    };
    this.auditLogs.unshift(log);
  }

  search(queryStr: string): SearchHit[] {
    const q = queryStr.toLowerCase().trim();
    if (!q) return [];

    const hits: SearchHit[] = [];

    // Search elections
    for (const el of this.elections) {
      if (
        el.title.toLowerCase().includes(q) ||
        el.election_type.toLowerCase().includes(q) ||
        el.status.toLowerCase().includes(q)
      ) {
        hits.push({
          id: el.id,
          entity_type: 'election',
          title: el.title,
          subtitle: `${el.election_type} • Status: ${el.status} • ${el.total_constituencies} Seats`,
          score: 1.0,
          metadata: { election: el },
        });
      }
    }

    // Search constituencies
    for (const c of this.constituencies) {
      if (
        c.name.toLowerCase().includes(q) ||
        c.code.toLowerCase().includes(q) ||
        c.state_name.toLowerCase().includes(q)
      ) {
        hits.push({
          id: c.id,
          entity_type: 'constituency',
          title: `${c.name} (${c.code})`,
          subtitle: `${c.state_name} • ${c.total_voters.toLocaleString()} voters • Phase ${c.phase}`,
          score: 0.95,
          metadata: { constituency: c },
        });
      }
    }

    // Search candidates
    for (const cand of this.candidates) {
      const party = this.parties.find((p) => p.id === cand.party_id);
      const constObj = this.constituencies.find((c) => c.id === cand.constituency_id);
      if (
        cand.name.toLowerCase().includes(q) ||
        party?.name.toLowerCase().includes(q) ||
        party?.code.toLowerCase().includes(q) ||
        constObj?.name.toLowerCase().includes(q)
      ) {
        hits.push({
          id: cand.id,
          entity_type: 'candidate',
          title: cand.name,
          subtitle: `${party?.code ?? 'IND'} candidate for ${constObj?.name ?? 'Constituency'} • Assets: ₹${cand.declared_assets_cr} Cr`,
          score: 0.9,
          metadata: { candidate: cand, party, constituency: constObj },
        });
      }
    }

    // Search parties
    for (const party of this.parties) {
      if (
        party.name.toLowerCase().includes(q) ||
        party.code.toLowerCase().includes(q) ||
        party.symbol.toLowerCase().includes(q)
      ) {
        hits.push({
          id: party.id,
          entity_type: 'party',
          title: `${party.name} (${party.code})`,
          subtitle: `Symbol: ${party.symbol} • Won: ${party.seats_won} / ${party.seats_contested} seats contested`,
          score: 0.85,
          metadata: { party },
        });
      }
    }

    return hits;
  }
}

// Global variable attached to globalThis to preserve state in Next.js development HMR
const globalForStore = globalThis as unknown as {
  electionPlatformStore: ElectionPlatformStore | undefined;
};

export const store = globalForStore.electionPlatformStore ?? new ElectionPlatformStore();

if (process.env.NODE_ENV !== 'production') {
  globalForStore.electionPlatformStore = store;
}
