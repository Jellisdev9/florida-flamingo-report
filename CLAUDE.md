# Florida Property Review

Editorial/business-news style real estate publication focused on Florida real estate.
Covers notable sales, agent moves, market trends, neighborhoods, luxury closings, and development news.

## Architecture

**One server. No Node. No React to run the site.** Django renders HTML server-side.

- **Backend** — Django + Django REST Framework (`backend/`)
- **Templates** — Django templates (`backend/templates/`), styled with Tailwind CSS (standalone CLI binary, no Node build step)
- **Database** — PostgreSQL (production) / SQLite (development)
- The DRF `/api/` endpoints are kept alongside the template views (useful for mobile/RSS/future use) but the site itself does not consume them — views query the ORM directly and pass context to templates.
- `artifacts/florida-property-review/` is the **original React SPA — archived, not served**. The project pivoted from React+API to Django server-rendered templates; this directory is kept for reference only.

## Tech Stack

### Backend
- Django 5.x + Django REST Framework
- django-cors-headers, django-filter
- PostgreSQL (prod) / SQLite (dev)
- python-dotenv
- Tailwind CSS via the standalone CLI binary (`backend/tailwindcss`, gitignored — re-download per BUILD_PLAN.md Step 3)

## Project Structure

```
Florida-Front-End/
├── CLAUDE.md
├── BUILD_PLAN.md                   # order-of-operations for the Django rebuild
├── DJANGO_TEMPLATES_PLAN.md        # full template/view code reference
├── backend/                        # Django project root
│   ├── manage.py
│   ├── pyproject.toml              # uv-managed deps
│   ├── .env.example
│   ├── fixtures/                   # seed data (JSON)
│   ├── tailwindcss                 # standalone Tailwind binary (gitignored)
│   ├── static/css/{input,output}.css
│   ├── templates/
│   │   ├── base.html               # master template — header, market strip, footer
│   │   ├── home.html
│   │   ├── article_detail.html
│   │   ├── notable_sales.html
│   │   └── partials/
│   │       ├── top_markets_sidebar.html
│   │       └── top_agents_sidebar.html
│   ├── backend/                    # Django config package
│   │   ├── settings/
│   │   │   ├── base.py             # shared settings
│   │   │   ├── development.py      # SQLite, DEBUG=True, CORS localhost
│   │   │   └── production.py       # PostgreSQL, DEBUG=False
│   │   ├── urls.py                 # root URL config (template pages + /api/)
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── articles/                   # article content app
│   ├── sales/                      # notable sales app
│   ├── market/                     # market metrics, agents, neighborhoods app
│   └── subscribers/                # newsletter signups app
└── artifacts/
    └── florida-property-review/    # ARCHIVED React SPA — not served, kept for reference
```

## Django Apps

### articles/
Manages editorial article content.
- **Model:** `Article` — slug, title, headline, subheadline, category, body, byline, author_avatar_url, read_time_minutes, hero_image_url, published_date, is_featured, is_published
- **Categories:** NOTABLE_SALE, AGENT_WATCH, NEIGHBORHOOD_WATCH, DEVELOPMENT, MARKET_PULSE

### sales/
Manages notable property sales.
- **Model:** `NotableSale` — slug, title, price, location, city, region, property_type, close_date, hero_image_url, is_featured, article (FK), brokerage, beds, baths, sq_ft
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
- Handles duplicate email gracefully (redirects with no error instead of erroring)

## Pages (template-rendered)

| URL | Template | View | Notes |
|-----|----------|------|-------|
| `/` | `home.html` | `articles.views.home_view` | featured article hero, article cards, sidebars |
| `/articles/<slug>/` | `article_detail.html` | `articles.views.article_detail_view` | 404 on unknown slug |
| `/notable-sales/` | `notable_sales.html` | `sales.views.notable_sales_view` | region filter via `?region=`, statewide "Top Luxury Closings" sidebar ignores the filter by design |
| `/subscribe/` | — (redirect only) | `subscribers.views.subscribe_view` | POST-only, redirects back to `next` |

## API Endpoints (kept, not used by the site itself)

All endpoints are prefixed with `/api/`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/articles/ | List articles (`?category=`) |
| GET | /api/articles/featured/ | Featured article |
| GET | /api/articles/`<slug>`/ | Article detail |
| GET | /api/sales/ | List notable sales (`?region=`) |
| GET | /api/sales/featured/ | Featured sale |
| GET | /api/sales/top-closings/ | Top 5 closings by price |
| GET | /api/market/metrics/ | 5-tile header strip data |
| GET | /api/market/neighborhoods/ | Neighborhood intel cards |
| GET | /api/market/fastest-growing/ | Fastest growing markets |
| GET | /api/agents/top/ | Top agents this month |
| POST | /api/subscribers/ | Subscribe to newsletter |

## Development Workflow

Uses [uv](https://docs.astral.sh/uv/) for Python dependency management. Dependencies live in `backend/pyproject.toml`. No Node/pnpm needed to run the site.

```bash
# Backend setup (run once)
cd backend
cp .env.example .env
uv sync                              # creates .venv and installs all deps
uv run python manage.py migrate
uv run python manage.py createsuperuser

# Seed mock data (after migrations)
uv run python manage.py loaddata fixtures/initial_data.json

# Tailwind CSS — standalone binary, no Node required (see BUILD_PLAN.md Step 3)
curl -sLO https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-linux-x64
chmod +x tailwindcss-linux-x64
mv tailwindcss-linux-x64 tailwindcss
./tailwindcss -i static/css/input.css -o static/css/output.css
# add --watch during active development to recompile on template changes

# Run
uv run python manage.py runserver 8000

# Run tests
uv run python manage.py test         # all apps
uv run python manage.py test articles # single app

# Add a dependency
uv add <package>
```

`manage.py` defaults `DJANGO_SETTINGS_MODULE` to `backend.settings.development`, and `development.py` hardcodes SQLite with no required secrets — the server runs even without a `.env` file present, though one should still be created for `SECRET_KEY` and other overrides.

## Environment Variables

See `backend/.env.example`. Key variables:
- `DJANGO_SETTINGS_MODULE` — `backend.settings.development` locally
- `SECRET_KEY` — required in production
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` — production PostgreSQL
- `CORS_ALLOWED_ORIGINS` — comma-separated list of allowed frontend origins (relevant only for `/api/` consumers)

## Testing — TDD Red/Green

This project follows strict TDD. Every feature is written test-first: write a failing test (red), write the minimum code to make it pass (green), then refactor.

```bash
cd backend
uv run python manage.py test          # run all tests
uv run python manage.py test articles # run one app
```

Test file location mirrors the app structure:

```
backend/
├── articles/tests/{test_models,test_views,test_template_views}.py
├── sales/tests/{test_models,test_views,test_template_views}.py
├── market/tests/{test_models,test_views}.py
└── subscribers/tests/{test_models,test_views,test_template_views}.py
```

Use Django's built-in `TestCase` + DRF's `APITestCase`. `test_template_views.py` files use `self.client.get()`/`self.assertTemplateUsed`/`self.assertContains` for page-level tests, and `response.context[...]` when an assertion needs to target a specific context variable (e.g. the sales grid queryset) rather than scraping rendered HTML — this matters when a page has both a filtered section (the grid) and an unfiltered one (a statewide sidebar widget).

Cycle for every endpoint, model, or view change:
1. **Red** — write the test, assert the exact response shape/status/context, run it and watch it fail
2. **Green** — write the minimum model/view code to pass
3. **Refactor** — clean up, keep tests green

### What to test

| Layer | Test focus |
|-------|-----------|
| Models | field validation, `__str__`, unique constraints, ordering, computed properties (e.g. `price_display`) |
| Views (template) | status codes, template used, context contents, rendered content, filter params (`?region=`, `?category=`), edge cases (404, duplicate subscriber) |
| Views (API) | status codes, response shape, filter params, edge cases |

### What not to test

- Django internals (ORM, admin)
- Third-party library behavior
- Trivial getters with no logic

## Next Steps

- [ ] Production: add gunicorn + nginx config, PostgreSQL setup
- [ ] Decide the long-term fate of `artifacts/florida-property-review/` (archived React SPA) — keep as reference or remove
