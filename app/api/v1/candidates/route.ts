import { NextRequest, NextResponse } from 'next/server';
import { store } from '@/lib/store';

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const constituencyId = searchParams.get('constituency_id');
  const partyId = searchParams.get('party_id');

  let items = store.candidates;
  if (constituencyId) {
    items = items.filter((c) => c.constituency_id === constituencyId);
  }
  if (partyId) {
    items = items.filter((c) => c.party_id === partyId);
  }

  // Populate party and constituency details
  const enriched = items.map((c) => {
    const party = store.parties.find((p) => p.id === c.party_id);
    const constituency = store.constituencies.find((con) => con.id === c.constituency_id);
    return {
      ...c,
      party_name: party?.name,
      party_code: party?.code,
      party_symbol: party?.symbol,
      party_color: party?.color,
      constituency_name: constituency?.name,
      state_name: constituency?.state_name,
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
    if (!body.name || !body.age || !body.email || !body.phone || !body.constituency_id) {
      return NextResponse.json(
        { error: 'Missing required candidate fields (name, age, email, phone, constituency_id)' },
        { status: 400 }
      );
    }

    const created = store.addCandidate({
      name: body.name,
      age: Number(body.age),
      email: body.email,
      phone: body.phone,
      constituency_id: body.constituency_id,
      party_id: body.party_id || 'party-ind',
      education: body.education || 'Graduate',
      declared_assets_cr: Number(body.declared_assets_cr) || 1.5,
      criminal_cases: Number(body.criminal_cases) || 0,
      affidavit_status: body.affidavit_status || 'VERIFIED',
    });

    return NextResponse.json(created, { status: 201 });
  } catch (err: any) {
    return NextResponse.json({ error: err.message || 'Invalid payload' }, { status: 422 });
  }
}
