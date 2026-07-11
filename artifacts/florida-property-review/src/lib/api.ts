// ---------- Types ----------

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface Article {
  slug: string;
  headline: string;
  subheadline: string;
  category: string;
  byline: string;
  read_time_minutes: number;
  hero_image_url: string;
  published_date: string;
  is_featured: boolean;
}

export interface SaleFacts {
  price_display: string;
  location: string;
  brokerage: string;
  beds: number | null;
  baths: number | null;
  sq_ft: number | null;
}

export interface ArticleDetail extends Article {
  title: string;
  body: string;
  author_avatar_url: string;
  is_published: boolean;
  sale_facts: SaleFacts | null;
}

export interface NotableSale {
  slug: string;
  title: string;
  price: string;
  price_display: string;
  city: string;
  region: string;
  property_type: string;
  close_date: string;
  hero_image_url: string;
  is_featured: boolean;
  article: number | null;
  brokerage: string;
  beds: number | null;
  baths: string | null;
  sq_ft: number | null;
}

export interface MarketMetric {
  city: string;
  metric_label: string;
  value_display: string;
  change_display: string;
  is_positive: boolean;
}

export interface Agent {
  rank: number;
  name: string;
  location: string;
  volume_display: string;
}

export interface NeighborhoodIntel {
  neighborhood: string;
  city: string;
  description: string;
  tag: 'HOT' | 'RISING' | 'COOLING' | 'STABLE';
}

export interface FastestGrowingMarket {
  rank: number;
  location: string;
  change_display: string;
}

// ---------- Helpers ----------

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`/api${path}`);
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  return res.json() as Promise<T>;
}

async function post<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`/api${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  const data = await res.json().catch(() => ({})) as Record<string, unknown>;
  if (!res.ok) {
    const emailError = (data?.email as string[])?.[0];
    throw new Error(emailError ?? String(res.status));
  }
  return data as T;
}

export function formatDate(dateStr: string): string {
  const [year, month, day] = dateStr.split('-').map(Number);
  return new Date(year, month - 1, day).toLocaleDateString('en-US', {
    month: 'long', day: 'numeric', year: 'numeric',
  });
}

export function formatCategory(category: string): string {
  return category.replace(/_/g, ' ');
}

export const REGION_MAP: Record<string, string> = {
  'All Regions': '',
  'South Florida': 'SOUTH_FLORIDA',
  'Tampa Bay': 'TAMPA_BAY',
  'Orlando': 'ORLANDO',
  'Jacksonville': 'JACKSONVILLE',
  'Panhandle': 'PANHANDLE',
};

// ---------- API ----------

export const api = {
  articles: {
    list: (category?: string) =>
      get<PaginatedResponse<Article>>(`/articles/${category ? `?category=${category}` : ''}`),
    featured: () => get<ArticleDetail>('/articles/featured/'),
    detail: (slug: string) => get<ArticleDetail>(`/articles/${slug}/`),
  },
  sales: {
    list: (region?: string) =>
      get<PaginatedResponse<NotableSale>>(`/sales/${region ? `?region=${region}` : ''}`),
    featured: () => get<NotableSale>('/sales/featured/'),
    topClosings: () => get<NotableSale[]>('/sales/top-closings/'),
  },
  market: {
    metrics: () => get<MarketMetric[]>('/market/metrics/'),
    neighborhoods: () => get<NeighborhoodIntel[]>('/market/neighborhoods/'),
    fastestGrowing: () => get<FastestGrowingMarket[]>('/market/fastest-growing/'),
  },
  agents: {
    top: () => get<Agent[]>('/agents/top/'),
  },
  subscribers: {
    subscribe: (email: string) =>
      post<{ message: string }>('/subscribers/', { email }),
  },
};
