# Day 1 — Schema + Content Foundation

One box at a time. Each box is small enough to finish without
context-switching. Check it, move on — don't loop back to "improve"
a box you already checked.

---

### Warm-up (5 min)

- [ ] `cd backend && uv run python manage.py runserver 8000` — confirm
      it still starts clean, no errors in the terminal
- [ ] Open `http://localhost:8000` in a browser, confirm it loads
- [ ] Stop the server (`Ctrl+C`) — don't leave it running while you read code

---

### articles/Article (15 min) — DONE

- [x] Open `backend/articles/models.py`
- [x] Read the `Article` model top to bottom, once, no editing
- [x] SEO/meta description field? — **Deferred**, not decided yet.
- [x] `hero_image_url` — **Stays a URL field.** Content is coming from
      an automated scrape/generate pipeline, so the pipeline supplies
      an image URL directly rather than you uploading through admin.
- [x] **New context surfaced mid-review**: this site is meant to be
      largely self-populating — an external API will scrape sources
      and generate articles, with you as editor. That changed the
      real question from "is anything missing" to "does the schema
      support a review workflow." It does now:
      - Added `Article.status` (`DRAFT` / `PENDING_REVIEW` /
        `PUBLISHED`) replacing the old flat `is_published` boolean.
        Default stays `PUBLISHED` (matches old behavior for
        hand-written/admin articles); the automation pipeline should
        set `PENDING_REVIEW` explicitly so nothing goes live without
        your approval.
      - Added `source_url` + `source_name` for attribution on
        scraped/generated articles.
      - Migration applied, fixtures updated, all 77 tests still pass,
        live site re-verified. Committed as `0113b5a`.

### sales/NotableSale (15 min) — DONE

- [x] Open `backend/sales/models.py`
- [x] Read the `NotableSale` model top to bottom, once, no editing
- [x] SEO/meta field needed? — Deferred, same as Article.
- [x] `hero_image_url` — stays a URL field, matching Article.
- [x] **Bigger finding**: unlike `Article`, this model had **no publish
      gate at all** — every row in the DB was always shown on the site,
      with no draft/review concept whatsoever. That's a bigger risk
      than Article's old boolean, once sale data starts arriving from
      a scrape/generate pipeline (bad price/address data would go
      straight to production).
      - Added `NotableSale.status` (`DRAFT`/`PENDING_REVIEW`/`PUBLISHED`),
        default `PUBLISHED` to preserve current always-shown behavior
        for hand-entered sales.
      - Added `source_url`/`source_name` for attribution.
      - Gated every query that reads `NotableSale` (list API, featured,
        top-closings, the sales grid, the homepage closings widget) to
        `status=PUBLISHED`.
      - Migration applied, fixtures reloaded, all 77 tests pass, live
        site re-verified.

### market/* (10 min) — DONE

- [x] Open `backend/market/models.py`
- [x] Read `MarketMetric`, `Agent`, `NeighborhoodIntel`,
      `FastestGrowingMarket` — four short models, back to back
- [x] Missing field? — **Decision: skip the `status` workflow on
      these.** They're short numeric widget values, not long-form
      content — a wrong ticker number is low-stakes and trivially
      fixable, unlike a fabricated article or sale. Added
      `source_url`/`source_name` to all four for attribution only.
      Migration applied, tests pass, live site re-verified.
- [x] **Open gap, not yet fixed**: `FastestGrowingMarket.rank` is
      globally unique with no period field, unlike `Agent`
      (`unique_together = [rank, period_month, period_year]`).
      Refreshing it periodically will hit a unique-constraint error.
      Needs a decision later: add period fields to match `Agent`, or
      delete-and-replace on refresh.

### subscribers/Subscriber (5 min)

- [ ] Open `backend/subscribers/models.py`
- [ ] Read it — it's short
- [ ] One question: **anything missing?** (e.g. name field, source
      tracking) Answer "none" if genuinely nothing:
      - Answer:

---

### Break (take one — you've read every model in the app)

---

### Decide: real content vs. placeholder (10 min, decision only)

- [ ] Pick ONE of these three, nothing in between:
      - [ ] **(A)** Keep the 6 mock articles / 8 mock sales as-is for
            now, come back to real content later
      - [ ] **(B)** Write 2–3 real articles today to replace the mock
            ones, leave the rest as mock
      - [ ] **(C)** Full content pass — replace all mock fixture data
            with real content before moving to Day 2
- [ ] Write your choice here so Day 2 doesn't have to re-decide this:
      - Choice:

---

### Lock in schema changes (only if you found gaps above)

- [ ] If every "Answer:" above was "none" / "no changes" — **skip this
      whole section**, you're done for Day 1
- [ ] If you found ONE gap — pick the single most important one, write
      it as one sentence:
      - Change:
- [ ] Make that one model change
- [ ] `uv run python manage.py makemigrations`
- [ ] `uv run python manage.py migrate`
- [ ] `uv run python manage.py test` — confirm still 77/77 (or however
      many exist now) passing
- [ ] Stop here. Do not start a second schema change today — that's
      tomorrow's problem if it comes up.

---

## Done-for-today checkpoint

- [ ] All four models reviewed
- [ ] Content-strategy choice written down (A/B/C above)
- [ ] Zero or one schema change made (not more)
- [ ] Tests passing
- [ ] Close the laptop / stop — Day 2 is production settings, not today
