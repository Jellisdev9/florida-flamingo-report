import React from 'react';
import { TrendingUp, Home, Calendar, Building2, Gem, TrendingDown } from 'lucide-react';

export function MarketStrip() {
  const metrics = [
    {
      label: 'Miami Median Price',
      value: '$685,000',
      change: '+6.2%',
      isPositive: true,
      icon: Home
    },
    {
      label: 'Tampa Inventory',
      value: '3.1 Months',
      change: '-4.8%',
      isPositive: false,
      icon: Calendar
    },
    {
      label: 'Jacksonville Days on Market',
      value: '36 Days',
      change: '-2',
      isPositive: false,
      icon: TrendingDown
    },
    {
      label: 'Orlando Condo Activity',
      value: '1,248 Sales',
      change: '+9.1%',
      isPositive: true,
      icon: Building2
    },
    {
      label: 'Palm Beach Luxury Sales',
      value: '$10.4M Avg',
      change: '+11.3%',
      isPositive: true,
      icon: Gem
    }
  ];

  return (
    <div className="fpr-teal text-white w-full py-2 px-4 overflow-x-auto no-scrollbar border-t border-b border-gray-700/50 shadow-sm">
      <div className="max-w-7xl mx-auto flex items-center justify-between min-w-max gap-6">
        {metrics.map((metric, index) => {
          const Icon = metric.icon;
          return (
            <div key={index} className="flex flex-col gap-1 pr-6 border-r border-gray-600/50 last:border-0 last:pr-0">
              <div className="flex items-center gap-2 text-xs text-gray-300 uppercase tracking-wider font-semibold">
                <Icon className="w-3.5 h-3.5 text-gray-400" />
                {metric.label}
              </div>
              <div className="flex items-baseline gap-2">
                <span className="font-bold text-lg">{metric.value}</span>
                <span className={`text-sm font-semibold flex items-center gap-0.5 ${metric.isPositive ? 'fpr-green' : 'fpr-coral'}`}>
                  {metric.isPositive ? <TrendingUp className="w-3.5 h-3.5" /> : <TrendingDown className="w-3.5 h-3.5" />}
                  {metric.change}
                </span>
              </div>
              <div className="text-[10px] text-gray-400">vs. Apr 2024</div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
