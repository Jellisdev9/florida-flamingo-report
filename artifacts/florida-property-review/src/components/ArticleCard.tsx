import React from 'react';
import { Link } from 'wouter';

interface ArticleCardProps {
  category: string;
  headline: string;
  date: string;
  readTime: string;
  image: string;
  href?: string;
}

export function ArticleCard({ category, headline, date, readTime, image, href = '/articles/naples-bayfront-estate' }: ArticleCardProps) {
  return (
    <Link href={href} className="group flex flex-col gap-3 group cursor-pointer">
      <div className="relative aspect-[4/3] w-full overflow-hidden rounded-sm">
        <img 
          src={image} 
          alt={headline} 
          className="object-cover w-full h-full transition-transform duration-500 group-hover:scale-105"
        />
      </div>
      <div className="flex flex-col gap-1.5">
        <span className="text-[10px] font-bold tracking-wider fpr-coral uppercase">
          {category}
        </span>
        <h3 className="font-serif text-lg leading-tight font-bold group-hover:text-blue-900 transition-colors line-clamp-3">
          {headline}
        </h3>
        <p className="text-xs text-gray-500 mt-1">
          {date} &middot; {readTime} read
        </p>
      </div>
    </Link>
  );
}
