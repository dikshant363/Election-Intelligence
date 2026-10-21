import { NextResponse } from 'next/server';

export async function GET() {
  return NextResponse.json({
    name: 'Election Intelligence Platform',
    version: '1.0.0',
    framework: 'Next.js 15 App Router',
    environment: process.env.NODE_ENV || 'development',
    runtime: 'Node.js 22',
  });
}
