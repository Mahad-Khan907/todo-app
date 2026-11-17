import '@/styles/globals.css';
import type { Metadata } from 'next';
import Providers from '@/components/Providers';
import AuthProviderWrapper from '@/components/AuthProviderWrapper';

export const metadata: Metadata = {
  title: 'TaskFlow AI — Autonomous Todo & Workflow Assistant',
  description: 'AI-powered task management with OpenRouter Particle AI, recurring schedules, and smart email reminders.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <Providers>
          <AuthProviderWrapper>
            {children}
          </AuthProviderWrapper>
        </Providers>
      </body>
    </html>
  );
}