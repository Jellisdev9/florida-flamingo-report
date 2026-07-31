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

### articles/Article (15 min)

- [ ] Open `backend/articles/models.py`
- [ ] Read the `Article` model top to bottom, once, no editing
- [ ] Answer one question only: **does a real article need a meta
      description / SEO field that isn't there?** (yes/no — write it
      down here, don't fix it yet)
      - Answer:
- [ ] Answer one question only: **`hero_image_url` — stay as a plain
      URL field, or switch to uploaded images later?** (pick one, write
      it down, don't implement)
      - Answer:

### sales/NotableSale (15 min)

- [ ] Open `backend/sales/models.py`
- [ ] Read the `NotableSale` model top to bottom, once, no editing
- [ ] Same two questions as above, applied to this model:
      - SEO/meta field needed? Answer:
      - `hero_image_url` decision (should match your Article answer): Answer:

### market/* (10 min)

- [ ] Open `backend/market/models.py`
- [ ] Read `MarketMetric`, `Agent`, `NeighborhoodIntel`,
      `FastestGrowingMarket` — four short models, back to back
- [ ] One question: **is there any field you keep wanting to type into
      Django admin that doesn't exist yet?** Write it down if so,
      otherwise write "none":
      - Answer:

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
