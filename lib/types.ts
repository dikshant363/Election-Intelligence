export type ControlInterface =
  | 'enterpriseControlCenter'
  | 'executiveCommandCenter'
  | 'operationsConsole'
  | 'publicPortal';

export type ElectionType = 'GENERAL' | 'ASSEMBLY' | 'BY_ELECTION' | 'MUNICIPAL';
export type ElectionStatus = 'SCHEDULED' | 'ACTIVE' | 'COMPLETED' | 'CANCELLED';

export interface Election {
  id: string;
  title: string;
  election_type: ElectionType;
  start_date: string;
  end_date: string;
  status: ElectionStatus;
  total_registered_voters: number;
  turnout_percentage: number;
  total_constituencies: number;
  phases: number;
}

export interface Constituency {
  id: string;
  name: string;
  code: string;
  state_code: string;
  state_name: string;
  constituency_type: 'PARLIAMENTARY' | 'ASSEMBLY';
  total_voters: number;
  total_booths: number;
  reserved_category: 'GENERAL' | 'SC' | 'ST';
  phase: number;
}

export interface Party {
  id: string;
  name: string;
  code: string;
  symbol: string;
  color: string;
  founded_year: number;
  seats_contested: number;
  seats_won: number;
}

export interface Candidate {
  id: string;
  name: string;
  age: number;
  email: string;
  phone: string;
  constituency_id: string;
  party_id: string;
  education: string;
  declared_assets_cr: number;
  criminal_cases: number;
  affidavit_status: 'VERIFIED' | 'UNDER_REVIEW' | 'FLAGGED';
  submission_date: string;
}

export interface PollingBooth {
  id: string;
  constituency_id: string;
  booth_number: number;
  booth_name: string;
  location: string;
  registered_voters: number;
  votes_polled: number;
  evm_serial: string;
  status: 'NORMAL' | 'SENSITIVE' | 'HYPER_SENSITIVE';
}

export interface ElectionResult {
  result_key: string;
  election_id: string;
  constituency_id: string;
  winning_candidate_id: string;
  total_votes: number;
  candidate_votes: Record<string, number>;
  margin: number;
  is_declared: boolean;
  declaration_time: string;
}

export interface SystemHealthMetrics {
  cpuUtilization: number;
  memoryUtilization: number;
  diskFreeGb: number;
  dbPoolActive: number;
  dbPoolOverflow: number;
  redisLatencyMs: number;
  apiRequestsPerSec: number;
  p99LatencyMs: number;
}

export interface FeatureFlag {
  name: string;
  enabled: boolean;
  description: string;
  environment: string;
}

export interface UserAccount {
  id: string;
  username: string;
  email: string;
  role: string;
  isActive: boolean;
  mfaEnabled: boolean;
  lastLogin: string;
}

export interface AuditLog {
  id: string;
  timestamp: string;
  actor: string;
  action: string;
  resource: string;
  status: string;
  ipAddress: string;
}

export interface ExecutiveKpis {
  totalElectionsManaged: number;
  totalVotersRegistered: number;
  averageTurnoutPercent: number;
  totalConstituencies: number;
  totalCandidates: number;
  totalPollingBooths: number;
  aiQueriesProcessed: number;
  platformUptimePercent: number;
}

export interface RegionalTurnout {
  region: string;
  pollingBooths: number;
  voterTurnoutPercent: number;
  phaseStatus: 'COMPLETED' | 'IN_PROGRESS' | 'SCHEDULED';
  totalVoters: string;
}

export interface ETLBatch {
  id: string;
  sourceFile: string;
  recordsCount: string;
  provenance: string;
  status: 'LOADED' | 'PROCESSING' | 'VALIDATED' | 'FAILED';
  importedAt: string;
}

export interface AIProviderInfo {
  provider_name: string;
  is_active: boolean;
  latency_ms: number;
  model: string;
  max_context_tokens: number;
}

export interface AIMetrics {
  total_queries: number;
  avg_latency_ms: number;
  avg_grounding_score: number;
  citation_coverage_pct: number;
  active_provider: string;
}

export interface SearchHit {
  id: string;
  entity_type: 'election' | 'candidate' | 'constituency' | 'party' | 'booth';
  title: string;
  subtitle: string;
  highlight?: string;
  score: number;
  metadata: Record<string, any>;
}

export interface DatasetChecksumRecord {
  id: string;
  datasetName: string;
  storageLayerPath: string;
  recordCount: number;
  sizeBytes: number;
  expectedChecksum: string;
  computedChecksum: string;
  status: 'VERIFIED' | 'TAMPERED';
  algorithm: 'SHA-256';
  lastValidatedAt: string;
  anomalyDetails?: string;
}

export interface ChecksumValidationReport {
  scanId: string;
  timestamp: string;
  totalDatasetsScanned: number;
  verifiedCount: number;
  anomaliesCount: number;
  overallStatus: 'SECURE' | 'TAMPER_DETECTED' | 'IN_PROGRESS';
  merkleRootHash: string;
  durationMs: number;
  records: DatasetChecksumRecord[];
}
