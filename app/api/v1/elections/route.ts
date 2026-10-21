import { NextRequest, NextResponse } from 'next/server';
import { store } from '@/lib/store';

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const statusFilter = searchParams.get('status');
  const typeFilter = searchParams.get('type');

  let items = store.elections;
  if (statusFilter) {
    items = items.filter((e) => e.status.toLowerCase() === statusFilter.toLowerCase());
  }
  if (typeFilter) {
    items = items.filter((e) => e.election_type.toLowerCase() === typeFilter.toLowerCase());
  }

  return NextResponse.json({
    items,
    total: items.length,
    page: 1,
    size: items.length,
    pages: 1,
  });
}

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    if (!body.title || !body.election_type || !body.start_date || !body.end_date) {
      return NextResponse.json(
        { error: 'Missing required election fields (title, election_type, start_date, end_date)' },
        { status: 400 }
      );
    }

    const created = store.addElection({
      title: body.title,
      election_type: body.election_type,
      start_date: body.start_date,
      end_date: body.end_date,
      status: body.status || 'SCHEDULED',
      total_registered_voters: Number(body.total_registered_voters) || 1500000,
      turnout_percentage: 0,
      total_constituencies: Number(body.total_constituencies) || 1,
      phases: Number(body.phases) || 1,
    });

    return NextResponse.json(created, { status: 201 });
  } catch (err: any) {
    return NextResponse.json({ error: err.message || 'Invalid payload' }, { status: 422 });
  }
}
