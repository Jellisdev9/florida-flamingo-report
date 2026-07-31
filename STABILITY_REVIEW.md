# Stability & Production-Readiness Review — 2026-07-31

Full review of the current state (docs + code) to set direction for the next
3 days. Nothing in this doc has been acted on yet — it's findings only.

---

## Where things stand

- **Architecture**: Django server-rendered templates. React SPA and its
  planning doc removed. `BUILD_PLAN.md` + `DJANGO_TEMPLATES_PLAN.md`
  document the build that's already done; `CLAUDE.md` is accurate as of
  the last rewrite.
- **`replit.md`**: unfilled boilerplate for a totally different stack
  (Express/Postgres/Drizzle) — leftover from the original Replit
  scaffold, not describing this project at all. Candidate for deletion.
- **Pages working**: `/`, `/articles/<slug>/`, `/notable-sales/`
  (+ region filter), `/subscribe/` (POST). All verified returning 200
  with real rendered content.
- **Tests**: 77/77 passing. Coverage: articles (3 test files), sales (3),
  market (2), subscribers (3).
- **Git**: clean, pushed to `origin` (GitHub, private). Local
  `gitsafe-backup` (dead Replit-internal remote) removed.
- **Fixture data**: `fixtures/initial_data.json` — 6 articles, 8 sales,
  5 market metrics, 3 agents, 2 neighborhoods, 5 fastest-growing markets.
  This is mock/placeholder content, not real editorial content.

## Findings by layer

### Schema / models — solid, no urgent gaps
- All 4 apps (`articles`, `sales`, `market`, `subscribers`) have `Meta.ordering`
  and `__str__` defined. No missing constraints found.
- `hero_image_url` on `Article` and `NotableSale` is a plain `URLField`
  pointing at hotlinked Unsplash placeholder images — fine for mock data,
  but real content will need either real image URLs or an `ImageField`
  + media storage decision (local disk vs. S3/R2) before going live.
- Only one migration per app (`0001_initial`) — expected at this stage,
  but worth locking the schema down *before* generating a lot of real
  content, since schema changes against live data are more expensive
  than changes now.

### Admin / CMS — complete
All 4 apps have registered `ModelAdmin`s with sensible `list_display`,
`list_filter`, `search_fields`, and `prepopulated_fields` for slugs.
This is usable as a real CMS today.

### Tests — passing, decent coverage, one design note
- 77/77 green. Model + template-view tests exist for the pages that
  matter.
- The region-filter test fix earlier this session (checking
  `context['sales']` instead of scraping HTML) is the right pattern —
  worth using consistently for any future filtered-list assertions.

### Settings / security — biggest gap area for "production ready"
`backend/settings/production.py` already has `DEBUG=False`,
`SECRET_KEY` from env, Postgres config from env, HSTS, SSL redirect,
and secure cookies. That's a good baseline. Missing:

- **`CSRF_TRUSTED_ORIGINS`** — not set. Needed once this sits behind a
  real domain over HTTPS, or the subscribe form's CSRF check will
  reject legitimate submissions.
- **`SECURE_PROXY_SSL_HEADER`** — not set. If nginx terminates TLS and
  proxies plain HTTP to gunicorn (the planned VPS setup), Django won't
  know the original request was HTTPS without this, which breaks
  `SECURE_SSL_REDIRECT`/secure-cookie logic and can cause redirect loops.
- **No production `LOGGING` config** — `development.py` has one,
  `production.py` doesn't. Errors would only go to gunicorn's stdout.
- **`ALLOWED_HOSTS`** defaults to `[""]` if the env var is unset
  (`"".split(",")` → `['']`) — works by accident right now but should
  fail loudly instead if misconfigured.
- No `.env` exists yet even for local dev (only `.env.example`) — not
  urgent since `development.py` needs no secrets, but will be needed
  before running under `production.py` settings at all, even locally.

### Deployment — nothing built yet (expected, per today's plan)
- `gunicorn` and `psycopg2-binary` are already declared in
  `pyproject.toml`, but there's no gunicorn config, systemd unit, or
  nginx config in the repo yet.
- No Postgres instance exists yet — dev is SQLite only.
- Per the direction agreed today: **defer VPS/nginx/domain work**. Local
  first, until the product itself is solid.

## What "for now, host locally" concretely implies

Two things can be done entirely on this machine, before any VPS exists:

1. Run the app under **gunicorn instead of `runserver`** locally, to
   catch anything that only breaks under a production-style WSGI server
   (e.g. static file serving differences, `DEBUG=False` error pages).
2. Stand up a **local Postgres** instance and migrate to it, to catch
   any SQLite-vs-Postgres behavior differences (there are a few classic
   ones: case-sensitivity, `JSONField` behavior, migration edge cases)
   before it matters on a real server.

Neither requires a VPS, domain, or nginx.

## Proposed 3-day plan (draft — not started)

**Day 1 — Schema + content foundation**
- Review each model against what real content will need (image
  handling decision for `hero_image_url` fields, any missing fields
  for SEO/meta description, etc.) and lock in schema changes now,
  before generating more content.
- Decide real-vs-placeholder content strategy going forward.

**Day 2 — Production settings + local Postgres**
- Fix the settings gaps above (`CSRF_TRUSTED_ORIGINS`,
  `SECURE_PROXY_SSL_HEADER`, prod `LOGGING`, fail-loud `ALLOWED_HOSTS`).
- Install Postgres locally, migrate the schema, load fixtures, and run
  the full test suite + manual smoke test against it instead of SQLite.
- Create a real `backend/.env` (not committed) for local prod-style runs.

**Day 3 — Run under gunicorn locally + cleanup**
- Run the site locally via `gunicorn` (not `runserver`) against local
  Postgres, with `DJANGO_SETTINGS_MODULE=backend.settings.production`,
  to validate the actual production code path end-to-end.
- Delete `replit.md` (stale, describes a different stack) or replace it
  with an accurate project summary.
- Reassess: only after this is solid does a VPS conversation make sense.

---

This is a draft for discussion, not a commitment — happy to reorder or
cut anything before we start Day 1.
