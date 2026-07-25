# Florida Property Review — Frontend Architecture & Implementation Plan

> **Audience:** This document assumes no prior knowledge of Node.js or React.
> Every concept is explained from first principles. If you already know something,
> skip that section — but everything here is intentional and educational.

---

## Table of Contents

1. [The Big Picture — What Is a "Frontend"?](#1-the-big-picture)
2. [The Tech Stack — Every Tool Explained](#2-the-tech-stack)
3. [How the Project Is Laid Out on Disk](#3-project-structure)
4. [How Data Flows Through the App (Request Lifecycle)](#4-data-flow)
5. [The Architecture Patterns We Use](#5-architecture-patterns)
6. [Every File That Exists Today](#6-file-inventory)
7. [Environment Setup — Getting Node.js and pnpm Running](#7-environment-setup)
8. [The Test Infrastructure Plan (Next Major Task)](#8-test-infrastructure)
9. [Future Feature Roadmap](#9-future-features)
10. [Commenting Convention](#10-commenting-convention)

---

## 1. The Big Picture

### What is a "frontend"?

A **frontend** is the code that runs inside the user's web browser. When someone visits
`floridapropertyreview.com`, their browser downloads a bundle of HTML, CSS, and JavaScript
files from a server, and that JavaScript code then draws the entire page and handles all
user interaction — clicking tabs, submitting forms, etc.

Our frontend is a **Single-Page Application (SPA)**. That means:
- The browser downloads the app **once** at the first page load.
- After that, clicking links like "Notable Sales" does **not** load a new page from the server.
  Instead, JavaScript swaps out what's visible on screen — instantly, with no reload.
- All actual data (articles, sale prices, market stats) comes from a separate **API server**
  (our Django backend) via background network requests called **fetch calls**.

### Why separate frontend and backend?

The Django backend is the "source of truth" — it owns the database and the business logic.
The React frontend is purely a display layer. This separation means:
- We can update the design without touching the database.
- We can add a mobile app later that talks to the same Django API.
- Frontend and backend developers can work independently.

---

## 2. The Tech Stack

### Node.js

**What it is:** A JavaScript runtime that lets you run JavaScript *outside* a browser —
on your laptop or server. You don't write your application in Node.js directly; you use it
as the engine that runs all the build tools.

**Analogy:** Node.js is like Python for JavaScript. Just as `python script.py` runs a Python
file on the command line, `node script.js` runs a JavaScript file.

**We need it because:** Vite (our build tool), pnpm (our package manager), and Vitest (our
test runner) are all Node.js programs. Without Node.js installed, none of those commands work.

---

### pnpm (Package Manager)

**What it is:** A tool for downloading and managing JavaScript libraries ("packages").
When our code says `import { motion } from 'framer-motion'`, pnpm is what downloaded
the `framer-motion` library onto disk so that import can resolve.

**Where packages live:** `node_modules/` folder inside the project. This folder can be
hundreds of megabytes and is never committed to git (it's in `.gitignore`). Anyone who
clones the repo runs `pnpm install` to recreate it from the `pnpm-lock.yaml` manifest.

**Why pnpm not npm/yarn?** pnpm is faster and more disk-efficient. It uses a shared global
store and hard-links packages instead of copying them. This workspace (the whole
`florida-front-end/` directory) has a `pnpm-workspace.yaml` that ties all sub-packages
together so they can share dependencies.

**Key commands:**
```bash
pnpm install          # install all packages listed in package.json
pnpm add <name>       # add a new package as a runtime dependency
pnpm add -D <name>    # add a new package as a dev-only dependency (tests, build tools)
pnpm dev              # run the dev server (defined in package.json "scripts")
pnpm test             # run tests (once we set this up)
```

---

### Vite

**What it is:** The build tool that transforms our TypeScript + React source code into
plain JavaScript that browsers can actually understand.

Browsers cannot natively run TypeScript or JSX (the HTML-like syntax we write in React).
Vite compiles it down and bundles it into regular `.js` files.

**In development mode (`pnpm dev`):**
- Vite starts a local web server at `http://localhost:5173`
- It watches your files for changes and hot-reloads the browser instantly when you save
- It proxies any request starting with `/api` to Django at `http://localhost:8000`
  (this is how the frontend talks to the backend without CORS issues in dev)

**In production (`pnpm build`):**
- Vite compiles and minifies everything into a `dist/public/` folder
- Those static files are then served by nginx or a CDN

**Config file:** `vite.config.ts` at the root of `artifacts/florida-property-review/`

---

### TypeScript

**What it is:** JavaScript with a type system bolted on. Types are annotations that
describe what kind of data a variable holds.

**Example:**
```typescript
// Plain JavaScript — no idea what `sale` contains
function showPrice(sale) {
  return sale.price_display;
}

// TypeScript — the compiler knows exactly what fields exist on NotableSale
function showPrice(sale: NotableSale): string {
  return sale.price_display; // autocomplete works, typos are caught at compile time
}
```

TypeScript is compiled away before the browser sees it — browsers only run JavaScript.
The TypeScript compiler (`tsc`) just checks your code for mistakes.

**Why it matters here:** We define interfaces like `Article`, `NotableSale`, `MarketMetric`
in `src/lib/api.ts`. Those types are used everywhere. If the Django API changes a field name,
TypeScript will highlight every place the old name was used.

---

### React

**What it is:** A JavaScript library for building user interfaces. The core idea is
**components**: small, reusable pieces of UI that each manage their own state and render
themselves as HTML.

**A component is just a function that returns HTML-like syntax:**
```tsx
// This is a React component — a function that returns JSX
function WelcomeMessage({ name }: { name: string }) {
  return (
    <div className="greeting">
      <h1>Hello, {name}!</h1>
    </div>
  );
}

// Used like an HTML tag anywhere else in the app:
<WelcomeMessage name="Michael" />
```

The HTML-like syntax inside JavaScript is called **JSX** (JavaScript XML). Vite/Babel
compiles it into regular function calls before it runs.

**State:** When a value in a component can change over time (e.g. the selected region tab,
or an email input value), we store it in `useState`. React re-renders the component
automatically when state changes.

```tsx
const [activeTab, setActiveTab] = useState('All Regions');
// activeTab = current value
// setActiveTab = function to update it (triggers a re-render)
```

**Props:** Values passed *into* a component from its parent, like HTML attributes.
```tsx
<ArticleCard headline="Big Sale" date="June 2025" />
```

---

### Tailwind CSS

**What it is:** A CSS framework where instead of writing a separate `.css` file, you
apply pre-made utility classes directly in your JSX.

```tsx
// Without Tailwind — you'd write custom CSS in a separate file
<div className="article-card">...</div>

// With Tailwind — styling is inline via utility classes
<div className="bg-white border border-gray-200 rounded-sm p-5 shadow-sm">...</div>
// bg-white = white background
// border border-gray-200 = thin gray border
// rounded-sm = slightly rounded corners
// p-5 = 20px padding on all sides
// shadow-sm = subtle drop shadow
```

Our app also defines custom brand colors (FPR navy, coral, gold, teal) as CSS variables
in `index.css` and uses them as classes like `fpr-navy`, `fpr-coral`, `fpr-gold-bg`.

---

### @tanstack/react-query (TanStack Query)

**What it is:** A library that manages all network requests (fetching data from the API)
in a React app. Without it, you'd manually handle loading states, error states, caching,
and re-fetching — a lot of boilerplate.

**The core concept — `useQuery`:**
```tsx
// This one line does ALL of this:
// 1. Makes a GET request to /api/articles/ on first render
// 2. Shows `isLoading = true` while waiting
// 3. Stores the result in a cache keyed by ['articles', 'all']
// 4. If the same query is needed elsewhere, returns the cached value instantly
// 5. Re-fetches in the background when the window regains focus
const { data, isLoading, error } = useQuery({
  queryKey: ['articles', 'all'],     // cache key — must be unique per request
  queryFn: () => api.articles.list(), // the actual fetch function to call
});
```

**`useMutation` for POST requests (e.g. newsletter subscribe):**
```tsx
const subscribe = useMutation({
  mutationFn: (email: string) => api.subscribers.subscribe(email),
});

// To trigger it:
subscribe.mutate('user@example.com', {
  onSuccess: () => setSubscribed(true),
});
```

The global `QueryClient` (created in `App.tsx`) owns the cache. Every component in the
tree can read from it. `QueryClientProvider` wraps the whole app so every component
can access the client via hooks.

---

### wouter

**What it is:** A lightweight client-side router — it maps URL paths to React components
without reloading the page.

```tsx
// When the URL is "/", render HomePage
// When the URL is "/articles/naples-bayfront-estate", render ArticlePage
// When the URL is "/notable-sales", render NotableSalesPage
<Switch>
  <Route path="/" component={HomePage} />
  <Route path="/articles/:slug" component={ArticlePage} />
  <Route path="/notable-sales" component={NotableSalesPage} />
</Switch>
```

The `:slug` is a **route parameter** — a variable part of the URL. In `ArticlePage`,
we read it with `useParams()` to know which article to fetch.

---

### framer-motion

**What it is:** An animation library for React. We use it for fade-in transitions on
the article cards grid and the sales grid when the region filter changes.

---

### shadcn/ui + Radix UI

**What they are:** Pre-built, accessible UI components (dialogs, tooltips, tabs, etc.)
that we can import and use. Radix provides the logic and accessibility; shadcn provides
the styling layer on top. These live in `src/components/ui/`.

---

## 3. Project Structure

```
florida-front-end/                      ← Workspace root (pnpm workspace)
├── pnpm-workspace.yaml                 ← Tells pnpm which folders are packages
├── pnpm-lock.yaml                      ← Exact versions of every installed package (committed to git)
├── package.json                        ← Workspace-level dependencies
├── CLAUDE.md                           ← Instructions for the AI assistant
├── FRONTEND_PLAN.md                    ← This document
│
├── backend/                            ← Django API (separate from this doc's scope)
│
└── artifacts/
    └── florida-property-review/        ← The React SPA package
        ├── package.json                ← This app's dependencies and scripts
        ├── vite.config.ts              ← Build tool config (proxy, aliases, plugins)
        ├── tsconfig.json               ← TypeScript compiler config
        ├── index.html                  ← The single HTML file (entry point)
        └── src/
            ├── main.tsx                ← Entry point: mounts <App /> into index.html
            ├── App.tsx                 ← Root component: sets up providers + routing
            ├── index.css               ← Global CSS (brand colors, fonts, resets)
            │
            ├── lib/
            │   └── api.ts              ← All TypeScript types + all fetch functions
            │
            ├── hooks/
            │   └── useApi.ts           ← All React Query hooks (thin wrappers over api.ts)
            │
            ├── components/
            │   ├── Header.tsx          ← Top navigation bar + MarketStrip
            │   ├── MarketStrip.tsx     ← Scrollable ticker of market metrics
            │   ├── Sidebar.tsx         ← TopMarketsSidebar, TopAgentsSidebar, NewsletterCompact
            │   ├── ArticleCard.tsx     ← Reusable card for article previews
            │   └── ui/                 ← shadcn/ui auto-generated components
            │
            └── pages/
                ├── HomePage.tsx        ← "/" route
                ├── ArticlePage.tsx     ← "/articles/:slug" route
                ├── NotableSalesPage.tsx ← "/notable-sales" route
                └── not-found.tsx       ← Catch-all 404 page
```

### Why this folder structure?

- **`lib/`** — "dumb" utilities: types and raw fetch functions. No React, no hooks.
  Pure TypeScript. Could be used in a Node.js script or a test without a browser.
- **`hooks/`** — React-specific data-fetching logic. Wraps `lib/api.ts` in `useQuery`/
  `useMutation`. Each hook is a single responsibility (one endpoint).
- **`components/`** — Reusable UI pieces used by multiple pages.
- **`pages/`** — Full page layouts. One file per route. Pages compose components together.

---

## 4. Data Flow

Here is exactly what happens when a user visits the home page:

```
1. Browser requests https://floridapropertyreview.com/
   └── Server returns index.html (one tiny HTML file)

2. index.html loads the compiled JavaScript bundle (main.tsx entry point)
   └── React boots up, App.tsx runs

3. App.tsx wraps everything in:
   - <QueryClientProvider>   ← gives all components access to the data cache
   - <TooltipProvider>       ← shadcn tooltip context
   - <WouterRouter>          ← enables client-side routing

4. wouter sees the URL is "/" → renders <HomePage />

5. HomePage renders immediately (empty/loading state visible to user)
   └── It calls several hooks:
       - useFeaturedArticle()       → fires GET /api/articles/featured/
       - useArticles()              → fires GET /api/articles/
       - useTopClosings()           → fires GET /api/sales/top-closings/
       - useNeighborhoodIntel()     → fires GET /api/market/neighborhoods/

6. Each hook uses useQuery() from TanStack Query:
   - Check cache: is this data already cached? If yes, return it instantly.
   - If not cached: call the queryFn (e.g. api.articles.featured())

7. api.articles.featured() calls fetch('/api/articles/featured/')
   - In development: Vite proxy intercepts this and forwards it to http://localhost:8000/api/articles/featured/
   - In production: nginx proxies /api/* to the Django server

8. Django receives the request, queries PostgreSQL, serializes the data to JSON, returns it

9. fetch() resolves with the JSON. TanStack Query:
   - Stores the result in the cache (keyed by ['articles', 'featured'])
   - Triggers a React re-render of every component that called useFeaturedArticle()

10. HomePage re-renders with real data — the hero image, headline, article cards all appear
```

---

## 5. Architecture Patterns

### Pattern 1: The Three-Layer Data Stack

Every piece of data follows the same path through three layers:

```
Layer 1: Types + Raw Fetch     (src/lib/api.ts)
    ↕ imported by
Layer 2: React Query Hooks     (src/hooks/useApi.ts)
    ↕ imported by
Layer 3: Components / Pages    (src/pages/*.tsx, src/components/*.tsx)
```

**Why three layers?**

- **Layer 1 (api.ts)** knows about HTTP and JSON. It can be tested without React.
- **Layer 2 (useApi.ts)** knows about React's lifecycle. It handles caching, loading state,
  error state, and re-fetching. It knows nothing about what the data looks like on screen.
- **Layer 3 (pages/components)** knows about HTML and user interaction. It knows nothing
  about how the data arrived.

This separation means: if we switch from REST to GraphQL, we only change Layer 1.
If we switch from TanStack Query to SWR, we only change Layer 2.

---

### Pattern 2: Component Composition

Pages don't contain all their own HTML — they are assembled from smaller components.

```
HomePage
├── Header              ← nav bar + market strip ticker
├── [hero section]      ← inline JSX in HomePage (large, not reused)
├── TopMarketsSidebar   ← reusable sidebar widget
├── ArticleCard × 5     ← reusable card, one per article
├── TopAgentsSidebar    ← reusable sidebar widget
└── [newsletter banner] ← inline JSX in HomePage (not reused)
```

`TopMarketsSidebar` is used on both `HomePage` and `ArticlePage`. Because it's its own
component, the data-fetching logic (the `useMarketMetrics()` hook call) lives in one place.
Both pages get it for free.

---

### Pattern 3: Custom Hooks

A **custom hook** is a function whose name starts with `use` that calls other hooks inside.
Custom hooks let you extract and reuse stateful logic.

```typescript
// Without a custom hook — you'd write this in every component that needs articles
const { data, isLoading, error } = useQuery({
  queryKey: ['articles', category ?? 'all'],
  queryFn: () => api.articles.list(category),
});

// With a custom hook — one line, readable, reusable
const { data: articlesPage, isLoading } = useArticles(category);
```

Every hook in `useApi.ts` is a thin wrapper. The names are descriptive. Reading a component
file, you immediately understand what data it needs without reading implementation details.

---

### Pattern 4: The @ Path Alias

Throughout the code you'll see imports like:
```typescript
import { api } from '@/lib/api';
import { useMarketMetrics } from '@/hooks/useApi';
```

The `@` is an alias for the `src/` directory. It's configured in both `vite.config.ts`
(for the dev server/build) and `tsconfig.json` (for TypeScript's type checker).

Without this alias, deep files would need ugly relative paths like:
```typescript
import { api } from '../../../lib/api'; // fragile, hard to read
```

---

### Pattern 5: TypeScript Interfaces as the Contract

`src/lib/api.ts` defines interfaces that exactly mirror what Django's serializers return:

```typescript
export interface Article {
  slug: string;            // matches Django: articles/serializers.py fields
  headline: string;
  subheadline: string;
  category: string;        // e.g. "NOTABLE_SALE"
  byline: string;
  read_time_minutes: number;
  hero_image_url: string;
  published_date: string;  // ISO date string: "2024-05-12"
  is_featured: boolean;
}
```

If Django ever renames `headline` to `title`, TypeScript will immediately show errors in
every component that reads `.headline`. This catches integration bugs at compile time
instead of at runtime.

---

## 6. File Inventory

### `src/main.tsx` — Entry Point

The very first JavaScript that runs. It finds the `<div id="root">` in `index.html` and
mounts the React application inside it. You rarely need to edit this file.

---

### `src/App.tsx` — Root Component

Sets up the three global providers that wrap everything:

1. **`QueryClientProvider`** — creates and provides the TanStack Query data cache.
   The `QueryClient` instance controls cache lifetime, retry behavior, etc.
2. **`TooltipProvider`** — enables shadcn tooltip components anywhere in the tree.
3. **`WouterRouter`** — enables client-side routing. The `base` prop is set from
   `import.meta.env.BASE_URL` so the app works when deployed to a subdirectory path.

Also defines the `Router` function which maps URL patterns to page components.

---

### `src/lib/api.ts` — Types and Fetch Functions

**TypeScript interfaces** (the data shapes):
- `PaginatedResponse<T>` — Django REST Framework wraps list endpoints in `{count, next, previous, results[]}`
- `Article` — list-view article (no body text, used for cards)
- `ArticleDetail extends Article` — full article (includes body, sale_facts)
- `SaleFacts` — embedded on ArticleDetail when the article covers a notable sale
- `NotableSale` — a property sale record
- `MarketMetric` — one tile in the market strip header
- `Agent` — top agent leaderboard entry
- `NeighborhoodIntel` — neighborhood watch card
- `FastestGrowingMarket` — one row in the fastest-growing sidebar

**Helper functions:**
- `get<T>(path)` — fires a GET request, throws on non-2xx, returns typed JSON
- `post<T>(path, body)` — fires a POST request, extracts field-level validation errors
- `formatDate('2024-05-12')` → `'May 12, 2024'`
- `formatCategory('NOTABLE_SALE')` → `'NOTABLE SALE'`
- `REGION_MAP` — maps display tab names to API enum values

**`api` object** — namespace for all fetch functions:
```typescript
api.articles.list(category?)   → GET /api/articles/?category=NOTABLE_SALE
api.articles.featured()        → GET /api/articles/featured/
api.articles.detail(slug)      → GET /api/articles/naples-bayfront-estate/
api.sales.list(region?)        → GET /api/sales/?region=SOUTH_FLORIDA
api.sales.featured()           → GET /api/sales/featured/
api.sales.topClosings()        → GET /api/sales/top-closings/
api.market.metrics()           → GET /api/market/metrics/
api.market.neighborhoods()     → GET /api/market/neighborhoods/
api.market.fastestGrowing()    → GET /api/market/fastest-growing/
api.agents.top()               → GET /api/agents/top/
api.subscribers.subscribe(email) → POST /api/subscribers/
```

---

### `src/hooks/useApi.ts` — React Query Hooks

One custom hook per API endpoint. Each hook:
1. Calls `useQuery` with a stable `queryKey` (cache key) and a `queryFn` (the fetch function)
2. Returns the `{ data, isLoading, error }` object from TanStack Query

The `queryKey` must be unique per combination of inputs. For example:
- `['articles', 'all']` — all articles, no category filter
- `['articles', 'NOTABLE_SALE']` — articles filtered to notable sales
- `['articles', 'featured']` — the featured article

TanStack Query will cache each key separately.

`useSubscribe` uses `useMutation` instead of `useQuery` because:
- Mutations are for actions that **change data** (POST, PUT, DELETE)
- Queries are for **reading data** (GET)
- Mutations are triggered manually (`.mutate(...)`) not automatically on render

---

### `src/components/MarketStrip.tsx` — Market Ticker

The horizontal scrolling bar just below the navigation. Shows 5 market metrics
(city, current value, % change vs prior month) from `GET /api/market/metrics/`.

Uses a `TrendingUp` or `TrendingDown` icon from `lucide-react` based on `is_positive`.
Color is applied via the `fpr-green` / `fpr-coral` CSS classes defined in `index.css`.

---

### `src/components/Sidebar.tsx` — Three Sidebar Widgets

Exports three components used in different pages:

1. **`TopMarketsSidebar`** — shows the same market metrics as the strip but in a
   vertical card format. Used on `HomePage` (right of hero) and `ArticlePage`.

2. **`TopAgentsSidebar`** — shows the top agents leaderboard from `GET /api/agents/top/`.
   Used on `HomePage`.

3. **`NewsletterCompact`** — a compact email subscribe form. Used on `ArticlePage` sidebar.
   Manages its own `email` state and `subscribed` state locally.

---

### `src/pages/HomePage.tsx` — The Home Page (`/`)

The most complex page. Composed of:
- **Hero section** — featured article with full-bleed image, pulled from `useFeaturedArticle()`
- **Article cards row** — 5 cards from `useArticles()`, limited with `.slice(0, 5)`
- **Luxury Closings** — top 2 closings from `useTopClosings()` with thumbnail + price
- **Top Agents** — `<TopAgentsSidebar />` component
- **Neighborhood Intelligence** — tag-badged cards from `useNeighborhoodIntel()`
- **Newsletter Banner** — full-width email capture, manages its own subscribe mutation

The `TAG_STYLES` constant maps neighborhood tags (`HOT`, `RISING`, `COOLING`, `STABLE`)
to Tailwind class strings for color coding.

---

### `src/pages/NotableSalesPage.tsx` — The Sales Page (`/notable-sales`)

Layout:
- **Page header** — static title + subtitle
- **Region filter tabs** — `TABS` array drives the tab buttons; `activeTab` state controls
  which tab is active; `REGION_MAP` converts the label to the API enum value
- **Featured sale hero** — large image card from `useFeaturedSale()`
- **Sales grid** — 2-column responsive grid from `useSales(region)`, re-fetches when tab changes
- **Top Luxury Closings sidebar** — ranked list from `useTopClosings()`
- **Fastest Growing Markets sidebar** — ranked list from `useFastestGrowingMarkets()`
- **Subscribe CTA sidebar** — compact subscribe form (manages its own state)

Key detail: `motion.div` from framer-motion wraps the sales grid with `key={activeTab}`.
The `key` prop forces React to unmount and remount the `motion.div` when the tab changes,
which re-triggers the fade-in animation.

---

### `src/pages/ArticlePage.tsx` — The Article Detail Page (`/articles/:slug`)

Reads the `slug` URL parameter via `useParams()`. Fetches:
- `useArticle(slug)` — the full article detail (body, sale_facts, etc.)
- `useArticles(article?.category)` — articles in the same category for "Related Stories"

Renders three states:
- **Loading** — simple "Loading…" message while fetch is in flight
- **Not found** — "Article not found." when the API returns 404 (useQuery throws, data is undefined)
- **Article** — full layout with hero image, body text, Sale Facts card (if `sale_facts` exists),
  and sidebar with related stories + TopMarketsSidebar + NewsletterCompact

The **drop cap** effect on the first paragraph (giant first letter, small caps first line)
is done purely with Tailwind's `first-letter:` and `first-line:` pseudo-element utilities.

**Sale Facts card:** Only rendered when `article.sale_facts !== null`. `sale_facts` is a
computed field on the Django `ArticleDetailSerializer` — it reads from the `NotableSale`
model that has a OneToOne FK back to the article (the `article` field on `NotableSale`).

---

### `vite.config.ts` — Build Configuration

Key things configured here:

1. **`base: basePath`** — the URL base path (defaults to `/`). Allows deploying to a
   subdirectory if needed.

2. **`react()` plugin** — enables JSX compilation and React Fast Refresh (hot reload
   that preserves state while you're developing).

3. **`tailwindcss()` plugin** — integrates Tailwind into Vite's build pipeline.

4. **`resolve.alias`** — sets up `@` → `src/` and `@assets` → `attached_assets/`.

5. **`server.proxy`** — the critical dev configuration: any request to `/api/*` is
   forwarded to `http://localhost:8000` (or `$DJANGO_API_URL`). This means our fetch
   calls to `/api/articles/` in development transparently hit Django.

---

## 7. Environment Setup

### Why Node.js and pnpm are not installed

This repo was built inside Replit (a cloud IDE that provides its own Node environment).
When running locally, Node.js and pnpm must be installed manually.

### Step 1: Install Node.js via nvm

`nvm` (Node Version Manager) is the recommended way to install Node.js on Linux/Mac
because it lets you switch between Node versions per project.

```bash
# Download and run the nvm install script
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

# Reload your shell (so nvm is on the PATH)
source ~/.bashrc   # or source ~/.zshrc if you use zsh

# Install the latest LTS (Long-Term Support) version of Node.js
nvm install --lts

# Verify it worked
node --version    # should print v20.x.x or v22.x.x
npm --version     # should print 10.x.x or similar
```

### Step 2: Enable pnpm via corepack

`corepack` ships with Node.js 16+. It manages alternative package managers like pnpm and yarn.

```bash
# Enable corepack (makes pnpm/yarn commands available)
corepack enable

# Install and activate the latest stable pnpm
corepack prepare pnpm@latest --activate

# Verify
pnpm --version    # should print 9.x.x or 10.x.x
```

### Step 3: Install all project dependencies

From the **workspace root** (`florida-front-end/`):

```bash
pnpm install
```

This reads `pnpm-lock.yaml` and installs the exact versions of every package.
It creates `node_modules/` folders in the workspace root and inside
`artifacts/florida-property-review/`.

### Step 4: Run the dev server (needs Django backend running first)

```bash
# Terminal 1 — Django backend
cd backend
uv run python manage.py runserver 8000

# Terminal 2 — React frontend
cd artifacts/florida-property-review
pnpm dev
# Open http://localhost:5173 in browser
```

---

## 8. Test Infrastructure Plan

### Why tests matter

Without tests:
- You discover bugs by manually clicking through the app after every change.
- A change in one component can silently break another.
- It's impossible to refactor confidently.

With tests:
- A test file describes *exactly what a component should do*.
- Run `pnpm test` and in seconds you know if anything broke.
- Tests also serve as documentation — reading a test tells you the intended behavior.

### What we test (and what we don't)

| What | Why |
|------|-----|
| Component renders correct data from API | The main contract — does the UI show what the API returns? |
| Loading states | User sees "Loading…" while data is in flight |
| Error / empty states | User sees "No sales found." when region has no results |
| User interactions | Click a tab → region filter changes → new API request fires |
| Newsletter form submission | Type email → click subscribe → success message appears |
| `formatDate`, `formatCategory`, `REGION_MAP` | Pure functions, trivial to test |

| What NOT to test | Why |
|------------------|-----|
| Tailwind class names | Not behavior — testing CSS classes is brittle |
| React Query internals | Library is already tested by its authors |
| Django API | Already tested in `backend/*/tests/` |
| That a component renders without crashing | Too weak — assert something meaningful |

### The tools

**Vitest** — the test runner. Works like `pytest` for Python. You write `describe` + `it`
blocks with `expect` assertions. Vitest runs in Node.js (not a browser), which is why we
need jsdom.

**jsdom** — a JavaScript implementation of the browser DOM. Gives Vitest a fake browser
environment so React components can render and be queried without an actual browser.

**React Testing Library (@testing-library/react)** — renders a component into the fake
DOM and gives you query functions to find elements the way a user would:
`screen.getByText('Miami')`, `screen.getByRole('button', { name: /subscribe/i })`.

**@testing-library/user-event** — simulates real user interactions (typing, clicking)
more faithfully than `.click()` on a DOM element.

**@testing-library/jest-dom** — extra assertion matchers:
`expect(el).toBeInTheDocument()`, `expect(el).toHaveTextContent(...)`.

**MSW (Mock Service Worker)** — intercepts `fetch()` calls in tests and returns fake
responses. This is the key: instead of hitting the real Django API (which might not be
running during tests), MSW pretends to be Django and returns controlled test data.

### The files to create

Once Node.js and pnpm are installed, add test packages:

```bash
cd artifacts/florida-property-review
pnpm add -D vitest jsdom @testing-library/react @testing-library/user-event @testing-library/jest-dom msw
```

Then add these scripts to `package.json`:
```json
"test": "vitest --config vitest.config.ts",
"test:run": "vitest run --config vitest.config.ts"
```

**Files to create** (all details including full code in `current_progress.md`):

```
artifacts/florida-property-review/
├── vitest.config.ts                ← Vitest config (jsdom env, setup file, @ alias)
└── src/
    ├── test/
    │   ├── setup.ts                ← Imports jest-dom matchers, starts/stops MSW server
    │   └── utils.tsx               ← renderWithProviders() — wraps components in QueryClient + Router
    ├── mocks/
    │   ├── fixtures.ts             ← Mock data matching exact Django API response shapes
    │   ├── handlers.ts             ← MSW route handlers (fake Django endpoints)
    │   └── server.ts               ← Creates the MSW server from handlers
    └── (test files colocated with source):
        ├── lib/api.test.ts         ← Tests for formatDate, formatCategory, REGION_MAP
        ├── components/
        │   ├── MarketStrip.test.tsx
        │   └── Sidebar.test.tsx
        └── pages/
            ├── HomePage.test.tsx
            ├── NotableSalesPage.test.tsx
            └── ArticlePage.test.tsx
```

### How MSW works in tests

```
Test code calls renderWithProviders(<MarketStrip />)
    ↓
React renders MarketStrip, which calls useMarketMetrics()
    ↓
TanStack Query calls api.market.metrics()
    ↓
api.market.metrics() calls fetch('http://localhost/api/market/metrics/')
    ↓
MSW intercepts this fetch call (not hitting any real network)
    ↓
MSW handler returns HttpResponse.json(mockMetrics)
    ↓
TanStack Query stores the result, re-renders MarketStrip
    ↓
Test asserts: screen.getByText('Miami') → passes
```

### TDD approach going forward

Even though the implementations already exist, write tests as if you don't know the
implementation. Assert *behavior* (what the user sees), not *implementation* (which
function was called).

**Red → Green → Refactor:**
1. Write the test first. Run it. Watch it fail (red).
2. Write the minimum code to make it pass (green).
3. Clean up. Keep tests green.

For new features after the test infrastructure is in place:
- Write a failing test for the new behavior.
- Implement the feature until the test passes.
- Then refactor if needed.

---

## 9. Future Feature Roadmap

These are not planned for immediate implementation but represent logical next steps:

### Short term
- [ ] **Node.js install** — prerequisite for everything else (see Section 7)
- [ ] **Test infrastructure setup** — vitest.config, MSW, renderWithProviders (see Section 8)
- [ ] **Write all test files** — one per component and page (full code in `current_progress.md`)
- [ ] **Article FK on NotableSale** — link sale records to their full article so sale cards
  navigate to the article page (backend FK exists, needs wiring)

### Medium term
- [ ] **Search** — a search bar in the header that queries `GET /api/articles/?search=`
  (Django filter backend supports this with minimal backend change)
- [ ] **Pagination** — the articles and sales grids currently show whatever the API
  returns; for large datasets, add "Load more" or page number controls
- [ ] **Category filter tabs on HomePage** — same pattern as region tabs on NotableSalesPage,
  but filtering articles by category (NOTABLE_SALE, AGENT_WATCH, etc.)

### Long term
- [ ] **Production deployment** — gunicorn + nginx config, PostgreSQL, SSL
- [ ] **Image optimization** — replace Unsplash placeholder URLs with a CDN-backed
  image upload flow in Django admin
- [ ] **RSS feed** — Django view that serializes articles to RSS XML for readers
- [ ] **Social share** — wire the Facebook/Twitter/LinkedIn buttons on ArticlePage
  to actual share URLs (currently they are visual-only)

---

## 10. Commenting Convention

### The rule going forward

**All frontend files will be commented extensively** because this is also a learning
project. Every non-obvious pattern, every library API, and every architectural decision
will have an inline comment explaining the *why* and *what*.

### What to comment

**Always comment:**
- Hook calls — what data is being fetched, what the shape is
- State declarations — what the state represents, when it changes
- Conditional rendering — what condition is being checked and why
- Library-specific patterns — anything from framer-motion, wouter, React Query
- CSS class groups — what visual effect they produce
- Non-obvious JavaScript — array methods, optional chaining, nullish coalescing

**Never comment:**
- `return` statements (obvious)
- `import` statements (the name is self-explanatory)
- Closing braces `}` or JSX tags (add indentation instead)

### Example: How a component should look with comments

```tsx
// This hook fires GET /api/market/metrics/ and returns an array of MarketMetric objects.
// TanStack Query caches the result under the key ['market', 'metrics'] so other
// components can read the same data without firing a second network request.
// The `= []` default prevents "map of undefined" errors while the request is in flight.
const { data: metrics = [] } = useMarketMetrics();

return (
  // overflow-x-auto: allows horizontal scrolling on narrow screens (mobile)
  // no-scrollbar: hides the scrollbar visually (defined in index.css) but keeps scroll functional
  <div className="fpr-teal text-white w-full py-2 px-4 overflow-x-auto no-scrollbar">

    {/* min-w-max: prevents the flex container from wrapping — forces horizontal layout */}
    <div className="max-w-7xl mx-auto flex items-center justify-between min-w-max gap-6">

      {/* metrics.map() iterates over the array and returns one JSX element per item.
          The `key` prop must be unique — React uses it to efficiently update the DOM
          when the list changes. We use `index` here because metrics don't have unique IDs. */}
      {metrics.map((metric, index) => (
        <div key={index} className="flex flex-col gap-1 pr-6 border-r border-gray-600/50 last:border-0">

          {/* metric.city and metric.metric_label come from the Django MarketMetric model */}
          <div className="text-xs text-gray-300 uppercase tracking-wider font-semibold">
            {metric.city} {metric.metric_label}
          </div>

          <div className="flex items-baseline gap-2">
            <span className="font-bold text-lg">{metric.value_display}</span>

            {/* Ternary operator: condition ? valueIfTrue : valueIfFalse
                If is_positive is true, show green TrendingUp icon; otherwise coral TrendingDown */}
            <span className={`text-sm font-semibold flex items-center gap-0.5 ${
              metric.is_positive ? 'fpr-green' : 'fpr-coral'
            }`}>
              {metric.is_positive
                ? <TrendingUp className="w-3.5 h-3.5" />
                : <TrendingDown className="w-3.5 h-3.5" />}
              {metric.change_display}
            </span>
          </div>

        </div>
      ))}

    </div>
  </div>
);
```

### Commenting style for TypeScript types

```typescript
// Article represents the shape of one item in GET /api/articles/ (list endpoint).
// It does NOT include the full body text — use ArticleDetail for that.
export interface Article {
  slug: string;             // URL-safe identifier, e.g. "naples-bayfront-estate"
  headline: string;         // The article title shown in cards and the hero
  subheadline: string;      // Secondary text below the headline
  category: string;         // One of: NOTABLE_SALE | AGENT_WATCH | NEIGHBORHOOD_WATCH | DEVELOPMENT | MARKET_PULSE
  byline: string;           // Author attribution, e.g. "By Caroline Bennett"
  read_time_minutes: number; // Estimated read time for the "X min" badge
  hero_image_url: string;   // Full URL to the article's hero image
  published_date: string;   // ISO 8601 date string: "2024-05-12"
  is_featured: boolean;     // If true, this article appears in the homepage hero
}
```

---

*Last updated: 2026-06-25*
*Next action: Install Node.js (Section 7), then implement test infrastructure (Section 8)*
