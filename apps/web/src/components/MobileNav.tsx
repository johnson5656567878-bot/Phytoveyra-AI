'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useTranslation } from '@/lib/i18n';
import { Home, Sprout, Camera, Bot, User } from 'lucide-react';

export const MobileNav: React.FC = () => {
  const pathname = usePathname();
  const { t } = useTranslation();

  const items = [
    { href: '/', label: t('nav.dashboard'), icon: Home },
    { href: '/crops', label: t('nav.crops'), icon: Sprout },
    { href: '/scan', label: t('nav.scan'), icon: Camera, isProminent: true },
    { href: '/assistant', label: t('nav.assistant'), icon: Bot },
    { href: '/admin', label: t('nav.admin'), icon: User }
  ];

  return (
    <div className="lg:hidden fixed bottom-0 left-0 right-0 z-50 bg-emerald-950/95 backdrop-blur-md border-t border-emerald-800/60 px-4 py-2 shadow-2xl">
      <div className="flex items-center justify-around">
        {items.map((item) => {
          const Icon = item.icon;
          const isActive = pathname === item.href;

          if (item.isProminent) {
            return (
              <Link
                key={item.href}
                href={item.href}
                className="flex flex-col items-center -mt-6 group"
              >
                <div className="w-14 h-14 rounded-full bg-gradient-to-tr from-emerald-500 to-teal-300 p-3 text-emerald-950 shadow-xl border-4 border-emerald-950 group-active:scale-95 transition-all flex items-center justify-center">
                  <Camera className="w-7 h-7 stroke-[2.5]" />
                </div>
                <span className="text-[10px] font-bold text-emerald-400 mt-1">
                  {item.label}
                </span>
              </Link>
            );
          }

          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex flex-col items-center py-1 px-2 rounded-lg transition-colors ${
                isActive ? 'text-emerald-400 font-bold' : 'text-emerald-300/70 hover:text-emerald-200'
              }`}
            >
              <Icon className="w-5 h-5" />
              <span className="text-[10px] mt-0.5">{item.label}</span>
            </Link>
          );
        })}
      </div>
    </div>
  );
};
