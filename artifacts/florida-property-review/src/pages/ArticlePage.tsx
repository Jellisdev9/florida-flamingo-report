import React from 'react';
import { Header } from '@/components/Header';
import { TopMarketsSidebar, NewsletterCompact } from '@/components/Sidebar';
import { Link } from 'wouter';
import { FaFacebook, FaLinkedin, FaTwitter } from 'react-icons/fa';
import { Mail, MapPin, Building2, Calendar, BedDouble } from 'lucide-react';

export function ArticlePage() {
  return (
    <div className="min-h-screen bg-[#f4f5f7] flex flex-col font-sans">
      <Header />
      
      <main className="flex-1 w-full max-w-7xl mx-auto px-4 md:px-8 py-8 flex flex-col lg:flex-row gap-10">
        
        {/* Main Article Column */}
        <div className="w-full lg:w-2/3 bg-white p-6 md:p-10 shadow-sm border border-gray-200 rounded-sm">
          <div className="mb-6">
            <span className="fpr-coral-bg text-white text-[10px] font-bold px-3 py-1 uppercase tracking-wider rounded-sm w-fit">
              Notable Sale
            </span>
          </div>
          
          <h1 className="font-serif text-4xl md:text-5xl font-bold leading-tight mb-4 italic text-[#0d1b2a]">
            $32.5M Naples Bayfront Estate Sets a New Benchmark
          </h1>
          
          <p className="text-xl text-gray-600 mb-8 font-medium">
            A rare bayside compound in Port Royal redefines luxury waterfront living.
          </p>
          
          <div className="flex flex-wrap items-center justify-between gap-4 py-4 border-t border-b border-gray-100 mb-8">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-gray-200 overflow-hidden shrink-0">
                <img src={`https://ui-avatars.com/api/?name=Caroline+Bennett&background=0d1b2a&color=fff`} alt="Author" />
              </div>
              <div className="flex flex-col">
                <span className="text-sm font-bold text-gray-900">By Caroline Bennett, Senior Real Estate Editor</span>
                <span className="text-xs text-gray-500">May 12, 2024 &middot; 5 min read</span>
              </div>
            </div>
            
            <div className="flex items-center gap-3 text-gray-400">
              <button className="hover:text-blue-600 transition-colors p-2 rounded-full hover:bg-gray-50"><FaFacebook size={18} /></button>
              <button className="hover:text-blue-500 transition-colors p-2 rounded-full hover:bg-gray-50"><FaTwitter size={18} /></button>
              <button className="hover:text-blue-700 transition-colors p-2 rounded-full hover:bg-gray-50"><FaLinkedin size={18} /></button>
              <button className="hover:text-gray-900 transition-colors p-2 rounded-full hover:bg-gray-50"><Mail size={18} /></button>
            </div>
          </div>
          
          <div className="w-full mb-10 rounded-sm overflow-hidden">
            <img 
              src="https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=1200" 
              alt="Naples Bayfront Estate" 
              className="w-full h-auto object-cover max-h-[500px]"
            />
            <p className="text-xs text-gray-400 text-right mt-2 italic">Photo: Premier Sotheby's International Realty</p>
          </div>
          
          <div className="prose prose-lg max-w-none text-gray-800">
            <p className="first-letter:text-7xl first-letter:font-serif first-letter:font-bold first-letter:text-[#0d1b2a] first-letter:mr-3 first-letter:float-left first-line:uppercase first-line:tracking-widest">
              A spectacular bayfront compound in Naples’ exclusive Port Royal neighborhood has closed for $32.5 million, marking one of the highest residential sales in Southwest Florida this year. The off-market transaction underscores the enduring strength of the ultra-luxury segment, even as broader market inventory begins to normalize.
            </p>
            <p className="mt-6">
              Located at 3255 Fort Charles Drive, the 11,276-square-foot estate sits on 1.5 acres with sweeping views of Naples Bay. Custom-built in 2019, the property features a rare deep-water yacht basin capable of accommodating vessels over 100 feet—a highly coveted amenity that drove competitive interest from multiple out-of-state buyers.
            </p>

            <div className="my-10 pl-6 border-l-4 border-[#d4a817]">
              <p className="text-2xl font-serif italic text-gray-900 leading-relaxed">
                "This sale underscores the enduring demand for trophy waterfront properties in Naples, particularly in Port Royal. Buyers at this level are immune to interest rate fluctuations; they are looking for irreplaceable assets."
              </p>
              <footer className="mt-4 text-sm font-bold text-gray-500 uppercase tracking-wider">
                — Michael Lawler, Premier Sotheby's International Realty
              </footer>
            </div>

            {/* Float Card */}
            <div className="bg-[#f4f5f7] border border-gray-200 p-6 rounded-sm my-8 md:float-right md:w-80 md:ml-8 md:mb-6 shadow-sm">
              <h4 className="font-serif font-bold text-xl mb-4 text-[#0d1b2a] border-b pb-2">Sale Facts</h4>
              <ul className="flex flex-col gap-4 text-sm">
                <li className="flex items-start gap-3">
                  <span className="fpr-gold mt-0.5"><Building2 size={16} /></span>
                  <div>
                    <span className="text-gray-500 block text-xs uppercase tracking-wider">Sale Price</span>
                    <span className="font-bold text-gray-900 text-lg">$32,500,000</span>
                  </div>
                </li>
                <li className="flex items-start gap-3">
                  <span className="fpr-gold mt-0.5"><MapPin size={16} /></span>
                  <div>
                    <span className="text-gray-500 block text-xs uppercase tracking-wider">Location</span>
                    <span className="font-bold text-gray-900">3255 Fort Charles Drive<br/>Naples, FL 34102</span>
                  </div>
                </li>
                <li className="flex items-start gap-3">
                  <span className="fpr-gold mt-0.5"><Building2 size={16} /></span>
                  <div>
                    <span className="text-gray-500 block text-xs uppercase tracking-wider">Brokerage</span>
                    <span className="font-bold text-gray-900">Premier Sotheby's Int. Realty</span>
                  </div>
                </li>
                <li className="flex items-start gap-3">
                  <span className="fpr-gold mt-0.5"><BedDouble size={16} /></span>
                  <div>
                    <span className="text-gray-500 block text-xs uppercase tracking-wider">Property Size</span>
                    <span className="font-bold text-gray-900">8 Beds | 10.5 Baths<br/>11,276 SQ FT</span>
                  </div>
                </li>
              </ul>
            </div>

            <p className="mt-6">
              The buyer, identified only through an LLC registered in Delaware, plans to utilize the estate as a seasonal residence. The transaction was handled entirely off-market, reflecting a growing trend among high-net-worth individuals seeking privacy in their real estate dealings.
            </p>
            <p className="mt-6">
              Market data from the Naples Area Board of Realtors indicates that while overall luxury inventory (homes priced above $5 million) has increased 14% year-over-year, properties with direct Gulf access and deep-water dockage remain acutely scarce. This supply-demand imbalance continues to push prices for prime waterfront acreage to record highs, solidifying Naples' position alongside Palm Beach and Miami Beach as one of the nation's premier luxury real estate hubs.
            </p>
          </div>
        </div>

        {/* Sidebar */}
        <div className="w-full lg:w-1/3 flex flex-col gap-8">
          <div className="bg-white border border-gray-200 rounded-sm p-5 shadow-sm">
            <h3 className="font-serif font-bold text-lg mb-4 pb-2 border-b-2 border-[#0d1b2a]">Related Stories</h3>
            <div className="flex flex-col gap-5">
              <Link href="#" className="flex gap-4 group cursor-pointer">
                <img src="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=400" className="w-20 h-20 object-cover rounded-sm shrink-0" alt="Boca" />
                <div className="flex flex-col">
                  <span className="text-[10px] font-bold text-gray-500 uppercase tracking-wider mb-1">Notable Sale</span>
                  <span className="font-bold text-sm leading-snug group-hover:fpr-gold transition-colors line-clamp-2 mb-1">Modern Masterpiece in Boca Raton Sells for $24M</span>
                  <span className="text-xs text-gray-400">May 8, 2024</span>
                </div>
              </Link>
              <div className="w-full h-px bg-gray-100"></div>
              <Link href="#" className="flex gap-4 group cursor-pointer">
                <img src="https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=400" className="w-20 h-20 object-cover rounded-sm shrink-0" alt="Trend" />
                <div className="flex flex-col">
                  <span className="text-[10px] font-bold text-gray-500 uppercase tracking-wider mb-1">Market Trend</span>
                  <span className="font-bold text-sm leading-snug group-hover:fpr-gold transition-colors line-clamp-2 mb-1">Luxury Inventory Tightens Across Southwest Florida</span>
                  <span className="text-xs text-gray-400">May 7, 2024</span>
                </div>
              </Link>
              <div className="w-full h-px bg-gray-100"></div>
              <Link href="#" className="flex gap-4 group cursor-pointer">
                <div className="w-20 h-20 bg-gray-100 rounded-sm shrink-0 flex items-center justify-center fpr-navy text-white font-serif italic text-2xl">PS</div>
                <div className="flex flex-col">
                  <span className="text-[10px] font-bold text-gray-500 uppercase tracking-wider mb-1">Agent News</span>
                  <span className="font-bold text-sm leading-snug group-hover:fpr-gold transition-colors line-clamp-2 mb-1">Premier Sotheby's Opens New Office in Naples</span>
                  <span className="text-xs text-gray-400">May 6, 2024</span>
                </div>
              </Link>
            </div>
          </div>
          
          <TopMarketsSidebar />
          <NewsletterCompact />
        </div>

      </main>
    </div>
  );
}
