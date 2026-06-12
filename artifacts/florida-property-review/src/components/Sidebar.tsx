import React from 'react';
import { TrendingUp, TrendingDown } from 'lucide-react';
import { Link } from 'wouter';

export function TopMarketsSidebar() {
  const markets = [
    { name: 'Miami', metric: '$685K', change: '+6.2%', isPos: true },
    { name: 'Palm Beach', metric: '$10.4M', change: '+11.3%', isPos: true },
    { name: 'Tampa', metric: '$415K', change: '-2.1%', isPos: false },
    { name: 'Orlando', metric: '$390K', change: '+4.5%', isPos: true },
    { name: 'Jacksonville', metric: '$345K', change: '-1.8%', isPos: false },
  ];

  return (
    <div className="bg-white border border-gray-200 rounded-sm p-5 shadow-sm h-fit">
      <div className="flex items-center justify-between mb-4 pb-2 border-b-2 border-[#0d1b2a]">
        <h3 className="font-serif font-bold text-lg">Top Markets</h3>
        <span className="text-xs text-gray-500 uppercase tracking-wider font-semibold">Trend</span>
      </div>
      <div className="flex flex-col gap-4">
        {markets.map((market, i) => (
          <div key={i} className="flex items-center justify-between group cursor-pointer">
            <div className="flex flex-col">
              <span className="font-semibold text-gray-900 group-hover:fpr-gold transition-colors">{market.name}</span>
              <span className="text-sm text-gray-500">{market.metric} Avg</span>
            </div>
            <div className={`flex items-center gap-1 font-bold ${market.isPos ? 'fpr-green' : 'fpr-coral'}`}>
              {market.isPos ? <TrendingUp className="w-4 h-4" /> : <TrendingDown className="w-4 h-4" />}
              {market.change}
            </div>
          </div>
        ))}
      </div>
      <Link href="/notable-sales" className="mt-6 block w-full text-center text-sm font-bold fpr-navy text-white py-2.5 rounded-sm hover:bg-[#0f4c5c] transition-colors">
        VIEW FULL REPORT →
      </Link>
    </div>
  );
}

export function NewsletterCompact() {
  return (
    <div className="fpr-navy text-white rounded-sm p-6 mt-6 shadow-sm">
      <h3 className="font-serif font-bold text-xl mb-2 text-center">Stay ahead of the market.</h3>
      <p className="text-sm text-gray-300 text-center mb-4">Get the latest Florida real estate intelligence delivered weekly.</p>
      <div className="flex flex-col gap-2">
        <input 
          type="email" 
          placeholder="Email address" 
          className="w-full px-3 py-2 text-gray-900 rounded-sm focus:outline-none focus:ring-2 focus:ring-[#d4a817]"
        />
        <button className="w-full fpr-gold-bg text-black font-bold py-2 rounded-sm hover:bg-yellow-500 transition-colors">
          SUBSCRIBE
        </button>
      </div>
      <p className="text-[10px] text-gray-400 text-center mt-3">No spam. Unsubscribe anytime.</p>
    </div>
  );
}

export function TopAgentsSidebar() {
  const agents = [
    { rank: 1, name: 'The Jills Zeder Group', location: 'Miami Beach', volume: '$98.4M' },
    { rank: 2, name: 'Corcoran Reverie Group', location: 'Naples', volume: '$72.1M' },
    { rank: 3, name: 'Compass Florida Group', location: 'Miami', volume: '$65.7M' },
  ];

  return (
    <div className="bg-white border border-gray-200 rounded-sm p-5 shadow-sm h-full">
      <div className="flex items-center justify-between mb-4 pb-2 border-b-2 border-[#0d1b2a]">
        <h3 className="font-serif font-bold text-lg">Top Agents This Month</h3>
      </div>
      <div className="flex flex-col gap-5">
        {agents.map((agent) => (
          <div key={agent.rank} className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center font-serif font-bold text-lg fpr-navy text-white shrink-0">
              {agent.rank}
            </div>
            <div className="flex flex-col">
              <span className="font-bold text-sm text-gray-900">{agent.name}</span>
              <span className="text-xs text-gray-500">{agent.location} &middot; {agent.volume}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
