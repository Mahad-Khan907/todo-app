import { NextResponse } from 'next/server';

export async function GET() {
  try {
    // Basic health check - confirm the service is running
    return NextResponse.json({ status: 'ok', timestamp: new Date().toISOString() }, { status: 200 });
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : 'Unknown error';
    return NextResponse.json({ status: 'error', error: errorMessage }, { status: 500 });
  }
}