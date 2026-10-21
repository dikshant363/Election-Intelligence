import { NextRequest, NextResponse } from 'next/server';
import { store } from '@/lib/store';

export async function GET() {
  return NextResponse.json({
    batches: store.etlBatches,
    total: store.etlBatches.length,
  });
}

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const filename = body.filename || `electoral_import_${Date.now()}.csv`;
    const records = body.records || '500 records';
    const provenance = body.provenance || 'State Election Commission / Manual Upload';

    const batch = store.addETLBatch(filename, records, provenance);
    return NextResponse.json({ batch, success: true }, { status: 201 });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
