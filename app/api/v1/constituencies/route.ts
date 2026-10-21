import { NextRequest, NextResponse } from 'next/server';
import { store } from '@/lib/store';

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const stateCode = searchParams.get('state_code');

  let items = store.constituencies;
  if (stateCode) {
    items = items.filter((c) => c.state_code === stateCode);
  }

  return NextResponse.json({
    items,
    total: items.length,
    page: 1,
    size: items.length,
    pages: 1,
  });
}
