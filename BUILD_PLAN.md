# Build Plan — Django Templates

One server. No Node. No React. Just Django rendering HTML.

**Done when:** `uv run python manage.py runserver 8000` shows a live site at localhost:8000.

---

## The pages we're building

| URL | Template | View |
|-----|----------|------|
| `/` | `home.html` | `articles/views.py` |
| `/articles/<slug>/` | `article_detail.html` | `articles/views.py` |
| `/notable-sales/` | `notable_sales.html` | `sales/views.py` |
| `/subscribe/` | (redirect only) | `subscribers/views.py` |

---

## Step 1 — Settings

No test needed. Just config changes.

- [ ] In `backend/backend/settings/base.py`:
  - Change `"DIRS": []` → `"DIRS": [BASE_DIR / "templates"]`
  - Add `STATICFILES_DIRS = [BASE_DIR / "static"]` below `STATIC_ROOT`

**Done when:** Django starts without errors.

---

## Step 2 — Add `price_display` to the NotableSale model

The serializer computes this today. Templates need it on the model itself.

### RED — write the test first

In `backend/sales/tests/test_models.py`, add:

```python
def test_price_display(self):
    sale = NotableSale(price=4750000)
    self.assertEqual(sale.price_display, "$4,750,000")
```

Run it — watch it fail:
```bash
cd backend
uv run python manage.py test sales.tests.test_models
```

### GREEN — add the property

In `backend/sales/models.py`, add inside the `NotableSale` class:

```python
@property
def price_display(self):
    return f"${self.price:,.0f}"
```

Run tests again — should pass.

**No migration needed** — this is a Python property, not a database column.

---

## Step 3 — Tailwind CSS

No test needed. Just tooling.

```bash
cd backend

# Download the standalone binary (no Node required)
curl -sLO https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-linux-x64
chmod +x tailwindcss-linux-x64
mv tailwindcss-linux-x64 tailwindcss
```

Create `backend/tailwind.config.js`:
```js
module.exports = {
  content: ["./templates/**/*.html"],
  theme: {
    extend: {
      fontFamily: {
        serif: ['"Playfair Display"', 'Georgia', 'serif'],
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
```

Create `backend/static/css/input.css`:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

.fpr-navy      { background-color: #0d1b2a; }
.fpr-teal      { background-color: #0f4c5c; }
.fpr-gold      { color: #d4a817; }
.fpr-gold-bg   { background-color: #d4a817; }
.fpr-coral     { color: #e05c4b; }
.fpr-coral-bg  { background-color: #e05c4b; }
.fpr-green     { color: #2e7d32; }
```

Compile:
```bash
./tailwindcss -i static/css/input.css -o static/css/output.css
```

**Done when:** `static/css/output.css` exists and is not empty.

---

## Step 4 — base.html

The master template. Every page extends it. Contains header, market strip, footer.

### RED

Create `backend/articles/tests/test_template_views.py`:

```python
from django.test import TestCase
from django.urls import reverse
from articles.models import Article
import datetime

class BaseTemplateTest(TestCase):
    def test_home_uses_base_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'base.html')
```

Run — fails because `home` URL doesn't exist yet.

### GREEN

- [ ] Create `backend/templates/` directory
- [ ] Create `backend/templates/base.html` (see DJANGO_TEMPLATES_PLAN.md Step 3)
- [ ] Add `home_view` to `articles/views.py` (stub — just renders `home.html`)
- [ ] Add `home.html` stub that extends `base.html`
- [ ] Wire `path("", home_view, name="home")` in `backend/backend/urls.py`

Run test — passes.

---

## Step 5 — Home page

### RED

Add to `backend/articles/tests/test_template_views.py`:

```python
class HomeViewTest(TestCase):
    def setUp(self):
        Article.objects.create(
            slug='test-featured',
            headline='Featured Headline',
            category='MARKET_PULSE',
            body='Body.',
            byline='Staff Writer',
            published_date=datetime.date.today(),
            is_featured=True,
            is_published=True,
        )

    def test_returns_200(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home.html')

    def test_featured_article_in_context(self):
        response = self.client.get(reverse('home'))
        self.assertIsNotNone(response.context['featured'])

    def test_featured_headline_renders(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Featured Headline')
```

Run — fails.

### GREEN

- [ ] Implement `home_view` in `articles/views.py` (queries featured, articles, closings, neighborhoods)
- [ ] Build out `templates/home.html` (see DJANGO_TEMPLATES_PLAN.md Step 7)
- [ ] Create `templates/partials/top_markets_sidebar.html`
- [ ] Create `templates/partials/top_agents_sidebar.html`

Run tests — all pass.

---

## Step 6 — Article detail page

### RED

Add to `backend/articles/tests/test_template_views.py`:

```python
class ArticleDetailViewTest(TestCase):
    def setUp(self):
        self.article = Article.objects.create(
            slug='my-article',
            headline='My Article Headline',
            category='AGENT_WATCH',
            body='Article body.',
            byline='Staff Writer',
            published_date=datetime.date.today(),
            is_published=True,
        )

    def test_returns_200(self):
        response = self.client.get(reverse('article_detail', args=['my-article']))
        self.assertEqual(response.status_code, 200)

    def test_returns_404_for_missing_slug(self):
        response = self.client.get(reverse('article_detail', args=['nope']))
        self.assertEqual(response.status_code, 404)

    def test_headline_renders(self):
        response = self.client.get(reverse('article_detail', args=['my-article']))
        self.assertContains(response, 'My Article Headline')
```

Run — fails.

### GREEN

- [ ] Add `article_detail_view` to `articles/views.py`
- [ ] Create `templates/article_detail.html` (see DJANGO_TEMPLATES_PLAN.md Step 10)
- [ ] Wire `path("articles/<slug:slug>/", article_detail_view, name="article_detail")` in `urls.py`

Run tests — all pass.

---

## Step 7 — Notable Sales page

### RED

Create `backend/sales/tests/test_template_views.py`:

```python
from django.test import TestCase
from django.urls import reverse
from sales.models import NotableSale
import datetime

class NotableSalesViewTest(TestCase):
    def setUp(self):
        NotableSale.objects.create(
            slug='test-sale',
            title='Bayfront Estate',
            price=3500000,
            location='123 Bay Dr, Naples FL',
            city='Naples',
            region='SOUTH_FLORIDA',
            property_type='WATERFRONT_ESTATE',
            close_date=datetime.date.today(),
        )

    def test_returns_200(self):
        response = self.client.get(reverse('notable_sales'))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        response = self.client.get(reverse('notable_sales'))
        self.assertTemplateUsed(response, 'notable_sales.html')

    def test_sale_renders(self):
        response = self.client.get(reverse('notable_sales'))
        self.assertContains(response, 'Bayfront Estate')

    def test_region_filter(self):
        response = self.client.get(reverse('notable_sales') + '?region=ORLANDO')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Bayfront Estate')
```

Run — fails.

### GREEN

- [ ] Add `notable_sales_view` to `sales/views.py`
- [ ] Create `templates/notable_sales.html` (see DJANGO_TEMPLATES_PLAN.md Step 9)
- [ ] Wire `path("notable-sales/", notable_sales_view, name="notable_sales")` in `urls.py`

Run tests — all pass.

---

## Step 8 — Newsletter subscribe

### RED

Create `backend/subscribers/tests/test_template_views.py`:

```python
from django.test import TestCase
from django.urls import reverse
from subscribers.models import Subscriber

class SubscribeViewTest(TestCase):
    def test_post_creates_subscriber(self):
        self.client.post(reverse('subscribe'), {'email': 'test@example.com', 'next': '/'})
        self.assertTrue(Subscriber.objects.filter(email='test@example.com').exists())

    def test_post_redirects(self):
        response = self.client.post(reverse('subscribe'), {'email': 'test@example.com', 'next': '/'})
        self.assertRedirects(response, '/')

    def test_duplicate_email_does_not_error(self):
        Subscriber.objects.create(email='dupe@example.com')
        response = self.client.post(reverse('subscribe'), {'email': 'dupe@example.com', 'next': '/'})
        self.assertEqual(response.status_code, 302)
```

Run — fails.

### GREEN

- [ ] Add `subscribe_view` to `subscribers/views.py` (see DJANGO_TEMPLATES_PLAN.md Step 6)
- [ ] Wire `path("subscribe/", subscribe_view, name="subscribe")` in `urls.py`

Run tests — all pass.

---

## Step 9 — Full test run + smoke test

```bash
cd backend

# Run every test
uv run python manage.py test articles sales subscribers market

# Start the server
uv run python manage.py runserver 8000
```

Open `http://localhost:8000` and click through:
- [ ] Homepage loads with articles
- [ ] Click an article — detail page loads
- [ ] Click Notable Sales — grid loads
- [ ] Click a region tab — filters work
- [ ] Submit newsletter email — redirects back with no error

---

## Tailwind recompile reminder

Any time you add new Tailwind classes to a template, rerun:

```bash
cd backend
./tailwindcss -i static/css/input.css -o static/css/output.css
```

Add `--watch` to keep it running in a second terminal during development.

---

## Reference

Full template code for every file lives in `DJANGO_TEMPLATES_PLAN.md`.
This file is just the order of operations.
