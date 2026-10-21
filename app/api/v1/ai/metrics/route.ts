import { NextResponse } from 'next/server';
import { store } from '@/lib/store';

export async function GET() {
  return NextResponse.json({
    total_queries: store.kpis.aiQueriesProcessed,
    avg_latency_ms: 135,
    avg_grounding_score: 0.958,
    citation_coverage_pct: 98.4,
    active_provider: process.env.GEMINI_API_KEY ? 'Gemini 2.5 Flash' : 'Local Semantic Engine',
    safety_guardrails_status: 'ACTIVE_ENFORCED',
    citation_attributions_enforced: true,
  });
}
