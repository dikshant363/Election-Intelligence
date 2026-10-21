import { NextResponse } from 'next/server';
import { store } from '@/lib/store';

export async function GET() {
  return NextResponse.json({
    items: store.parties,
    total: store.parties.length,
    page: 1,
    size: store.parties.length,
    pages: 1,
  });
}
