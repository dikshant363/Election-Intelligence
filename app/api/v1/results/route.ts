import { NextRequest, NextResponse } from 'next/server';
import { store } from '@/lib/store';

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const electionId = searchParams.get('election_id');
  const constituencyId = searchParams.get('constituency_id');

  let items = store.results;
  if (electionId) {
    items = items.filter((r) => r.election_id === electionId);
  }
  if (constituencyId) {
    items = items.filter((r) => r.constituency_id === constituencyId);
  }

  // Enrich with candidate and constituency names
  const enriched = items.map((res) => {
    const constituency = store.constituencies.find((c) => c.id === res.constituency_id);
    const winner = store.candidates.find((c) => c.id === res.winning_candidate_id);
    const winnerParty = store.parties.find((p) => p.id === winner?.party_id);
    return {
      ...res,
      constituency_name: constituency?.name,
      constituency_code: constituency?.code,
      winner_name: winner?.name,
      winner_party: winnerParty?.code,
      winner_party_color: winnerParty?.color,
    };
  });

  return NextResponse.json({
    items: enriched,
    total: enriched.length,
    page: 1,
    size: enriched.length,
    pages: 1,
  });
}

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    if (!body.election_id || !body.constituency_id || !body.candidate_votes) {
      return NextResponse.json(
        { error: 'Missing required fields (election_id, constituency_id, candidate_votes)' },
        { status: 400 }
      );
    }

    const votes = body.candidate_votes as Record<string, number>;
    const sorted = Object.entries(votes).sort((a, b) => b[1] - a[1]);
    const winnerId = sorted.length > 0 ? sorted[0][0] : undefined;
    const runnerUpVotes = sorted.length > 1 ? sorted[1][1] : 0;
    const winnerVotes = sorted.length > 0 ? sorted[0][1] : 0;
    const margin = winnerVotes - runnerUpVotes;
    const totalVotes = Object.values(votes).reduce((sum, v) => sum + v, 0);

    const saved = store.declareResult({
      result_key: `res-${body.constituency_id}-${Date.now().toString(36)}`,
      election_id: body.election_id,
      constituency_id: body.constituency_id,
      winning_candidate_id: body.winning_candidate_id || winnerId || '',
      total_votes: totalVotes,
      candidate_votes: votes,
      margin,
      is_declared: true,
      declaration_time: new Date().toISOString(),
    });

    return NextResponse.json(saved, { status: 201 });
  } catch (err: any) {
    return NextResponse.json({ error: err.message || 'Invalid payload' }, { status: 422 });
  }
}
