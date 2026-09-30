'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useTranslation, LANGUAGES, LanguageCode } from '@/lib/i18n';
import { Leaf, Camera, Globe, Sparkles } from 'lucide-react';

export const Navbar: React.FC = () => {
  const pathname = usePathname();
  const { language, setLanguage, t } = useTranslation();

  const navItems = [
    { href: '/', label: t('nav.dashboard') },
    { href: '/crops', label: t('nav.crops') },
    { href: '/scan', label: t('nav.scan') },
    { href: '/treatment', label: t('nav.treatment') },
    { href: '/recovery', label: t('nav.recovery') },
    { href: '/weather', label: t('nav.weather') },
    { href: '/fertilizer', label: t('nav.fertilizer') },
    { href: '/assistant', label: t('nav.assistant') },
    { href: '/experts', label: t('nav.experts') },
    { href: '/admin', label: t('nav.admin') },
  ];

  return (
    <header className="sticky top-0 z-50 bg-emerald-950/95 backdrop-blur-md border-b border-emerald-800/60 text-white shadow-xl">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          
          {/* Logo & Brand */}
          <Link href="/" className="flex items-center space-x-3 group shrink-0">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-500 to-teal-400 p-2 text-emerald-950 shadow-md group-hover:scale-105 transition-transform flex items-center justify-center">
              <Leaf className="w-6 h-6 fill-current" />
            </div>
            <div>
              <span className="text-xl font-bold tracking-tight text-emerald-100 flex items-center gap-1.5">
                {t('appName')}
                <span className="text-[10px] font-bold uppercase tracking-wider bg-emerald-500/20 text-emerald-300 px-2 py-0.5 rounded-full border border-emerald-500/30">
                  AI
                </span>
              </span>
              <p className="text-[11px] text-emerald-400/80 hidden sm:block">
                {t('tagline')}
              </p>
            </div>
          </Link>

          {/* Desktop Navigation Links */}
          <nav className="hidden lg:flex items-center space-x-1 xl:space-x-1.5 overflow-x-auto py-1">
            {navItems.map((item) => {
              const isActive = pathname === item.href;
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`px-3 py-1.5 rounded-xl text-xs font-semibold whitespace-nowrap transition-all ${
                    isActive
                      ? 'bg-emerald-500 text-emerald-950 shadow-md font-bold'
                      : 'text-emerald-200/90 hover:text-white hover:bg-emerald-900/60'
                  }`}
                >
                  {item.label}
                </Link>
              );
            })}
          </nav>

          {/* Right Controls (Language Dropdown, Quick Scan) */}
          <div className="flex items-center space-x-3 shrink-0">
            
            {/* Language Selector */}
            <div className="relative flex items-center bg-emerald-900/80 border border-emerald-700/80 rounded-xl px-2.5 py-1.5 text-xs text-emerald-200 shadow-sm">
              <Globe className="w-4 h-4 mr-1.5 text-emerald-400 shrink-0" />
              <select
                value={language}
                onChange={(e) => setLanguage(e.target.value as LanguageCode)}
                className="bg-transparent border-none text-emerald-100 font-semibold focus:outline-none cursor-pointer text-xs"
              >
                {LANGUAGES.map((lang) => (
                  <option key={lang.code} value={lang.code} className="bg-emerald-950 text-white">
                    {lang.nativeName} ({lang.code.toUpperCase()})
                  </option>
                ))}
              </select>
            </div>

            {/* Quick Scan Button */}
            <Link
              href="/scan"
              className="hidden sm:inline-flex items-center space-x-1.5 bg-gradient-to-r from-emerald-500 to-teal-400 hover:from-emerald-400 hover:to-teal-300 text-emerald-950 font-bold px-3.5 py-1.5 rounded-xl shadow-md transition-all transform hover:scale-105 text-xs"
            >
              <Camera className="w-4 h-4" />
              <span>{t('dashboard.quickScan')}</span>
            </Link>

          </div>
        </div>
      </div>
    </header>
  );
};
