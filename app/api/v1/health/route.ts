import { NextResponse } from 'next/server';
import { store } from '@/lib/store';

export async function GET() {
  const metrics = store.healthMetrics;
  return NextResponse.json({
    status: 'HEALTHY',
    version: '1.0.0',
    timestamp: new Date().toISOString(),
    components: {
      database: {
        status: 'UP',
        type: 'PostgreSQL 16',
        active_connections: metrics.dbPoolActive,
        overflow: metrics.dbPoolOverflow,
      },
      cache: {
        status: 'UP',
        type: 'Redis 8.8',
        latency_ms: metrics.redisLatencyMs,
      },
      search_sal: {
        status: 'UP',
        type: 'Search Abstraction Layer',
        indexed_entities: 9540,
      },
      ai_provider_gateway: {
        status: 'UP',
        active_provider: 'Gemini / Cloud LLM',
        readiness: true,
      },
    },
    system: {
      cpu_percent: metrics.cpuUtilization,
      memory_percent: metrics.memoryUtilization,
      disk_free_gb: metrics.diskFreeGb,
      requests_per_sec: metrics.apiRequestsPerSec,
      p99_latency_ms: metrics.p99LatencyMs,
    },
  });
}
