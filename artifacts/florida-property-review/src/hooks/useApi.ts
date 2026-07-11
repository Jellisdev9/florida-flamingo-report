import { useQuery, useMutation } from '@tanstack/react-query';
import { api } from '@/lib/api';

export function useArticles(category?: string) {
  return useQuery({
    queryKey: ['articles', category ?? 'all'],
    queryFn: () => api.articles.list(category),
  });
}

export function useFeaturedArticle() {
  return useQuery({
    queryKey: ['articles', 'featured'],
    queryFn: api.articles.featured,
  });
}

export function useArticle(slug: string) {
  return useQuery({
    queryKey: ['articles', slug],
    queryFn: () => api.articles.detail(slug),
    enabled: !!slug,
  });
}

export function useSales(region?: string) {
  return useQuery({
    queryKey: ['sales', region ?? 'all'],
    queryFn: () => api.sales.list(region),
  });
}

export function useFeaturedSale() {
  return useQuery({
    queryKey: ['sales', 'featured'],
    queryFn: api.sales.featured,
  });
}

export function useTopClosings() {
  return useQuery({
    queryKey: ['sales', 'top-closings'],
    queryFn: api.sales.topClosings,
  });
}

export function useMarketMetrics() {
  return useQuery({
    queryKey: ['market', 'metrics'],
    queryFn: api.market.metrics,
  });
}

export function useNeighborhoodIntel() {
  return useQuery({
    queryKey: ['market', 'neighborhoods'],
    queryFn: api.market.neighborhoods,
  });
}

export function useFastestGrowingMarkets() {
  return useQuery({
    queryKey: ['market', 'fastest-growing'],
    queryFn: api.market.fastestGrowing,
  });
}

export function useTopAgents() {
  return useQuery({
    queryKey: ['agents', 'top'],
    queryFn: api.agents.top,
  });
}

export function useSubscribe() {
  return useMutation({
    mutationFn: (email: string) => api.subscribers.subscribe(email),
  });
}
