# Session Plan — 2026-07-11

Everything I (Claude) intend to do, in order, with the exact commands.
Nothing below runs until you approve it. Steps marked **[needs your OK]**
are the ones that change things; everything else is read-only.

---

## Where things stand right now (verified, not assumed)

- The project pivoted from a React SPA to a **Django server-rendered site**.
  The Django build (BUILD_PLAN.md Steps 1–8) is complete on disk.
- The Django dev server is **currently running** at http://localhost:8000
  (I started it earlier this session; the database is seeded with
  6 articles, 8 sales, 5 metrics, 3 agents).
- The test suite: **77 tests, 76 pass, 1 fails.**
- **None of this work has ever been committed to git.** The entire
  `backend/` folder, all the planning docs, and the React changes exist
  only in the working directory. This is the biggest risk in the project.
- The `.gitignore` is from the old React/Replit era and does not exclude
  Python artifacts (database file, virtualenv, secrets, the 100MB
  Tailwind binary).

---

## Step 1 — Commit the current working state  **[needs your OK]**

**Why first:** every other step modifies files. Snapshot before changing.

**What gets committed:** everything — all source code, templates, tests,
fixtures, and the five .md docs — exactly as it sits on disk right now.

**What gets left out (staged around, no files touched or deleted):**

| File | Why it stays out |
|------|------------------|
| `backend/db.sqlite3` | Your local database. Rebuildable via `migrate` + `loaddata`. Binary files pollute git history. |
| `backend/tailwindcss` | 100MB compiler binary, re-downloadable with one `curl` command (documented in BUILD_PLAN.md). |
| `backend/.venv/` | Installed Python packages. Rebuildable with `uv sync`. Machine-specific. |
| `backend/.env` | Secrets (if the file exists). Never belongs in git. |
| `__pycache__/` folders | Python's automatic bytecode cache. Regenerated on every run. |

**The commands:**

```bash
git add -A -- ':!backend/.venv' ':!backend/db.sqlite3' ':!backend/tailwindcss' ':!backend/.env' ':!*__pycache__*'
git status --short        # you review this list before anything is committed
git commit -m "Add Django template site, planning docs, and React API wiring"
```

**Done when:** `git log` shows the new commit and `git status` shows only
the deliberately-excluded files as untracked.

---

## Step 2 — Update .gitignore  **[needs your OK]**

**Why second (not first):** it edits a file, so it happens after the
snapshot. Its job is to make the excluded files from Step 1 permanently
invisible to git, so no future commit picks them up by accident.

**The change:** append these lines to the existing `.gitignore`
(nothing removed, nothing else touched):

```gitignore
# Python / Django
__pycache__/
*.pyc
.venv/
backend/db.sqlite3
backend/.env
backend/tailwindcss
backend/staticfiles/
```

Then commit that one-file change:

```bash
git add .gitignore
git commit -m "Ignore Python/Django artifacts and secrets"
```

**Done when:** `git status` is completely clean — no stray untracked files.

---

## Step 3 — Fix the one failing test (TDD)  **[needs your OK]**

**The failure:** `sales/tests/test_template_views.py` →
`test_region_filter_excludes_other_regions`.

**What it does:** loads `/notable-sales/?region=ORLANDO` and asserts the
South Florida sale "Bayfront Estate" appears **nowhere on the page**.

**Why it fails:** the region filter on the sales grid works correctly
(the grid shows "No sales found for this region."). But the
**Top Luxury Closings sidebar** is designed to always show the biggest
closings statewide, regardless of the filter — both plan docs specify
this. So "Bayfront Estate" legitimately appears in the sidebar, and the
page-wide assertion trips.

**The verdict:** the implementation matches the documented intent; the
**test's assertion is scoped too broadly**. Under TDD the test is the
spec — and this spec was written imprecisely. The fix is to the test,
not the code.

**The fix:** change the assertion so it checks the sale is absent from
the *sales grid* — the simplest robust way is to assert the empty-state
message is shown and the sale title doesn't appear *before* the sidebar
section, or split the check using the grid's surrounding markup. I will
show you the exact edit before making it.

**Verify:**

```bash
cd backend
uv run python manage.py test        # expect: 77 tests, 0 failures
```

Then commit:

```bash
git commit -am "Scope region-filter test to the sales grid"
```

**Done when:** full suite green, committed.

---

## Step 4 — Smoke-test the running site (read-only)

The server is already up. This is BUILD_PLAN.md Step 9's checklist.
I check each page returns HTTP 200 and contains real content:

```bash
curl -s http://localhost:8000/                                   # homepage: featured headline present?
curl -s http://localhost:8000/articles/<some-slug>/              # article detail renders?
curl -s http://localhost:8000/notable-sales/                     # sales grid renders?
curl -s "http://localhost:8000/notable-sales/?region=ORLANDO"    # filter works?
curl -s http://localhost:8000/static/css/output.css              # styles load?
```

The newsletter form POST I'll test with a throwaway email:

```bash
# get a CSRF token from the page, then:
curl -s -X POST http://localhost:8000/subscribe/ -d "email=smoketest@example.com&next=/" ...
```

**Better option:** you open http://localhost:8000 in your browser and
click through yourself — you'll actually *see* the site, which curl
can't give you. I recommend we do both.

**Done when:** all 5 pages verified, newsletter subscribe works.

---

## Step 5 — Rewrite CLAUDE.md  **[needs your OK]**

**Why:** CLAUDE.md still describes the abandoned React architecture.
It's the first thing loaded in every future session — if it's wrong,
every future session starts confused (like this one did).

**What changes:**
- Architecture: Django server-rendered templates, not React SPA
- Dev workflow: `runserver` + Tailwind standalone binary, no Node/pnpm
- The template/view/URL structure that actually exists
- React app marked as archived in `artifacts/` (kept, not served)
- Keep: the TDD section, the uv workflow, the model/app documentation
  (all still accurate)

Then commit it, and delete this SESSION_PLAN.md file (its job is done —
the task list and git history carry the record forward).

---

## Step 6 — Housekeeping (last, quick)

- Stop the background dev server I started (or leave it running if
  you're actively browsing the site — your call).
- Update my persistent memory: the project is now Django-templates-first,
  so future sessions don't reach for the React/Vitest plan by mistake.

---

## Explicitly NOT in this plan

- No changes to any view, model, template, or URL — the app works.
- No touching the React app in `artifacts/` — it stays archived as-is.
- No new features (search, pagination, HTMX filters) — those are
  follow-ups to discuss after the baseline is committed and green.
- No pushing to any remote — commits stay local unless you say otherwise.
