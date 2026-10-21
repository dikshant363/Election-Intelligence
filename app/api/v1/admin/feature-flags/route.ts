import { NextRequest, NextResponse } from 'next/server';
import { store } from '@/lib/store';

export async function GET() {
  return NextResponse.json({
    flags: store.featureFlags,
    total: store.featureFlags.length,
  });
}

export async function PATCH(req: NextRequest) {
  try {
    const body = await req.json();
    const { name } = body;
    if (!name) {
      return NextResponse.json({ error: 'Flag name is required' }, { status: 400 });
    }

    const updatedFlags = store.toggleFeatureFlag(name);
    return NextResponse.json({ flags: updatedFlags, success: true });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
