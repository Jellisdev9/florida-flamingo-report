# Florida Property Review — Handoff / Progress Snapshot
**Date:** 2026-06-30

---

## What This Project Is

Editorial real estate publication for Florida.  
**Stack:** React 19 + Vite + TypeScript SPA (this folder) wired to a Django 5 + DRF backend at `../../backend/`.

---

## What Is Complete

### Backend (`../../backend/`)
All four Django apps scaffolded, migrated, seeded, and tested.

| App | Models | API Endpoints | Tests |
|-----|--------|---------------|-------|
| `articles` | `Article` | `GET /api/articles/`, `/api/articles/featured/`, `/api/articles/<slug>/` | ✅ test_models + test_views |
| `sales` | `NotableSale` | `GET /api/sales/`, `/api/sales/featured/`, `/api/sales/top-closings/` | ✅ test_models + test_views |
| `market` | `MarketMetric`, `Agent`, `NeighborhoodIntel`, `FastestGrowingMarket` | `GET /api/market/metrics/`, `/api/market/neighborhoods/`, `/api/market/fastest-growing/`, `/api/agents/top/` | ✅ test_models + test_views |
| `subscribers` | `Subscriber` | `POST /api/subscribers/` | ✅ test_models + test_views |

Seed data: `../../backend/fixtures/initial_data.json` (29 objects covering all models).

### Frontend (`src/`)
All components wired to the Django API — **no more hardcoded mock data**.

| File | Status |
|------|--------|
| `src/lib/api.ts` | ✅ All TypeScript types + `formatDate`, `formatCategory`, `REGION_MAP`, `api.*` fetch functions |
| `src/hooks/useApi.ts` | ✅ All React Query hooks (`useArticles`, `useFeaturedArticle`, `useArticle`, `useSales`, `useFeaturedSale`, `useTopClosings`, `useMarketMetrics`, `useNeighborhoodIntel`, `useFastestGrowingMarkets`, `useTopAgents`, `useSubscribe`) |
| `src/components/MarketStrip.tsx` | ✅ Wired — `useMarketMetrics()` |
| `src/components/Sidebar.tsx` | ✅ Wired — `TopMarketsSidebar` (metrics), `TopAgentsSidebar` (agents), `NewsletterCompact` (subscribe mutation) |
| `src/pages/HomePage.tsx` | ✅ Wired — featured article hero, article cards grid, luxury closings, neighborhood intel, newsletter banner |
| `src/pages/NotableSalesPage.tsx` | ✅ Wired — featured sale hero, region-filtered sales grid, top closings sidebar, fastest growing markets sidebar, subscribe CTA |
| `src/pages/ArticlePage.tsx` | ✅ Wired — article detail by slug (`useParams`), related stories (same category), Sale Facts card (when `sale_facts` not null) |
| `vite.config.ts` | ✅ Proxy `/api` → `http://localhost:8000` (or `$DJANGO_API_URL`) |

---

## What Is NOT Done — The Next Task

### Frontend test infrastructure does not exist yet.

The project chose **TDD red/green** from the start. The backend was done TDD. The React wiring was done without tests (acknowledged mistake). The agreed plan is:

> **Option A** — Set up Vitest + React Testing Library + MSW retroactively, write tests for all wired components/hooks. All tests should be green since the implementation already exists. Re-establish strict TDD going forward.

**No test files exist yet** in `src/`. The packages below are not installed.

---

## Step 1 — Install Test Packages

Run from this directory (`artifacts/florida-property-review/`):

```bash
pnpm add -D vitest jsdom @testing-library/react @testing-library/user-event @testing-library/jest-dom msw
```

Then update `package.json` scripts (add after `"typecheck"`):

```json
"test": "vitest --config vitest.config.ts",
"test:run": "vitest run --config vitest.config.ts"
```

---

## Step 2 — Create Test Infrastructure Files

### `vitest.config.ts` (root of this folder)

```typescript
import { defineConfig } from 'vitest/config';
import { fileURLToPath, URL } from 'node:url';

export default defineConfig({
  test: {
    globals: true,
    environment: 'jsdom',
    environmentOptions: {
      jsdom: { url: 'http://localhost/' },
    },
    setupFiles: ['./src/test/setup.ts'],
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
});
```

### `src/test/setup.ts`

```typescript
import '@testing-library/jest-dom';
import { server } from '@/mocks/server';
import { beforeAll, afterEach, afterAll } from 'vitest';

beforeAll(() => server.listen({ onUnhandledRequest: 'error' }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

### `src/test/utils.tsx`

```tsx
import React from 'react';
import { render, type RenderOptions } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Router } from 'wouter';

function makeQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: { retry: false, gcTime: 0 },
      mutations: { retry: false },
    },
  });
}

export function renderWithProviders(ui: React.ReactElement, options?: RenderOptions) {
  const queryClient = makeQueryClient();
  function Wrapper({ children }: { children: React.ReactNode }) {
    return (
      <QueryClientProvider client={queryClient}>
        <Router>{children}</Router>
      </QueryClientProvider>
    );
  }
  return render(ui, { wrapper: Wrapper, ...options });
}
```

### `src/mocks/fixtures.ts`

Mock data matching exact API response shapes (used by MSW handlers):

```typescript
import type {
  Article, ArticleDetail, NotableSale, MarketMetric,
  Agent, NeighborhoodIntel, FastestGrowingMarket, PaginatedResponse,
} from '@/lib/api';

export const mockArticle: Article = {
  slug: 'naples-bayfront-estate',
  headline: '$32.5M Naples Bayfront Estate Sets a New Benchmark',
  subheadline: 'A rare bayside compound in Port Royal redefines luxury waterfront living.',
  category: 'NOTABLE_SALE',
  byline: 'By Caroline Bennett, Senior Real Estate Editor',
  read_time_minutes: 5,
  hero_image_url: 'https://example.com/hero.jpg',
  published_date: '2024-05-12',
  is_featured: true,
};

export const mockArticleDetail: ArticleDetail = {
  ...mockArticle,
  title: '$32.5M Naples Bayfront Estate Sets a New Benchmark',
  body: 'First paragraph of the article.\n\nSecond paragraph of the article.',
  author_avatar_url: 'https://example.com/avatar.jpg',
  is_published: true,
  sale_facts: {
    price_display: '$32,500,000',
    location: '3255 Fort Charles Drive, Naples, FL',
    brokerage: "Premier Sotheby's International Realty",
    beds: 8,
    baths: 10.5,
    sq_ft: 11276,
  },
};

export const mockArticlesPage: PaginatedResponse<Article> = {
  count: 1, next: null, previous: null,
  results: [mockArticle],
};

export const mockSale: NotableSale = {
  slug: 'la-gorce-island',
  title: 'La Gorce Island Waterfront Estate',
  price: '48000000.00',
  price_display: '$48,000,000',
  city: 'Miami Beach',
  region: 'SOUTH_FLORIDA',
  property_type: 'WATERFRONT_ESTATE',
  close_date: '2024-05-09',
  hero_image_url: 'https://example.com/sale.jpg',
  is_featured: true,
  article: null,
  brokerage: 'Douglas Elliman',
  beds: 8,
  baths: '9.5',
  sq_ft: 12000,
};

export const mockSalesPage: PaginatedResponse<NotableSale> = {
  count: 1, next: null, previous: null,
  results: [mockSale],
};

export const mockMetrics: MarketMetric[] = [
  { city: 'Miami', metric_label: 'Median Price', value_display: '$685,000', change_display: '+6.2%', is_positive: true },
  { city: 'Tampa', metric_label: 'Inventory', value_display: '3.1 Months', change_display: '-4.8%', is_positive: false },
];

export const mockAgents: Agent[] = [
  { rank: 1, name: 'The Jills Zeder Group', location: 'Miami Beach', volume_display: '$98.4M' },
  { rank: 2, name: 'Corcoran Reverie Group', location: 'Naples', volume_display: '$72.1M' },
];

export const mockNeighborhoods: NeighborhoodIntel[] = [
  { neighborhood: 'Winter Park', city: 'Orlando', description: 'Inventory hits 18-month low.', tag: 'HOT' },
  { neighborhood: 'St. Petersburg', city: 'Tampa Bay', description: 'Downtown condo prices surge.', tag: 'RISING' },
];

export const mockFastestGrowing: FastestGrowingMarket[] = [
  { rank: 1, location: 'Winter Park', change_display: '+18.7%' },
  { rank: 2, location: 'West Palm Beach', change_display: '+14.2%' },
];

export const mockTopClosings: NotableSale[] = [
  mockSale,
  { ...mockSale, slug: 'boca-raton-estate', title: 'Boca Raton Estate', price_display: '$32,500,000', city: 'Boca Raton' },
];
```

### `src/mocks/handlers.ts`

```typescript
import { http, HttpResponse } from 'msw';
import {
  mockArticlesPage, mockArticleDetail, mockSale, mockSalesPage,
  mockMetrics, mockAgents, mockNeighborhoods, mockFastestGrowing, mockTopClosings,
} from './fixtures';

export const handlers = [
  http.get('http://localhost/api/articles/', ({ request }) => {
    const url = new URL(request.url);
    const category = url.searchParams.get('category');
    if (category) {
      const filtered = mockArticlesPage.results.filter(a => a.category === category);
      return HttpResponse.json({ ...mockArticlesPage, results: filtered, count: filtered.length });
    }
    return HttpResponse.json(mockArticlesPage);
  }),

  http.get('http://localhost/api/articles/featured/', () =>
    HttpResponse.json(mockArticleDetail)),

  http.get('http://localhost/api/articles/:slug', ({ params }) => {
    if (params.slug === 'naples-bayfront-estate') return HttpResponse.json(mockArticleDetail);
    return new HttpResponse(null, { status: 404 });
  }),

  http.get('http://localhost/api/sales/', ({ request }) => {
    const url = new URL(request.url);
    const region = url.searchParams.get('region');
    if (region) {
      const filtered = mockSalesPage.results.filter(s => s.region === region);
      return HttpResponse.json({ ...mockSalesPage, results: filtered, count: filtered.length });
    }
    return HttpResponse.json(mockSalesPage);
  }),

  http.get('http://localhost/api/sales/featured/', () =>
    HttpResponse.json(mockSale)),

  http.get('http://localhost/api/sales/top-closings/', () =>
    HttpResponse.json(mockTopClosings)),

  http.get('http://localhost/api/market/metrics/', () =>
    HttpResponse.json(mockMetrics)),

  http.get('http://localhost/api/market/neighborhoods/', () =>
    HttpResponse.json(mockNeighborhoods)),

  http.get('http://localhost/api/market/fastest-growing/', () =>
    HttpResponse.json(mockFastestGrowing)),

  http.get('http://localhost/api/agents/top/', () =>
    HttpResponse.json(mockAgents)),

  http.post('http://localhost/api/subscribers/', () =>
    HttpResponse.json({ message: 'Subscribed successfully.' }, { status: 201 })),
];
```

### `src/mocks/server.ts`

```typescript
import { setupServer } from 'msw/node';
import { handlers } from './handlers';

export const server = setupServer(...handlers);
```

---

## Step 3 — Write the Test Files

All tests should pass (green) since the implementations are complete. Write them TDD-style by asserting behaviour, not implementation.

### `src/lib/api.test.ts`

Test `formatDate`, `formatCategory`, `REGION_MAP`:

```typescript
import { describe, it, expect } from 'vitest';
import { formatDate, formatCategory, REGION_MAP } from '@/lib/api';

describe('formatDate', () => {
  it('formats ISO date string to long locale date', () => {
    expect(formatDate('2024-05-12')).toBe('May 12, 2024');
  });
  it('handles January correctly (month - 1)', () => {
    expect(formatDate('2024-01-01')).toBe('January 1, 2024');
  });
});

describe('formatCategory', () => {
  it('replaces underscores with spaces', () => {
    expect(formatCategory('NOTABLE_SALE')).toBe('NOTABLE SALE');
    expect(formatCategory('AGENT_WATCH')).toBe('AGENT WATCH');
  });
  it('leaves categories with no underscores unchanged', () => {
    expect(formatCategory('DEVELOPMENT')).toBe('DEVELOPMENT');
  });
});

describe('REGION_MAP', () => {
  it('maps All Regions to empty string', () => {
    expect(REGION_MAP['All Regions']).toBe('');
  });
  it('maps display names to API enum values', () => {
    expect(REGION_MAP['South Florida']).toBe('SOUTH_FLORIDA');
    expect(REGION_MAP['Tampa Bay']).toBe('TAMPA_BAY');
    expect(REGION_MAP['Orlando']).toBe('ORLANDO');
  });
});
```

### `src/components/MarketStrip.test.tsx`

```tsx
import { describe, it, expect } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import { MarketStrip } from '@/components/MarketStrip';
import { renderWithProviders } from '@/test/utils';

describe('MarketStrip', () => {
  it('renders city names from the API', async () => {
    renderWithProviders(<MarketStrip />);
    await waitFor(() => {
      expect(screen.getByText(/Miami/)).toBeInTheDocument();
      expect(screen.getByText(/Tampa/)).toBeInTheDocument();
    });
  });

  it('renders value_display for each metric', async () => {
    renderWithProviders(<MarketStrip />);
    await waitFor(() => {
      expect(screen.getByText('$685,000')).toBeInTheDocument();
      expect(screen.getByText('3.1 Months')).toBeInTheDocument();
    });
  });

  it('renders change_display for each metric', async () => {
    renderWithProviders(<MarketStrip />);
    await waitFor(() => {
      expect(screen.getByText('+6.2%')).toBeInTheDocument();
      expect(screen.getByText('-4.8%')).toBeInTheDocument();
    });
  });
});
```

### `src/components/Sidebar.test.tsx`

```tsx
import { describe, it, expect } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { TopMarketsSidebar, TopAgentsSidebar, NewsletterCompact } from '@/components/Sidebar';
import { renderWithProviders } from '@/test/utils';

describe('TopMarketsSidebar', () => {
  it('renders city names and values from the API', async () => {
    renderWithProviders(<TopMarketsSidebar />);
    await waitFor(() => {
      expect(screen.getByText('Miami')).toBeInTheDocument();
      expect(screen.getByText('$685,000')).toBeInTheDocument();
      expect(screen.getByText('+6.2%')).toBeInTheDocument();
    });
  });
});

describe('TopAgentsSidebar', () => {
  it('renders agent names, locations, and volume from the API', async () => {
    renderWithProviders(<TopAgentsSidebar />);
    await waitFor(() => {
      expect(screen.getByText('The Jills Zeder Group')).toBeInTheDocument();
      expect(screen.getByText(/\$98\.4M/)).toBeInTheDocument();
      expect(screen.getByText('Corcoran Reverie Group')).toBeInTheDocument();
    });
  });

  it('renders rank numbers', async () => {
    renderWithProviders(<TopAgentsSidebar />);
    await waitFor(() => {
      expect(screen.getByText('1')).toBeInTheDocument();
      expect(screen.getByText('2')).toBeInTheDocument();
    });
  });
});

describe('NewsletterCompact', () => {
  it('renders email input and subscribe button', () => {
    renderWithProviders(<NewsletterCompact />);
    expect(screen.getByPlaceholderText('Email address')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /subscribe/i })).toBeInTheDocument();
  });

  it('shows success message after subscribing', async () => {
    const user = userEvent.setup();
    renderWithProviders(<NewsletterCompact />);
    await user.type(screen.getByPlaceholderText('Email address'), 'test@example.com');
    await user.click(screen.getByRole('button', { name: /subscribe/i }));
    await waitFor(() => {
      expect(screen.getByText(/subscribed/i)).toBeInTheDocument();
    });
  });
});
```

### `src/pages/HomePage.test.tsx`

```tsx
import { describe, it, expect } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { HomePage } from '@/pages/HomePage';
import { renderWithProviders } from '@/test/utils';

describe('HomePage', () => {
  it('renders the featured article headline in the hero', async () => {
    renderWithProviders(<HomePage />);
    await waitFor(() => {
      expect(screen.getByText('$32.5M Naples Bayfront Estate Sets a New Benchmark')).toBeInTheDocument();
    });
  });

  it('renders article cards from the API', async () => {
    renderWithProviders(<HomePage />);
    await waitFor(() => {
      // Article card headline should appear
      expect(screen.getAllByText('$32.5M Naples Bayfront Estate Sets a New Benchmark').length).toBeGreaterThan(0);
    });
  });

  it('renders luxury closings with price and title', async () => {
    renderWithProviders(<HomePage />);
    await waitFor(() => {
      expect(screen.getByText('$48,000,000')).toBeInTheDocument();
      expect(screen.getByText('La Gorce Island Waterfront Estate')).toBeInTheDocument();
    });
  });

  it('renders neighborhood intelligence cards', async () => {
    renderWithProviders(<HomePage />);
    await waitFor(() => {
      expect(screen.getByText('Winter Park')).toBeInTheDocument();
      expect(screen.getByText('Inventory hits 18-month low.')).toBeInTheDocument();
      expect(screen.getByText('HOT')).toBeInTheDocument();
    });
  });

  it('shows success message after subscribing via newsletter banner', async () => {
    const user = userEvent.setup();
    renderWithProviders(<HomePage />);
    const emailInput = screen.getByPlaceholderText('Your email address');
    await user.type(emailInput, 'reader@example.com');
    await user.click(screen.getByRole('button', { name: /subscribe/i }));
    await waitFor(() => {
      expect(screen.getByText(/subscribed/i)).toBeInTheDocument();
    });
  });
});
```

### `src/pages/NotableSalesPage.test.tsx`

```tsx
import { describe, it, expect } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { NotableSalesPage } from '@/pages/NotableSalesPage';
import { renderWithProviders } from '@/test/utils';

describe('NotableSalesPage', () => {
  it('renders the page heading', () => {
    renderWithProviders(<NotableSalesPage />);
    expect(screen.getByRole('heading', { name: /Notable Sales/i, level: 1 })).toBeInTheDocument();
  });

  it('renders the featured sale title', async () => {
    renderWithProviders(<NotableSalesPage />);
    await waitFor(() => {
      expect(screen.getByText('La Gorce Island Waterfront Estate')).toBeInTheDocument();
    });
  });

  it('renders region filter tabs', () => {
    renderWithProviders(<NotableSalesPage />);
    expect(screen.getByRole('button', { name: 'All Regions' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'South Florida' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Tampa Bay' })).toBeInTheDocument();
  });

  it('shows empty state when a region has no sales', async () => {
    const user = userEvent.setup();
    renderWithProviders(<NotableSalesPage />);
    // Tampa Bay tab — mock handler returns empty for TAMPA_BAY filter
    await user.click(screen.getByRole('button', { name: 'Tampa Bay' }));
    await waitFor(() => {
      expect(screen.getByText('No sales found for this region.')).toBeInTheDocument();
    });
  });

  it('renders fastest growing markets', async () => {
    renderWithProviders(<NotableSalesPage />);
    await waitFor(() => {
      expect(screen.getByText('Winter Park')).toBeInTheDocument();
      expect(screen.getByText('+18.7%')).toBeInTheDocument();
    });
  });

  it('renders top luxury closings', async () => {
    renderWithProviders(<NotableSalesPage />);
    await waitFor(() => {
      expect(screen.getAllByText('La Gorce Island Waterfront Estate').length).toBeGreaterThan(0);
    });
  });
});
```

### `src/pages/ArticlePage.test.tsx`

`useParams` must be mocked because `ArticlePage` is rendered outside a real wouter `<Route>`.

```tsx
import { describe, it, expect } from 'vitest';
import { vi } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import { renderWithProviders } from '@/test/utils';

// Mock wouter's useParams before importing ArticlePage
vi.mock('wouter', async () => {
  const actual = await vi.importActual<typeof import('wouter')>('wouter');
  return { ...actual, useParams: () => ({ slug: 'naples-bayfront-estate' }) };
});

// Import AFTER the mock is declared
const { ArticlePage } = await import('@/pages/ArticlePage');

describe('ArticlePage', () => {
  it('renders the article headline', async () => {
    renderWithProviders(<ArticlePage />);
    await waitFor(() => {
      expect(screen.getByRole('heading', { level: 1 }))
        .toHaveTextContent('$32.5M Naples Bayfront Estate Sets a New Benchmark');
    });
  });

  it('renders article body paragraphs', async () => {
    renderWithProviders(<ArticlePage />);
    await waitFor(() => {
      expect(screen.getByText('First paragraph of the article.')).toBeInTheDocument();
      expect(screen.getByText('Second paragraph of the article.')).toBeInTheDocument();
    });
  });

  it('renders the Sale Facts card with price and location', async () => {
    renderWithProviders(<ArticlePage />);
    await waitFor(() => {
      expect(screen.getByText('Sale Facts')).toBeInTheDocument();
      expect(screen.getByText('$32,500,000')).toBeInTheDocument();
      expect(screen.getByText('3255 Fort Charles Drive, Naples, FL')).toBeInTheDocument();
    });
  });

  it('renders sale facts property size', async () => {
    renderWithProviders(<ArticlePage />);
    await waitFor(() => {
      expect(screen.getByText(/8 Beds/)).toBeInTheDocument();
      expect(screen.getByText(/11,276 SQ FT/)).toBeInTheDocument();
    });
  });
});

// Separate test for 404 — needs its own useParams mock
describe('ArticlePage (unknown slug)', () => {
  it('shows not found message for unknown slug', async () => {
    vi.doMock('wouter', async () => {
      const actual = await vi.importActual<typeof import('wouter')>('wouter');
      return { ...actual, useParams: () => ({ slug: 'does-not-exist' }) };
    });
    const { ArticlePage: ArticlePageNotFound } = await import('@/pages/ArticlePage');
    renderWithProviders(<ArticlePageNotFound />);
    await waitFor(() => {
      expect(screen.getByText('Article not found.')).toBeInTheDocument();
    });
  });
});
```

---

## Run Commands

### Backend

```bash
cd /home/michaelsullivan/Projects/real-estate/Florida-Front-End/backend

# First-time setup (if needed)
uv sync
uv run python manage.py migrate
uv run python manage.py loaddata fixtures/initial_data.json

# Run dev server
uv run python manage.py runserver 8000

# Run backend tests
uv run python manage.py test
```

### Frontend

```bash
cd /home/michaelsullivan/Projects/real-estate/Florida-Front-End/artifacts/florida-property-review

# Install deps (including new test packages after adding them to package.json)
pnpm install

# Dev server (needs backend running on :8000)
pnpm dev

# Run tests (once infrastructure is in place)
pnpm test:run     # single run (CI)
pnpm test         # watch mode
```

---

## Key Architectural Notes

- **Path alias:** `@` → `src/` (configured in `tsconfig.json` and `vite.config.ts`; must also be in `vitest.config.ts`)
- **Proxy:** Vite proxies `/api/*` → `http://localhost:8000`. In tests, MSW intercepts at `http://localhost/api/*` (jsdom base URL = `http://localhost/`)
- **React Query retries:** Set `retry: false` in test QueryClient to avoid 3-retry delays on expected 404s
- **wouter `useParams`:** Must `vi.mock('wouter', ...)` before importing `ArticlePage` in tests
- **MSW version:** Use v2 syntax — `http.get(...)` from `msw`, `HttpResponse.json(...)` from `msw`
- **Subscriber POST:** Returns 201 on new, 200 on duplicate (not 400). The `post()` helper in `api.ts` only throws on non-ok status.
- **`sale_facts`:** SerializerMethodField on `ArticleDetailSerializer` — reads from the reverse OneToOne `obj.sale`. Only present on `ArticleDetail`, not on `Article` (list type).
- **Agent fixtures:** `period_month=6, period_year=2026` so `top_agents` view returns them for the current month.
- **Python tooling:** `uv` only — no pip, no venv. Dependencies in `backend/pyproject.toml`.
- **JS tooling:** `pnpm` workspaces — workspace root is `Florida-Front-End/`, catalog in `pnpm-workspace.yaml`.

---

## TDD Rule (from project memory)

> **Always write the failing test first, then minimum code to pass.**  
> Backend: `Django TestCase` / `APITestCase` in `<app>/tests/`.  
> Frontend: `Vitest` + `React Testing Library`, colocated `Component.test.tsx`, MSW for API mocking.  
> Never write implementation before the test exists.
