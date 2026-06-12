import React, { useState } from 'react';
import { Header } from '@/components/Header';
import { Link } from 'wouter';
import { MapPin, Calendar, Bell } from 'lucide-react';
import { motion } from 'framer-motion';

export function NotableSalesPage() {
  const [activeTab, setActiveTab] = useState('All Regions');
  const tabs = ['All Regions', 'South Florida', 'Tampa Bay', 'Orlando', 'Jacksonville', 'Panhandle'];

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
          {tabs.map(tab => (
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
          
          {/* Main Content Area */}
          <div className="w-full lg:w-2/3 flex flex-col gap-10">
            
            {/* Featured Sale Hero */}
            <div className="relative rounded-sm overflow-hidden shadow-sm group bg-black">
              <img 
                src="https://images.unsplash.com/photo-1502005229762-cf1b2da7c5d6?w=1200" 
                alt="Miami Beach Estate" 
                className="w-full h-[450px] object-cover opacity-70 group-hover:opacity-80 group-hover:scale-105 transition-all duration-700"
              />
              <div className="absolute inset-0 z-20 flex flex-col justify-end p-6 md:p-10 text-white bg-gradient-to-t from-black/90 via-black/40 to-transparent">
                <span className="fpr-coral-bg text-white text-xs font-bold px-3 py-1 uppercase tracking-wider rounded-sm w-fit mb-4 shadow-md">
                  FEATURED SALE
                </span>
                <h2 className="font-serif text-3xl md:text-4xl font-bold leading-tight mb-3">
                  Billionaire tech founder pays $48M for Miami Beach waterfront estate
                </h2>
                <p className="text-gray-200 mb-6 max-w-2xl text-sm md:text-base">
                  The 12,000-SF modern compound on La Gorce Island sold off-market in one of May's top residential closings in South Florida.
                </p>
                <div className="flex flex-wrap gap-4 text-xs font-semibold mb-6">
                  <div className="flex items-center gap-1"><MapPin size={14} className="text-[#d4a817]" /> La Gorce Island, Miami Beach</div>
                  <div className="flex items-center gap-1"><Calendar size={14} className="text-[#d4a817]" /> May 9, 2024</div>
                </div>
                <Link href="/articles/naples-bayfront-estate" className="flex items-center gap-2 font-bold text-sm bg-white text-black px-6 py-3 w-fit rounded-sm hover:fpr-gold-bg hover:text-white transition-colors shadow-sm">
                  READ FULL STORY &rarr;
                </Link>
              </div>
            </div>
            
            {/* Grid of Sales */}
            <div>
              <div className="flex items-center justify-between mb-6">
                <h3 className="font-serif font-bold text-2xl text-[#0d1b2a]">Recent Notable Sales</h3>
                <Link href="#" className="text-sm font-bold fpr-navy text-white px-4 py-2 rounded-sm hover:bg-[#0f4c5c] transition-colors">
                  VIEW ALL SALES &rarr;
                </Link>
              </div>
              
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                {[
                  { price: "$32,500,000", cat: "WATERFRONT ESTATE", title: "Boca Raton Oceanfront Estate Sells for $32.5M", loc: "Boca Raton, FL", date: "May 12, 2024", img: "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=600" },
                  { price: "$18,750,000", cat: "CONDO PENTHOUSE", title: "Surf Club Four Seasons Penthouse Closes at $18.75M", loc: "Surfside, FL", date: "May 11, 2024", img: "https://images.unsplash.com/photo-1551361415-69c87624334f?w=600" },
                  { price: "$26,000,000", cat: "COMMERCIAL", title: "Coral Gables Office Building Trades for $26M", loc: "Coral Gables, FL", date: "May 10, 2024", img: "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=600" },
                  { price: "$24,000,000", cat: "WATERFRONT ESTATE", title: "Naples Bayfront Home Sells for $24M", loc: "Naples, FL", date: "May 8, 2024", img: "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=600" },
                  { price: "$9,800,000", cat: "CONDO RESIDENCE", title: "Park Grove Tower Unit Closes for $9.8M", loc: "Coconut Grove, FL", date: "May 5, 2024", img: "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=600" },
                ].map((sale, i) => (
                  <Link href="/articles/naples-bayfront-estate" key={i} className="group relative rounded-sm overflow-hidden bg-white shadow-sm border border-gray-200 flex flex-col h-full cursor-pointer">
                    <div className="relative h-48 w-full overflow-hidden">
                      <div className="absolute top-3 right-3 z-10 fpr-navy text-white text-sm font-bold px-3 py-1 rounded-sm shadow-md">
                        {sale.price}
                      </div>
                      <img src={sale.img} alt={sale.title} className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105" />
                    </div>
                    <div className="p-5 flex flex-col flex-1">
                      <span className="text-[10px] font-bold tracking-wider fpr-coral uppercase mb-2">
                        {sale.cat}
                      </span>
                      <h4 className="font-serif text-lg font-bold leading-tight mb-3 group-hover:text-blue-900 transition-colors">
                        {sale.title}
                      </h4>
                      <div className="mt-auto flex items-center justify-between text-xs text-gray-500 pt-3 border-t border-gray-100">
                        <span className="flex items-center gap-1"><MapPin size={12}/> {sale.loc}</span>
                        <span>{sale.date}</span>
                      </div>
                    </div>
                  </Link>
                ))}
              </div>
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
                {[
                  { title: "La Gorce Island Estate", loc: "Miami Beach", price: "$48,000,000" },
                  { title: "Boca Raton Oceanfront Estate", loc: "Boca Raton", price: "$32,500,000" },
                  { title: "Bay Point Compound", loc: "Miami", price: "$28,750,000" },
                  { title: "Naples Bayfront Home", loc: "Naples", price: "$24,000,000" },
                  { title: "Surf Club Penthouse", loc: "Surfside", price: "$18,750,000" }
                ].map((item, i) => (
                  <div key={i} className="flex items-center gap-3">
                    <span className="font-serif font-bold text-2xl text-gray-200 shrink-0 w-6">{i+1}</span>
                    <div className="flex flex-col flex-1">
                      <span className="font-bold text-sm text-gray-900">{item.title}</span>
                      <span className="text-xs text-gray-500">{item.loc}</span>
                    </div>
                    <span className="fpr-navy text-white text-xs font-bold px-2 py-1 rounded-sm shrink-0">
                      {item.price}
                    </span>
                  </div>
                ))}
              </div>
              <button className="mt-6 w-full text-center text-xs font-bold text-gray-500 uppercase tracking-wider hover:text-gray-900 transition-colors">
                View All &rarr;
              </button>
            </div>
            
            {/* Fastest Growing Markets */}
            <div className="bg-white border border-gray-200 rounded-sm p-5 shadow-sm">
              <div className="flex items-center justify-between mb-5 pb-2 border-b-2 border-[#0d1b2a]">
                <h3 className="font-serif font-bold text-lg">Fastest Growing Markets</h3>
                <span className="text-xs text-gray-500 uppercase tracking-wider font-semibold">% Change</span>
              </div>
              <div className="flex flex-col gap-4">
                {[
                  { loc: "Winter Park", val: "+18.7%" },
                  { loc: "West Palm Beach", val: "+14.2%" },
                  { loc: "Sarasota", val: "+13.5%" },
                  { loc: "Lakeland", val: "+12.2%" },
                  { loc: "Jacksonville Beach", val: "+11.8%" }
                ].map((item, i) => (
                  <div key={i} className="flex items-center justify-between border-b border-gray-100 last:border-0 pb-3 last:pb-0">
                    <div className="flex items-center gap-3">
                      <span className="font-serif font-bold text-lg text-[#d4a817] w-4">{i+1}</span>
                      <span className="font-bold text-sm text-gray-800">{item.loc}</span>
                    </div>
                    <span className="font-bold fpr-green">{item.val}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Subscribe CTA Card */}
            <div className="bg-[#0f4c5c] text-white rounded-sm p-6 shadow-sm flex flex-col items-center text-center">
              <div className="w-12 h-12 rounded-full fpr-gold-bg text-black flex items-center justify-center mb-4">
                <Bell size={24} />
              </div>
              <h3 className="font-serif font-bold text-2xl mb-2">Subscribe for Deal Alerts</h3>
              <p className="text-sm text-gray-200 mb-6 leading-relaxed">
                Get the latest notable sales, off-market opportunities, and market intelligence—delivered weekly.
              </p>
              <div className="w-full flex flex-col gap-3">
                <input 
                  type="email" 
                  placeholder="Email address" 
                  className="w-full px-4 py-3 text-gray-900 rounded-sm focus:outline-none focus:ring-2 focus:ring-[#d4a817] text-sm"
                />
                <button className="w-full fpr-navy text-white font-bold py-3 rounded-sm hover:bg-gray-800 transition-colors shadow-md text-sm">
                  SUBSCRIBE
                </button>
              </div>
              <p className="text-[10px] text-gray-300 mt-4">No spam. Unsubscribe anytime.</p>
            </div>
            
          </div>
          
        </div>
      </main>
    </div>
  );
}
