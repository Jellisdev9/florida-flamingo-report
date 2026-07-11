import React from 'react';
import { TrendingUp, TrendingDown } from 'lucide-react';
import { useMarketMetrics } from '@/hooks/useApi';

export function MarketStrip() {
  const { data: metrics = [] } = useMarketMetrics();

  return (
    <div className="fpr-teal text-white w-full py-2 px-4 overflow-x-auto no-scrollbar border-t border-b border-gray-700/50 shadow-sm">
      <div className="max-w-7xl mx-auto flex items-center justify-between min-w-max gap-6">
        {metrics.map((metric, index) => (
          <div key={index} className="flex flex-col gap-1 pr-6 border-r border-gray-600/50 last:border-0 last:pr-0">
            <div className="flex items-center gap-2 text-xs text-gray-300 uppercase tracking-wider font-semibold">
              {metric.city} {metric.metric_label}
            </div>
            <div className="flex items-baseline gap-2">
              <span className="font-bold text-lg">{metric.value_display}</span>
              <span className={`text-sm font-semibold flex items-center gap-0.5 ${metric.is_positive ? 'fpr-green' : 'fpr-coral'}`}>
                {metric.is_positive
                  ? <TrendingUp className="w-3.5 h-3.5" />
                  : <TrendingDown className="w-3.5 h-3.5" />}
                {metric.change_display}
              </span>
            </div>
            <div className="text-[10px] text-gray-400">vs. Apr 2024</div>
          </div>
        ))}
      </div>
    </div>
  );
}
