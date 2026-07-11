import React, { useState } from 'react';
import { Header } from '@/components/Header';
import { Link } from 'wouter';
import { MapPin, Calendar, Bell } from 'lucide-react';
import { motion } from 'framer-motion';
import {
  useFeaturedSale,
  useSales,
  useTopClosings,
  useFastestGrowingMarkets,
  useSubscribe,
} from '@/hooks/useApi';
import { formatDate, REGION_MAP } from '@/lib/api';

const TABS = ['All Regions', 'South Florida', 'Tampa Bay', 'Orlando', 'Jacksonville', 'Panhandle'];

const TYPE_LABELS: Record<string, string> = {
  WATERFRONT_ESTATE: 'WATERFRONT ESTATE',
  CONDO_PENTHOUSE: 'CONDO PENTHOUSE',
  CONDO_RESIDENCE: 'CONDO RESIDENCE',
  COMMERCIAL: 'COMMERCIAL',
  SINGLE_FAMILY: 'SINGLE FAMILY',
};

export function NotableSalesPage() {
  const [activeTab, setActiveTab] = useState('All Regions');
  const region = REGION_MAP[activeTab];

  const { data: featuredSale } = useFeaturedSale();
  const { data: salesPage } = useSales(region || undefined);
  const { data: topClosings = [] } = useTopClosings();
  const { data: fastestGrowing = [] } = useFastestGrowingMarkets();
  const sales = salesPage?.results ?? [];

  const [email, setEmail] = useState('');
  const [subscribed, setSubscribed] = useState(false);
  const subscribe = useSubscribe();

  const handleSubscribe = () => {
    if (!email) return;
    subscribe.mutate(email, { onSuccess: () => { setSubscribed(true); setEmail(''); } });
  };

  return (
    <div className="min-h-screen bg-[#f4f5f7] flex flex-col font-sans">
      <Header />

      <div className="w-full bg-white border-b border-gray-200 py-8 px-4 md:px-8">
        <div className="max-w-7xl mx-auto flex flex-col gap-2">
          <h1 className="font-serif text-4xl md:text-5xl font-bold text-[#0d1b2a]">Notable Sales</h1>
          <p className="text-lg text-gray-500">The biggest closings. The most exclusive addresses. Across Florida.</p>
        </div>
      </div>

      <main className="flex-1 w-full max-w-7xl mx-auto px-4 md:px-8 py-8 flex flex-col gap-8">

        {/* Region Filter Tabs */}
        <div className="flex items-center gap-4 overflow-x-auto no-scrollbar pb-2">
          {TABS.map(tab => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`whitespace-nowrap px-4 py-2 rounded-full text-sm font-bold transition-all ${
                activeTab === tab
                  ? 'bg-[#0d1b2a] text-white border-b-2 border-[#d4a817]'
                  : 'bg-white text-gray-600 border border-gray-200 hover:bg-gray-50'
              }`}
            >
              {tab}
            </button>
          ))}
        </div>

        <div className="flex flex-col lg:flex-row gap-10">

          {/* Main Content */}
          <div className="w-full lg:w-2/3 flex flex-col gap-10">

            {/* Featured Sale Hero */}
            {featuredSale && (
              <div className="relative rounded-sm overflow-hidden shadow-sm group bg-black">
                <img
                  src={featuredSale.hero_image_url || 'https://images.unsplash.com/photo-1502005229762-cf1b2da7c5d6?w=1200'}
                  alt={featuredSale.title}
                  className="w-full h-[450px] object-cover opacity-70 group-hover:opacity-80 group-hover:scale-105 transition-all duration-700"
                />
                <div className="absolute inset-0 z-20 flex flex-col justify-end p-6 md:p-10 text-white bg-gradient-to-t from-black/90 via-black/40 to-transparent">
                  <span className="fpr-coral-bg text-white text-xs font-bold px-3 py-1 uppercase tracking-wider rounded-sm w-fit mb-4 shadow-md">
                    FEATURED SALE
                  </span>
                  <h2 className="font-serif text-3xl md:text-4xl font-bold leading-tight mb-3">
                    {featuredSale.title}
                  </h2>
                  <p className="text-gray-200 mb-6 max-w-2xl text-sm md:text-base">
                    {featuredSale.price_display} — {featuredSale.city}, FL
                  </p>
                  <div className="flex flex-wrap gap-4 text-xs font-semibold mb-6">
                    <div className="flex items-center gap-1"><MapPin size={14} className="text-[#d4a817]" /> {featuredSale.city}</div>
                    <div className="flex items-center gap-1"><Calendar size={14} className="text-[#d4a817]" /> {formatDate(featuredSale.close_date)}</div>
                  </div>
                  <Link
                    href={featuredSale.article ? `/articles/${featuredSale.slug}` : '/notable-sales'}
                    className="flex items-center gap-2 font-bold text-sm bg-white text-black px-6 py-3 w-fit rounded-sm hover:fpr-gold-bg hover:text-white transition-colors shadow-sm"
                  >
                    READ FULL STORY &rarr;
                  </Link>
                </div>
              </div>
            )}

            {/* Sales Grid */}
            <div>
              <div className="flex items-center justify-between mb-6">
                <h3 className="font-serif font-bold text-2xl text-[#0d1b2a]">Recent Notable Sales</h3>
              </div>

              <motion.div
                key={activeTab}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.3 }}
                className="grid grid-cols-1 sm:grid-cols-2 gap-6"
              >
                {sales.map((sale) => (
                  <Link
                    href={sale.article ? `/articles/${sale.slug}` : '#'}
                    key={sale.slug}
                    className="group relative rounded-sm overflow-hidden bg-white shadow-sm border border-gray-200 flex flex-col h-full cursor-pointer"
                  >
                    <div className="relative h-48 w-full overflow-hidden">
                      <div className="absolute top-3 right-3 z-10 fpr-navy text-white text-sm font-bold px-3 py-1 rounded-sm shadow-md">
                        {sale.price_display}
                      </div>
                      <img
                        src={sale.hero_image_url || 'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=600'}
                        alt={sale.title}
                        className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
                      />
                    </div>
                    <div className="p-5 flex flex-col flex-1">
                      <span className="text-[10px] font-bold tracking-wider fpr-coral uppercase mb-2">
                        {TYPE_LABELS[sale.property_type] ?? sale.property_type.replace(/_/g, ' ')}
                      </span>
                      <h4 className="font-serif text-lg font-bold leading-tight mb-3 group-hover:text-blue-900 transition-colors">
                        {sale.title}
                      </h4>
                      <div className="mt-auto flex items-center justify-between text-xs text-gray-500 pt-3 border-t border-gray-100">
                        <span className="flex items-center gap-1"><MapPin size={12} /> {sale.city}, FL</span>
                        <span>{formatDate(sale.close_date)}</span>
                      </div>
                    </div>
                  </Link>
                ))}
              </motion.div>

              {sales.length === 0 && (
                <p className="text-gray-400 text-sm py-8 text-center">No sales found for this region.</p>
              )}
            </div>
          </div>

          {/* Sidebar */}
          <div className="w-full lg:w-1/3 flex flex-col gap-8">

            {/* Top Luxury Closings */}
            <div className="bg-white border border-gray-200 rounded-sm p-5 shadow-sm">
              <div className="flex items-center justify-between mb-5 pb-2 border-b-2 border-[#0d1b2a]">
                <h3 className="font-serif font-bold text-lg">Top Luxury Closings</h3>
              </div>
              <div className="flex flex-col gap-4">
                {topClosings.map((sale, i) => (
                  <div key={sale.slug} className="flex items-center gap-3">
                    <span className="font-serif font-bold text-2xl text-gray-200 shrink-0 w-6">{i + 1}</span>
                    <div className="flex flex-col flex-1">
                      <span className="font-bold text-sm text-gray-900">{sale.title}</span>
                      <span className="text-xs text-gray-500">{sale.city}</span>
                    </div>
                    <span className="fpr-navy text-white text-xs font-bold px-2 py-1 rounded-sm shrink-0">
                      {sale.price_display}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* Fastest Growing Markets */}
            <div className="bg-white border border-gray-200 rounded-sm p-5 shadow-sm">
              <div className="flex items-center justify-between mb-5 pb-2 border-b-2 border-[#0d1b2a]">
                <h3 className="font-serif font-bold text-lg">Fastest Growing Markets</h3>
                <span className="text-xs text-gray-500 uppercase tracking-wider font-semibold">% Change</span>
              </div>
              <div className="flex flex-col gap-4">
                {fastestGrowing.map((item) => (
                  <div key={item.rank} className="flex items-center justify-between border-b border-gray-100 last:border-0 pb-3 last:pb-0">
                    <div className="flex items-center gap-3">
                      <span className="font-serif font-bold text-lg text-[#d4a817] w-4">{item.rank}</span>
                      <span className="font-bold text-sm text-gray-800">{item.location}</span>
                    </div>
                    <span className="font-bold fpr-green">{item.change_display}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Subscribe CTA */}
            <div className="bg-[#0f4c5c] text-white rounded-sm p-6 shadow-sm flex flex-col items-center text-center">
              <div className="w-12 h-12 rounded-full fpr-gold-bg text-black flex items-center justify-center mb-4">
                <Bell size={24} />
              </div>
              <h3 className="font-serif font-bold text-2xl mb-2">Subscribe for Deal Alerts</h3>
              <p className="text-sm text-gray-200 mb-6 leading-relaxed">
                Get the latest notable sales, off-market opportunities, and market intelligence—delivered weekly.
              </p>
              {subscribed ? (
                <p className="text-[#d4a817] font-bold">You're subscribed!</p>
              ) : (
                <div className="w-full flex flex-col gap-3">
                  <input
                    type="email"
                    placeholder="Email address"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && handleSubscribe()}
                    className="w-full px-4 py-3 text-gray-900 rounded-sm focus:outline-none focus:ring-2 focus:ring-[#d4a817] text-sm"
                  />
                  <button
                    onClick={handleSubscribe}
                    disabled={subscribe.isPending}
                    className="w-full fpr-navy text-white font-bold py-3 rounded-sm hover:bg-gray-800 transition-colors shadow-md text-sm disabled:opacity-60"
                  >
                    {subscribe.isPending ? 'SUBSCRIBING…' : 'SUBSCRIBE'}
                  </button>
                </div>
              )}
              <p className="text-[10px] text-gray-300 mt-4">No spam. Unsubscribe anytime.</p>
            </div>

          </div>
        </div>
      </main>
    </div>
  );
}
