import { NextResponse } from 'next/server';
import { store } from '@/lib/store';

export async function GET() {
  return NextResponse.json({
    items: store.auditLogs,
    total: store.auditLogs.length,
  });
}
