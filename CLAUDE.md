# Florida Property Review

Editorial/business-news style real estate publication focused on Florida real estate.
Covers notable sales, agent moves, market trends, neighborhoods, luxury closings, and development news.

## Architecture

**Frontend** — React + Vite + TypeScript SPA (`artifacts/florida-property-review/`)
**Backend** — Django + Django REST Framework (`backend/`)
**Database** — PostgreSQL (production) / SQLite (development)

The React frontend fetches all data from Django API endpoints. Django Admin is the CMS for managing content.

## Tech Stack

### Frontend
- React 18 + TypeScript
- Vite (build tool)
- Tailwind CSS + shadcn/ui components
- wouter (client-side routing)
- @tanstack/react-query (data fetching)
- framer-motion (animations)

### Backend
- Django 5.x + Django REST Framework
- django-cors-headers
- django-filter
- PostgreSQL (prod) / SQLite (dev)
- python-dotenv

## Project Structure

```
Florida-Front-End/
├── CLAUDE.md
├── backend/                        # Django project root
│   ├── manage.py
│   ├── requirements.txt
│   ├── .env.example
│   ├── fixtures/                   # Seed data (JSON)
│   ├── backend/                    # Django config package
│   │   ├── settings/
│   │   │   ├── base.py             # Shared settings
│   │   │   ├── development.py      # SQLite, DEBUG=True, CORS localhost
│   │   │   └── production.py       # PostgreSQL, DEBUG=False
│   │   ├── urls.py                 # Root URL config
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── articles/                   # Article content app
│   ├── sales/                      # Notable sales app
│   ├── market/                     # Market metrics, agents, neighborhoods app
│   └── subscribers/                # Newsletter signups app
└── artifacts/
    └── florida-property-review/    # React SPA (existing, unchanged)
        └── src/
            ├── pages/              # HomePage, ArticlePage, NotableSalesPage
            └── components/         # Header, Sidebar, ArticleCard, MarketStrip
```

## Django Apps

### articles/
Manages editorial article content.
- **Model:** `Article` — slug, headline, subheadline, category, body, byline, hero_image_url, published_date, is_featured

- **Categories:** NOTABLE_SALE, AGENT_WATCH, NEIGHBORHOOD_WATCH, DEVELOPMENT, MARKET_PULSE

### sales/
Manages notable property sales.
- **Model:** `NotableSale` — slug, title, price, location, city, region, property_type, close_date, brokerage, beds, baths, sq_ft, is_featured, article (FK)

- **Regions:** SOUTH_FLORIDA, TAMPA_BAY, ORLANDO, JACKSONVILLE, PANHANDLE
- **Types:** WATERFRONT_ESTATE, CONDO_PENTHOUSE, CONDO_RESIDENCE, COMMERCIAL, SINGLE_FAMILY

### market/
Manages all market data widgets shown in the header strip and sidebars.
- **Model:** `MarketMetric` — powers the 5-tile header strip (city, value_display, change_display, is_positive)
- **Model:** `Agent` — top agents leaderboard (name, location, volume_display, rank, period_month/year)
- **Model:** `NeighborhoodIntel` — neighborhood watch cards (neighborhood, city, description, tag: HOT/RISING/COOLING)
- **Model:** `FastestGrowingMarket` — fastest growing markets sidebar (location, change_display, rank)

### subscribers/
Manages newsletter subscriptions.
- **Model:** `Subscriber` — email, subscribed_at, is_active
- Handles duplicate email gracefully (returns 200 instead of 400)

## API Endpoints

All endpoints are prefixed with `/api/`

| Method | Endpoint | Description | React Consumer |
|--------|----------|-------------|----------------|
| GET | /api/articles/ | List articles (`?category=`) | HomePage cards |
| GET | /api/articles/featured/ | Featured homepage hero article | HomePage hero |
| GET | /api/articles/`<slug>`/ | Article detail | ArticlePage |
| GET | /api/sales/ | List notable sales (`?region=`) | NotableSalesPage grid |
| GET | /api/sales/featured/ | Featured sale hero | NotableSalesPage hero |
| GET | /api/sales/top-closings/ | Top 5 closings by price | Sidebar widget |
| GET | /api/market/metrics/ | 5-tile header strip data | MarketStrip.tsx |
| GET | /api/market/neighborhoods/ | Neighborhood intel cards | HomePage sidebar |
| GET | /api/market/fastest-growing/ | Fastest growing markets | NotableSalesPage sidebar |
| GET | /api/agents/top/ | Top agents this month | Sidebar widget |
| POST | /api/subscribers/ | Subscribe to newsletter | Newsletter forms |

## Development Workflow

Uses [uv](https://docs.astral.sh/uv/) for Python dependency management. Dependencies live in `backend/pyproject.toml`.

```bash
# Backend setup (run once)
cd backend
cp .env.example .env
uv sync                              # creates .venv and installs all deps
uv run python manage.py migrate
uv run python manage.py createsuperuser

# Seed mock data (after migrations)
uv run python manage.py loaddata fixtures/initial_data.json

# Run backend
uv run python manage.py runserver 8000

# Run tests
uv run python manage.py test         # all apps
uv run python manage.py test articles # single app

# Add a dependency
uv add <package>

# Frontend (separate terminal)
cd artifacts/florida-property-review
pnpm install
pnpm dev  # runs on :5173, proxy /api → :8000
```

## Environment Variables

See `backend/.env.example`. Key variables:
- `DJANGO_SETTINGS_MODULE` — `backend.settings.development` locally
- `SECRET_KEY` — required in production
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` — production PostgreSQL
- `CORS_ALLOWED_ORIGINS` — comma-separated list of allowed frontend origins

## React → Django Migration Plan

React components currently use hardcoded mock data. Wire them up in this order:

1. `MarketStrip.tsx` → `GET /api/market/metrics/`
2. `HomePage.tsx` article cards → `GET /api/articles/?category=`
3. `NotableSalesPage.tsx` grid → `GET /api/sales/?region=`
4. `ArticlePage.tsx` → `GET /api/articles/<slug>/`
5. All sidebar widgets → their respective endpoints

Pattern for each: replace hardcoded array with `useQuery()` from @tanstack/react-query.

## Testing — TDD Red/Green

This project follows strict TDD. Every feature is written test-first: write a failing test (red), write the minimum code to make it pass (green), then refactor.

### Django (backend)

Use Django's built-in `TestCase` + DRF's `APITestCase`.

```bash
cd backend
python manage.py test          # run all tests
python manage.py test articles  # run one app
```

Test file location mirrors the app structure:

```
backend/
├── articles/
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_models.py      # model validation, str(), constraints
│   │   └── test_views.py       # API endpoint responses, filters, status codes
├── sales/
│   └── tests/
│       ├── test_models.py
│       └── test_views.py
├── market/
│   └── tests/
│       ├── test_models.py
│       └── test_views.py
└── subscribers/
    └── tests/
        ├── test_models.py
        └── test_views.py
```

Cycle for every endpoint or model change:
1. **Red** — write the test, assert the exact response shape/status, run it and watch it fail
2. **Green** — write the minimum model/serializer/view code to pass
3. **Refactor** — clean up, keep tests green

### React (frontend)

Use Vitest + React Testing Library.

```bash
cd artifacts/florida-property-review
pnpm test          # watch mode
pnpm test --run    # single run (CI)
```

Test file location: colocated with the component (`Component.test.tsx`).

Cycle for every component wired to a real API:
1. **Red** — mock the API response with MSW, assert the rendered output fails
2. **Green** — implement the `useQuery` hook + render logic
3. **Refactor** — clean up component, keep tests green

### What to test

| Layer | Test focus |
|-------|-----------|
| Models | field validation, `__str__`, unique constraints, ordering |
| Serializers | field output, computed fields (`price_display`), read-only enforcement |
| API views | status codes, response shape, filter params (`?region=`, `?category=`), edge cases (404, duplicate subscriber) |
| React components | renders with mocked API data, loading state, empty state, filter tab interaction |

### What not to test

- Django internals (ORM, admin)
- Third-party library behavior
- Trivial getters with no logic

## Next Steps

- [ ] Seed `fixtures/initial_data.json` with mock data from React components
- [ ] Wire React components to Django API (replace hardcoded data)
- [ ] Add Vite proxy config to forward `/api` → `http://localhost:8000`
- [ ] Add `article` FK to `NotableSale` for notable sale → article linking
- [ ] Production: add gunicorn + nginx config, PostgreSQL setup
