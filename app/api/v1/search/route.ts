import { NextRequest, NextResponse } from 'next/server';
import { store } from '@/lib/store';

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const q = searchParams.get('q') || '';
  const page = parseInt(searchParams.get('page') || '1', 10);
  const pageSize = parseInt(searchParams.get('page_size') || '20', 10);

  const hits = store.search(q);
  const total = hits.length;
  const startIndex = (page - 1) * pageSize;
  const paginatedHits = hits.slice(startIndex, startIndex + pageSize);

  return NextResponse.json({
    hits: paginatedHits,
    total,
    page,
    page_size: pageSize,
    total_pages: Math.ceil(total / pageSize) || 1,
    query: q,
  });
}
