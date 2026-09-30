import type { Metadata } from 'next';
import './globals.css';
import { LanguageProvider } from '@/lib/i18n';
import { Navbar } from '@/components/Navbar';
import { MobileNav } from '@/components/MobileNav';

export const metadata: Metadata = {
  title: 'PhytoVeyra AI – Multilingual AI Plant Health, Treatment & Recovery Platform',
  description: 'Production-quality AI agricultural platform for plant disease diagnosis, context-aware treatment, recovery tracking, and voice interaction.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-emerald-950 text-emerald-50 min-h-screen font-sans antialiased selection:bg-emerald-500 selection:text-emerald-950 flex flex-col">
        <LanguageProvider>
          <Navbar />
          <main className="flex-grow max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 pb-24 lg:pb-12">
            {children}
          </main>
          <MobileNav />
        </LanguageProvider>
      </body>
    </html>
  );
}
