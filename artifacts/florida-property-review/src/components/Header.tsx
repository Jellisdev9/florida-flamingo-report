import React from 'react';
import { Link, useLocation } from 'wouter';
import { Search, TrendingUp, TrendingDown, Home, Calendar, Building2, Gem } from 'lucide-react';
import { MarketStrip } from './MarketStrip';

export function Header() {
  const [location] = useLocation();

  const navLinks = [
    { name: 'Home', href: '/' },
    { name: 'Notable Sales', href: '/notable-sales' },
    { name: 'Market Pulse', href: '#' },
    { name: 'Agents', href: '#' },
    { name: 'Neighborhoods', href: '#' },
    { name: 'Submit a Deal', href: '#' },
    { name: 'About', href: '#' },
  ];

  return (
    <header className="w-full">
      <div className="fpr-navy text-white px-4 md:px-8 py-4">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex flex-col items-center md:items-start text-center md:text-left gap-1">
            <Link href="/" className="flex items-center gap-3 group">
              <div className="fpr-gold-bg text-black font-bold text-xl px-2 py-1 flex items-center justify-center h-10 w-10">
                FPR
              </div>
              <div>
                <h1 className="font-serif text-2xl md:text-3xl font-bold tracking-tight">Florida Property Review</h1>
                <p className="text-gray-400 text-xs md:text-sm tracking-wide hidden md:block">
                  Notable sales, agent moves, market trends, and neighborhood intelligence across Florida.
                </p>
              </div>
            </Link>
          </div>
          
          <div className="flex items-center gap-6 mt-2 md:mt-0 w-full md:w-auto overflow-x-auto pb-2 md:pb-0">
            <nav className="flex items-center gap-6 whitespace-nowrap text-sm font-medium">
              {navLinks.map((link) => {
                const isActive = location === link.href || (link.href !== '/' && location.startsWith(link.href));
                return (
                  <Link 
                    key={link.name} 
                    href={link.href}
                    className={`pb-1 border-b-2 transition-colors ${isActive ? 'border-[#d4a817] fpr-gold' : 'border-transparent text-gray-300 hover:text-white'}`}
                  >
                    {link.name}
                  </Link>
                );
              })}
            </nav>
            <button className="text-gray-300 hover:text-white ml-auto md:ml-0" data-testid="button-search">
              <Search className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>
      <MarketStrip />
    </header>
  );
}
