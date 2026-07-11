import React, { useState } from 'react';
import { Header } from '@/components/Header';
import { TopMarketsSidebar, TopAgentsSidebar } from '@/components/Sidebar';
import { ArticleCard } from '@/components/ArticleCard';
import { Link } from 'wouter';
import { motion } from 'framer-motion';
import {
  useFeaturedArticle,
  useArticles,
  useTopClosings,
  useNeighborhoodIntel,
  useSubscribe,
} from '@/hooks/useApi';
import { formatDate, formatCategory } from '@/lib/api';

const TAG_STYLES: Record<string, string> = {
  HOT: 'fpr-coral-bg text-white',
  RISING: 'fpr-gold-bg text-black',
  COOLING: 'bg-blue-100 text-blue-800',
  STABLE: 'bg-gray-100 text-gray-700',
};

export function HomePage() {
  const { data: featured } = useFeaturedArticle();
  const { data: articlesPage } = useArticles();
  const { data: topClosings = [] } = useTopClosings();
  const { data: neighborhoods = [] } = useNeighborhoodIntel();
  const articles = articlesPage?.results ?? [];

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

      <main className="flex-1 w-full max-w-7xl mx-auto px-4 md:px-8 py-8 md:py-10 flex flex-col gap-10">

        {/* Top Hero Section */}
        <div className="flex flex-col lg:flex-row gap-8">
          {/* Left Hero Card */}
          <div className="lg:w-2/3 relative rounded-sm overflow-hidden shadow-sm group">
            <div className="absolute inset-0 bg-black/40 z-10"></div>
            <img
              src={featured?.hero_image_url || 'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=1200'}
              alt={featured?.headline || 'Featured Story'}
              className="w-full h-[400px] md:h-[500px] object-cover transition-transform duration-700 group-hover:scale-105"
            />
            <div className="absolute inset-0 z-20 flex flex-col justify-end p-6 md:p-10 text-white bg-gradient-to-t from-black/80 via-black/40 to-transparent">
              <span className="fpr-coral-bg text-white text-xs font-bold px-3 py-1 uppercase tracking-wider rounded-sm w-fit mb-4">
                Featured Story
              </span>
              <h2 className="font-serif text-3xl md:text-5xl font-bold leading-tight mb-3">
                {featured?.headline || 'Florida's real estate market, tracked like a business desk.'}
              </h2>
              <p className="text-lg md:text-xl text-gray-200 mb-6 max-w-2xl">
                {featured?.subheadline || 'Deal flow, agent moves, and market shifts—delivered with clarity and speed.'}
              </p>
              <Link
                href={featured ? `/articles/${featured.slug}` : '/articles/naples-bayfront-estate'}
                className="flex items-center gap-2 font-bold text-sm bg-white text-black px-6 py-3 w-fit rounded-sm hover:fpr-gold-bg hover:text-white transition-colors"
              >
                READ THE STORY &rarr;
              </Link>
            </div>
          </div>

          {/* Right Sidebar */}
          <div className="lg:w-1/3">
            <TopMarketsSidebar />
          </div>
        </div>

        {/* Article Cards Row */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-6"
        >
          {articles.slice(0, 5).map((article) => (
            <ArticleCard
              key={article.slug}
              category={formatCategory(article.category)}
              headline={article.headline}
              date={formatDate(article.published_date)}
              readTime={`${article.read_time_minutes} min`}
              image={article.hero_image_url}
              href={`/articles/${article.slug}`}
            />
          ))}
        </motion.div>

        {/* Lower Section (3 cols) */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">

          {/* Luxury Closings */}
          <div className="bg-white border border-gray-200 rounded-sm p-5 shadow-sm h-full">
            <div className="flex items-center justify-between mb-4 pb-2 border-b-2 border-[#0d1b2a]">
              <h3 className="font-serif font-bold text-lg">Luxury Closings</h3>
            </div>
            <div className="flex flex-col gap-4">
              {topClosings.slice(0, 2).map((sale, i) => (
                <React.Fragment key={sale.slug}>
                  {i > 0 && <div className="h-px w-full bg-gray-100"></div>}
                  <Link href={sale.article ? `/articles/${sale.slug}` : '/notable-sales'} className="flex items-start gap-4 group">
                    <img
                      src={sale.hero_image_url || 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=400'}
                      alt={sale.city}
                      className="w-20 h-20 object-cover rounded-sm shrink-0"
                    />
                    <div className="flex flex-col">
                      <span className="font-bold text-lg text-gray-900 group-hover:fpr-gold transition-colors">{sale.price_display}</span>
                      <span className="text-sm text-gray-600 line-clamp-2">{sale.title}</span>
                    </div>
                  </Link>
                </React.Fragment>
              ))}
            </div>
          </div>

          <TopAgentsSidebar />

          {/* Neighborhood Intelligence */}
          <div className="bg-white border border-gray-200 rounded-sm p-5 shadow-sm h-full">
            <div className="flex items-center justify-between mb-4 pb-2 border-b-2 border-[#0d1b2a]">
              <h3 className="font-serif font-bold text-lg">Neighborhood Intelligence</h3>
            </div>
            <div className="flex flex-col gap-5">
              {neighborhoods.map((n, i) => (
                <div key={i} className={`flex flex-col gap-2 ${i < neighborhoods.length - 1 ? 'border-b border-gray-100 pb-4' : ''}`}>
                  <div className="flex items-center gap-2">
                    <span className="font-bold text-gray-900">{n.neighborhood}</span>
                    <span className={`text-[10px] font-bold px-2 py-0.5 rounded-sm ${TAG_STYLES[n.tag] ?? 'bg-gray-100 text-gray-700'}`}>
                      {n.tag}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600">{n.description}</p>
                </div>
              ))}
            </div>
          </div>

        </div>

        {/* Newsletter Banner */}
        <div className="w-full fpr-navy rounded-sm p-8 md:p-12 shadow-sm text-center flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="text-left max-w-xl">
            <h3 className="font-serif font-bold text-3xl text-white mb-2">Stay ahead of the market.</h3>
            <p className="text-gray-300">Join 15,000+ real estate professionals receiving our daily market intelligence.</p>
          </div>
          {subscribed ? (
            <p className="text-[#d4a817] font-bold text-lg">You're subscribed!</p>
          ) : (
            <div className="flex w-full md:w-auto max-w-md gap-2">
              <input
                type="email"
                placeholder="Your email address"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSubscribe()}
                className="flex-1 px-4 py-3 text-gray-900 rounded-sm focus:outline-none focus:ring-2 focus:ring-[#d4a817]"
              />
              <button
                onClick={handleSubscribe}
                disabled={subscribe.isPending}
                className="fpr-gold-bg text-black font-bold px-6 py-3 rounded-sm hover:bg-yellow-500 transition-colors shrink-0 disabled:opacity-60"
              >
                {subscribe.isPending ? 'SUBSCRIBING…' : 'SUBSCRIBE'}
              </button>
            </div>
          )}
        </div>

      </main>

      <footer className="w-full border-t border-gray-200 bg-white py-12 px-4 md:px-8 mt-auto">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-6">
          <div className="flex items-center gap-3 opacity-50 grayscale">
            <div className="fpr-navy text-white font-bold text-xl px-2 py-1 flex items-center justify-center h-10 w-10">
              FPR
            </div>
            <span className="font-serif font-bold text-lg">Florida Property Review</span>
          </div>
          <div className="text-sm text-gray-500">
            &copy; 2024 Florida Property Review. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  );
}
