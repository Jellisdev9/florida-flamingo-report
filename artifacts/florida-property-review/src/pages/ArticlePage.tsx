import React from 'react';
import { Header } from '@/components/Header';
import { TopMarketsSidebar, NewsletterCompact } from '@/components/Sidebar';
import { Link, useParams } from 'wouter';
import { FaFacebook, FaLinkedin, FaTwitter } from 'react-icons/fa';
import { Mail, MapPin, Building2, BedDouble } from 'lucide-react';
import { useArticle, useArticles } from '@/hooks/useApi';
import { formatDate, formatCategory } from '@/lib/api';

export function ArticlePage() {
  const { slug } = useParams<{ slug: string }>();
  const { data: article, isLoading } = useArticle(slug ?? '');
  const { data: relatedPage } = useArticles(article?.category);
  const related = (relatedPage?.results ?? [])
    .filter((a) => a.slug !== slug)
    .slice(0, 3);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-[#f4f5f7] flex flex-col font-sans">
        <Header />
        <main className="flex-1 flex items-center justify-center">
          <p className="text-gray-400 text-sm">Loading…</p>
        </main>
      </div>
    );
  }

  if (!article) {
    return (
      <div className="min-h-screen bg-[#f4f5f7] flex flex-col font-sans">
        <Header />
        <main className="flex-1 flex items-center justify-center">
          <p className="text-gray-500">Article not found.</p>
        </main>
      </div>
    );
  }

  const sale = article.sale_facts;

  return (
    <div className="min-h-screen bg-[#f4f5f7] flex flex-col font-sans">
      <Header />

      <main className="flex-1 w-full max-w-7xl mx-auto px-4 md:px-8 py-8 flex flex-col lg:flex-row gap-10">

        {/* Main Article Column */}
        <div className="w-full lg:w-2/3 bg-white p-6 md:p-10 shadow-sm border border-gray-200 rounded-sm">
          <div className="mb-6">
            <span className="fpr-coral-bg text-white text-[10px] font-bold px-3 py-1 uppercase tracking-wider rounded-sm w-fit">
              {formatCategory(article.category)}
            </span>
          </div>

          <h1 className="font-serif text-4xl md:text-5xl font-bold leading-tight mb-4 italic text-[#0d1b2a]">
            {article.headline}
          </h1>

          {article.subheadline && (
            <p className="text-xl text-gray-600 mb-8 font-medium">{article.subheadline}</p>
          )}

          <div className="flex flex-wrap items-center justify-between gap-4 py-4 border-t border-b border-gray-100 mb-8">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-gray-200 overflow-hidden shrink-0">
                {article.author_avatar_url && (
                  <img src={article.author_avatar_url} alt="Author" />
                )}
              </div>
              <div className="flex flex-col">
                <span className="text-sm font-bold text-gray-900">{article.byline}</span>
                <span className="text-xs text-gray-500">
                  {formatDate(article.published_date)} &middot; {article.read_time_minutes} min read
                </span>
              </div>
            </div>
            <div className="flex items-center gap-3 text-gray-400">
              <button className="hover:text-blue-600 transition-colors p-2 rounded-full hover:bg-gray-50"><FaFacebook size={18} /></button>
              <button className="hover:text-blue-500 transition-colors p-2 rounded-full hover:bg-gray-50"><FaTwitter size={18} /></button>
              <button className="hover:text-blue-700 transition-colors p-2 rounded-full hover:bg-gray-50"><FaLinkedin size={18} /></button>
              <button className="hover:text-gray-900 transition-colors p-2 rounded-full hover:bg-gray-50"><Mail size={18} /></button>
            </div>
          </div>

          {article.hero_image_url && (
            <div className="w-full mb-10 rounded-sm overflow-hidden">
              <img
                src={article.hero_image_url}
                alt={article.headline}
                className="w-full h-auto object-cover max-h-[500px]"
              />
            </div>
          )}

          <div className="prose prose-lg max-w-none text-gray-800">
            {article.body.split('\n\n').map((paragraph, i) => (
              <p
                key={i}
                className={i === 0
                  ? 'first-letter:text-7xl first-letter:font-serif first-letter:font-bold first-letter:text-[#0d1b2a] first-letter:mr-3 first-letter:float-left first-line:uppercase first-line:tracking-widest'
                  : 'mt-6'}
              >
                {paragraph}
              </p>
            ))}

            {/* Sale Facts Card */}
            {sale && (
              <div className="bg-[#f4f5f7] border border-gray-200 p-6 rounded-sm my-8 md:float-right md:w-80 md:ml-8 md:mb-6 shadow-sm">
                <h4 className="font-serif font-bold text-xl mb-4 text-[#0d1b2a] border-b pb-2">Sale Facts</h4>
                <ul className="flex flex-col gap-4 text-sm">
                  <li className="flex items-start gap-3">
                    <span className="fpr-gold mt-0.5"><Building2 size={16} /></span>
                    <div>
                      <span className="text-gray-500 block text-xs uppercase tracking-wider">Sale Price</span>
                      <span className="font-bold text-gray-900 text-lg">{sale.price_display}</span>
                    </div>
                  </li>
                  <li className="flex items-start gap-3">
                    <span className="fpr-gold mt-0.5"><MapPin size={16} /></span>
                    <div>
                      <span className="text-gray-500 block text-xs uppercase tracking-wider">Location</span>
                      <span className="font-bold text-gray-900">{sale.location}</span>
                    </div>
                  </li>
                  {sale.brokerage && (
                    <li className="flex items-start gap-3">
                      <span className="fpr-gold mt-0.5"><Building2 size={16} /></span>
                      <div>
                        <span className="text-gray-500 block text-xs uppercase tracking-wider">Brokerage</span>
                        <span className="font-bold text-gray-900">{sale.brokerage}</span>
                      </div>
                    </li>
                  )}
                  {(sale.beds || sale.baths || sale.sq_ft) && (
                    <li className="flex items-start gap-3">
                      <span className="fpr-gold mt-0.5"><BedDouble size={16} /></span>
                      <div>
                        <span className="text-gray-500 block text-xs uppercase tracking-wider">Property Size</span>
                        <span className="font-bold text-gray-900">
                          {[
                            sale.beds && `${sale.beds} Beds`,
                            sale.baths && `${sale.baths} Baths`,
                            sale.sq_ft && `${sale.sq_ft.toLocaleString()} SQ FT`,
                          ].filter(Boolean).join(' | ')}
                        </span>
                      </div>
                    </li>
                  )}
                </ul>
              </div>
            )}
          </div>
        </div>

        {/* Sidebar */}
        <div className="w-full lg:w-1/3 flex flex-col gap-8">
          {related.length > 0 && (
            <div className="bg-white border border-gray-200 rounded-sm p-5 shadow-sm">
              <h3 className="font-serif font-bold text-lg mb-4 pb-2 border-b-2 border-[#0d1b2a]">Related Stories</h3>
              <div className="flex flex-col gap-5">
                {related.map((a, i) => (
                  <React.Fragment key={a.slug}>
                    {i > 0 && <div className="w-full h-px bg-gray-100"></div>}
                    <Link href={`/articles/${a.slug}`} className="flex gap-4 group cursor-pointer">
                      <img
                        src={a.hero_image_url || 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=400'}
                        className="w-20 h-20 object-cover rounded-sm shrink-0"
                        alt={a.headline}
                      />
                      <div className="flex flex-col">
                        <span className="text-[10px] font-bold text-gray-500 uppercase tracking-wider mb-1">
                          {formatCategory(a.category)}
                        </span>
                        <span className="font-bold text-sm leading-snug group-hover:fpr-gold transition-colors line-clamp-2 mb-1">
                          {a.headline}
                        </span>
                        <span className="text-xs text-gray-400">{formatDate(a.published_date)}</span>
                      </div>
                    </Link>
                  </React.Fragment>
                ))}
              </div>
            </div>
          )}
          <TopMarketsSidebar />
          <NewsletterCompact />
        </div>

      </main>
    </div>
  );
}
