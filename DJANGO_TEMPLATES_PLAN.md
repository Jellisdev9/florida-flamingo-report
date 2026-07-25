# Django Template Conversion Plan

Convert the React SPA to Django server-rendered templates. The Django models,
admin, and database are already done — only the frontend layer changes.

---

## What changes vs. what stays

| Layer | Status |
|-------|--------|
| Django models (`Article`, `NotableSale`, `MarketMetric`, etc.) | **Keep as-is** |
| Django Admin (your CMS) | **Keep as-is** |
| DRF serializers + API views | **Keep** (they're free, and useful later for mobile/RSS) |
| React SPA (`artifacts/florida-property-review/`) | **Removed** — no longer served |
| Node / pnpm / Vite / TypeScript toolchain | **Gone** — never needed again |
| Tailwind CSS classes | **Keep** — same classes, served via standalone binary |
| URL structure (`/`, `/articles/<slug>/`, `/notable-sales/`) | **Keep** |

---

## New file structure inside `backend/`

```
backend/
├── templates/                  ← NEW: all HTML templates
│   ├── base.html               ← shell: <html>, header, market strip, footer
│   ├── home.html               ← extends base, homepage layout
│   ├── article_detail.html     ← extends base, article page
│   └── notable_sales.html      ← extends base, sales grid + filter
├── static/                     ← NEW: CSS and JS assets
│   └── css/
│       └── output.css          ← compiled Tailwind output
├── articles/
│   └── views.py                ← ADD HomeView, ArticleDetailView
├── sales/
│   └── views.py                ← ADD NotableSalesView
└── backend/
    ├── urls.py                 ← ADD template URL patterns
    └── settings/
        └── base.py             ← ADD TEMPLATES dirs, STATICFILES_DIRS
```

---

## Step 1 — Install Tailwind CSS (no Node required)

Tailwind publishes a standalone binary that needs no Node.js. It reads your
templates and generates only the CSS classes you actually use.

```bash
# From the backend/ directory
cd backend

# Download the standalone Tailwind binary for Linux x64
curl -sLO https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-linux-x64
chmod +x tailwindcss-linux-x64
mv tailwindcss-linux-x64 tailwindcss   # rename for convenience
```

Create the Tailwind config file at `backend/tailwind.config.js`:

```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  // Tell Tailwind which files to scan for class names
  content: ["./templates/**/*.html"],
  theme: {
    extend: {
      fontFamily: {
        // Match the React app's font stack
        serif: ['"Playfair Display"', 'Georgia', 'serif'],
        sans:  ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
```

Create the Tailwind input file at `backend/static/css/input.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Custom FPR color utilities — same as the React app's index.css */
.fpr-navy        { background-color: #0d1b2a; }
.fpr-teal        { background-color: #0f4c5c; }
.fpr-gold        { color: #d4a817; }
.fpr-gold-bg     { background-color: #d4a817; }
.fpr-coral       { color: #e05c4b; }
.fpr-coral-bg    { background-color: #e05c4b; }
.fpr-green       { color: #2e7d32; }
```

Compile Tailwind (run this whenever you change a template):

```bash
# From backend/
./tailwindcss -i static/css/input.css -o static/css/output.css --watch
```

The `--watch` flag recompiles automatically when templates change. Run this in
a second terminal alongside `manage.py runserver`.

---

## Step 2 — Configure Django settings

In `backend/backend/settings/base.py`, update two sections:

```python
# --- Templates ---
# Tell Django where to find template files
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Look in backend/templates/ for templates
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# --- Static files ---
# Tell Django where your CSS/JS files live during development
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_URL = '/static/'
```

`BASE_DIR` is already set at the top of `base.py` — it points to `backend/`.

---

## Step 3 — Create `base.html`

This is the master template. Every page extends it. It contains the `<html>`
shell, the header nav, the market strip ticker, and the footer.

Create `backend/templates/base.html`:

```html
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{% block title %}Florida Property Review{% endblock %}</title>

  <!-- Google Fonts (same as React app) -->
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />

  <!-- Compiled Tailwind output -->
  <link rel="stylesheet" href="{% static 'css/output.css' %}" />
</head>
<body class="min-h-screen bg-[#f4f5f7] flex flex-col font-sans">

  <!-- ===== HEADER ===== -->
  <header class="w-full">
    <div class="fpr-navy text-white px-4 md:px-8 py-4">
      <div class="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">

        <!-- Logo + Masthead -->
        <a href="/" class="flex items-center gap-3 group">
          <div class="fpr-gold-bg text-black font-bold text-xl px-2 py-1 flex items-center justify-center h-10 w-10">
            FPR
          </div>
          <div>
            <h1 class="font-serif text-2xl md:text-3xl font-bold tracking-tight">Florida Property Review</h1>
            <p class="text-gray-400 text-xs md:text-sm tracking-wide hidden md:block">
              Notable sales, agent moves, market trends, and neighborhood intelligence across Florida.
            </p>
          </div>
        </a>

        <!-- Nav -->
        <nav class="flex items-center gap-6 whitespace-nowrap text-sm font-medium overflow-x-auto">
          <a href="/"               class="{% if request.resolver_match.url_name == 'home' %}border-b-2 border-[#d4a817] fpr-gold{% else %}text-gray-300 hover:text-white border-b-2 border-transparent{% endif %} pb-1 transition-colors">Home</a>
          <a href="/notable-sales/" class="{% if request.resolver_match.url_name == 'notable_sales' %}border-b-2 border-[#d4a817] fpr-gold{% else %}text-gray-300 hover:text-white border-b-2 border-transparent{% endif %} pb-1 transition-colors">Notable Sales</a>
          <a href="#" class="text-gray-300 hover:text-white pb-1 border-b-2 border-transparent transition-colors">Market Pulse</a>
          <a href="#" class="text-gray-300 hover:text-white pb-1 border-b-2 border-transparent transition-colors">Agents</a>
          <a href="#" class="text-gray-300 hover:text-white pb-1 border-b-2 border-transparent transition-colors">Neighborhoods</a>
          <a href="#" class="text-gray-300 hover:text-white pb-1 border-b-2 border-transparent transition-colors">About</a>
        </nav>

      </div>
    </div>

    <!-- Market Strip Ticker -->
    <div class="fpr-teal text-white w-full py-2 px-4 overflow-x-auto border-t border-b border-gray-700/50 shadow-sm">
      <div class="max-w-7xl mx-auto flex items-center justify-between min-w-max gap-6">
        {% for metric in market_metrics %}
        <div class="flex flex-col gap-1 pr-6 border-r border-gray-600/50 last:border-0 last:pr-0">
          <div class="text-xs text-gray-300 uppercase tracking-wider font-semibold">
            {{ metric.city }} {{ metric.metric_label }}
          </div>
          <div class="flex items-baseline gap-2">
            <span class="font-bold text-lg">{{ metric.value_display }}</span>
            <span class="text-sm font-semibold {% if metric.is_positive %}fpr-green{% else %}fpr-coral{% endif %}">
              {% if metric.is_positive %}▲{% else %}▼{% endif %}
              {{ metric.change_display }}
            </span>
          </div>
          <div class="text-[10px] text-gray-400">vs. Apr 2024</div>
        </div>
        {% endfor %}
      </div>
    </div>
  </header>
  <!-- ===== END HEADER ===== -->

  <!-- Page content goes here -->
  {% block content %}{% endblock %}

  <!-- ===== FOOTER ===== -->
  <footer class="w-full border-t border-gray-200 bg-white py-12 px-4 md:px-8 mt-auto">
    <div class="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-6">
      <div class="flex items-center gap-3 opacity-50 grayscale">
        <div class="fpr-navy text-white font-bold text-xl px-2 py-1 flex items-center justify-center h-10 w-10">FPR</div>
        <span class="font-serif font-bold text-lg">Florida Property Review</span>
      </div>
      <div class="text-sm text-gray-500">&copy; 2024 Florida Property Review. All rights reserved.</div>
    </div>
  </footer>
  <!-- ===== END FOOTER ===== -->

</body>
</html>
```

**Django template concept:** `{% block content %}{% endblock %}` defines a
named slot. Child templates fill the slot with `{% block content %} ... {% endblock %}`.
The `market_metrics` variable comes from the view's context dict (Step 4).

---

## Step 4 — Write the views

Django views are Python functions (or classes) that:
1. Query the database
2. Bundle data into a `context` dictionary
3. Render a template, passing the context in

### 4a — Home view (`articles/views.py`)

The home view needs: featured article, recent articles, top closings, neighborhood
intel, and market metrics (for the base template's strip).

```python
# articles/views.py  — add these imports and views alongside the existing API views

from django.shortcuts import render, get_object_or_404

from .models import Article
from sales.models import NotableSale
from market.models import MarketMetric, NeighborhoodIntel


def _base_context():
    """
    Returns context shared by every page (market strip data).
    Called from every view and merged into the page-specific context.
    """
    return {
        'market_metrics': MarketMetric.objects.all()[:5],
    }


def home_view(request):
    featured  = Article.objects.filter(is_featured=True, is_published=True).first()
    articles  = Article.objects.filter(is_published=True).exclude(
                    pk=featured.pk if featured else None
                )[:5]
    closings  = NotableSale.objects.order_by('-price')[:2]
    neighborhoods = NeighborhoodIntel.objects.all()[:3]

    # Handle newsletter POST (submitted from this page's form)
    subscribed = request.session.pop('subscribed', False)

    context = {
        **_base_context(),
        'featured':      featured,
        'articles':      articles,
        'closings':      closings,
        'neighborhoods': neighborhoods,
        'subscribed':    subscribed,
    }
    return render(request, 'home.html', context)


def article_detail_view(request, slug):
    article = get_object_or_404(Article, slug=slug, is_published=True)
    related = Article.objects.filter(
        category=article.category,
        is_published=True,
    ).exclude(pk=article.pk)[:3]

    context = {
        **_base_context(),
        'article': article,
        'related': related,
    }
    return render(request, 'article_detail.html', context)
```

### 4b — Notable Sales view (`sales/views.py`)

```python
# sales/views.py — add these alongside existing API views

from django.shortcuts import render

from .models import NotableSale
from market.models import MarketMetric, FastestGrowingMarket, Agent


REGION_MAP = {
    'SOUTH_FLORIDA':  'South Florida',
    'TAMPA_BAY':      'Tampa Bay',
    'ORLANDO':        'Orlando',
    'JACKSONVILLE':   'Jacksonville',
    'PANHANDLE':      'Panhandle',
}


def notable_sales_view(request):
    region = request.GET.get('region')     # e.g. "SOUTH_FLORIDA"

    featured = NotableSale.objects.filter(is_featured=True).first()
    sales    = NotableSale.objects.all()
    if region and region in REGION_MAP:
        sales = sales.filter(region=region)
    sales = sales[:20]

    top_closings    = NotableSale.objects.order_by('-price')[:5]
    fastest_growing = FastestGrowingMarket.objects.order_by('rank')[:5]
    market_metrics  = MarketMetric.objects.all()[:5]

    subscribed = request.session.pop('subscribed', False)

    context = {
        'market_metrics':  market_metrics,
        'featured':        featured,
        'sales':           sales,
        'top_closings':    top_closings,
        'fastest_growing': fastest_growing,
        'active_region':   region or '',
        'subscribed':      subscribed,
        'region_map':      REGION_MAP,
    }
    return render(request, 'notable_sales.html', context)
```

---

## Step 5 — Wire up URLs

Replace the React SPA's client-side routes with Django URL patterns.
Update `backend/backend/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

from articles.views import home_view, article_detail_view
from sales.views import notable_sales_view
from subscribers.views import subscribe_view   # see Step 6


def health_check(request):
    return JsonResponse({"status": "ok"})


urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    path("api/healthz/", health_check),

    # Existing DRF API (keep — costs nothing)
    path("api/", include("articles.urls")),
    path("api/", include("sales.urls")),
    path("api/", include("market.urls")),
    path("api/", include("subscribers.urls")),

    # NEW: Template-rendered pages
    path("",                         home_view,           name="home"),
    path("articles/<slug:slug>/",    article_detail_view, name="article_detail"),
    path("notable-sales/",           notable_sales_view,  name="notable_sales"),
    path("subscribe/",               subscribe_view,      name="subscribe"),
]
```

---

## Step 6 — Newsletter subscription (form POST)

The React version used JavaScript to POST JSON. In Django templates the form
POSTs HTML form data. The view saves the subscriber and redirects back.

Add to `subscribers/views.py` (alongside any existing API views):

```python
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from .models import Subscriber


@require_POST
def subscribe_view(request):
    email    = request.POST.get('email', '').strip()
    next_url = request.POST.get('next', '/')   # where to send user after

    if email:
        # get_or_create handles duplicate emails gracefully
        Subscriber.objects.get_or_create(email=email)
        request.session['subscribed'] = True

    return redirect(next_url)
```

In templates, the form looks like this:

```html
<form method="POST" action="{% url 'subscribe' %}" class="flex gap-2">
  {% csrf_token %}
  <!-- 'next' tells the view where to redirect after POST -->
  <input type="hidden" name="next" value="{{ request.path }}" />
  <input type="email" name="email" placeholder="Your email address"
         class="flex-1 px-4 py-3 text-gray-900 rounded-sm focus:outline-none focus:ring-2 focus:ring-[#d4a817]" />
  <button type="submit"
          class="fpr-gold-bg text-black font-bold px-6 py-3 rounded-sm hover:bg-yellow-500 transition-colors shrink-0">
    SUBSCRIBE
  </button>
</form>
```

**Django concept:** `{% csrf_token %}` inserts a hidden security token. Django
rejects any POST that doesn't include it. Always include it in forms.

---

## Step 7 — Create `home.html`

Create `backend/templates/home.html`:

```html
{% extends "base.html" %}

{% block title %}Florida Property Review — Florida Real Estate Intelligence{% endblock %}

{% block content %}
<main class="flex-1 w-full max-w-7xl mx-auto px-4 md:px-8 py-8 md:py-10 flex flex-col gap-10">

  <!-- Hero + Top Markets Sidebar -->
  <div class="flex flex-col lg:flex-row gap-8">

    <!-- Left: Featured Article Hero -->
    <div class="lg:w-2/3 relative rounded-sm overflow-hidden shadow-sm group">
      <div class="absolute inset-0 bg-black/40 z-10"></div>
      <img src="{{ featured.hero_image_url|default:'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=1200' }}"
           alt="{{ featured.headline|default:'Featured Story' }}"
           class="w-full h-[400px] md:h-[500px] object-cover transition-transform duration-700 group-hover:scale-105" />
      <div class="absolute inset-0 z-20 flex flex-col justify-end p-6 md:p-10 text-white bg-gradient-to-t from-black/80 via-black/40 to-transparent">
        <span class="fpr-coral-bg text-white text-xs font-bold px-3 py-1 uppercase tracking-wider rounded-sm w-fit mb-4">
          Featured Story
        </span>
        <h2 class="font-serif text-3xl md:text-5xl font-bold leading-tight mb-3">
          {{ featured.headline|default:"Florida's real estate market, tracked like a business desk." }}
        </h2>
        <p class="text-lg md:text-xl text-gray-200 mb-6 max-w-2xl">
          {{ featured.subheadline|default:"Deal flow, agent moves, and market shifts—delivered with clarity and speed." }}
        </p>
        {% if featured %}
        <a href="{% url 'article_detail' featured.slug %}"
           class="flex items-center gap-2 font-bold text-sm bg-white text-black px-6 py-3 w-fit rounded-sm hover:fpr-gold-bg hover:text-white transition-colors">
          READ THE STORY &rarr;
        </a>
        {% endif %}
      </div>
    </div>

    <!-- Right: Top Markets Sidebar -->
    <div class="lg:w-1/3">
      {% include "partials/top_markets_sidebar.html" %}
    </div>

  </div>

  <!-- Article Cards Row -->
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-6">
    {% for article in articles %}
    <a href="{% url 'article_detail' article.slug %}" class="group flex flex-col bg-white border border-gray-200 rounded-sm overflow-hidden shadow-sm hover:shadow-md transition-shadow">
      <div class="relative h-40 overflow-hidden">
        <img src="{{ article.hero_image_url|default:'https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=600' }}"
             alt="{{ article.headline }}"
             class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105" />
        <span class="absolute top-2 left-2 fpr-coral-bg text-white text-[10px] font-bold px-2 py-0.5 uppercase tracking-wider rounded-sm">
          {{ article.get_category_display }}
        </span>
      </div>
      <div class="p-4 flex flex-col gap-2 flex-1">
        <h3 class="font-serif font-bold text-sm leading-snug group-hover:fpr-gold transition-colors line-clamp-3">
          {{ article.headline }}
        </h3>
        <div class="mt-auto text-xs text-gray-400">
          {{ article.published_date|date:"M j, Y" }} &middot; {{ article.read_time_minutes }} min
        </div>
      </div>
    </a>
    {% endfor %}
  </div>

  <!-- Lower 3-Column Section -->
  <div class="grid grid-cols-1 md:grid-cols-3 gap-8">

    <!-- Luxury Closings -->
    <div class="bg-white border border-gray-200 rounded-sm p-5 shadow-sm h-full">
      <div class="flex items-center justify-between mb-4 pb-2 border-b-2 border-[#0d1b2a]">
        <h3 class="font-serif font-bold text-lg">Luxury Closings</h3>
      </div>
      <div class="flex flex-col gap-4">
        {% for sale in closings %}
        {% if not forloop.first %}<div class="h-px w-full bg-gray-100"></div>{% endif %}
        <a href="{% url 'notable_sales' %}" class="flex items-start gap-4 group">
          <img src="{{ sale.hero_image_url|default:'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=400' }}"
               alt="{{ sale.city }}"
               class="w-20 h-20 object-cover rounded-sm shrink-0" />
          <div class="flex flex-col">
            <span class="font-bold text-lg text-gray-900">{{ sale.price_display }}</span>
            <span class="text-sm text-gray-600">{{ sale.title }}</span>
          </div>
        </a>
        {% endfor %}
      </div>
    </div>

    <!-- Top Agents -->
    {% include "partials/top_agents_sidebar.html" %}

    <!-- Neighborhood Intelligence -->
    <div class="bg-white border border-gray-200 rounded-sm p-5 shadow-sm h-full">
      <div class="flex items-center justify-between mb-4 pb-2 border-b-2 border-[#0d1b2a]">
        <h3 class="font-serif font-bold text-lg">Neighborhood Intelligence</h3>
      </div>
      <div class="flex flex-col gap-5">
        {% for n in neighborhoods %}
        <div class="flex flex-col gap-2 {% if not forloop.last %}border-b border-gray-100 pb-4{% endif %}">
          <div class="flex items-center gap-2">
            <span class="font-bold text-gray-900">{{ n.neighborhood }}</span>
            <span class="text-[10px] font-bold px-2 py-0.5 rounded-sm
              {% if n.tag == 'HOT' %}fpr-coral-bg text-white
              {% elif n.tag == 'RISING' %}fpr-gold-bg text-black
              {% elif n.tag == 'COOLING' %}bg-blue-100 text-blue-800
              {% else %}bg-gray-100 text-gray-700{% endif %}">
              {{ n.tag }}
            </span>
          </div>
          <p class="text-sm text-gray-600">{{ n.description }}</p>
        </div>
        {% endfor %}
      </div>
    </div>

  </div>

  <!-- Newsletter Banner -->
  <div class="w-full fpr-navy rounded-sm p-8 md:p-12 shadow-sm text-center flex flex-col md:flex-row items-center justify-between gap-6">
    <div class="text-left max-w-xl">
      <h3 class="font-serif font-bold text-3xl text-white mb-2">Stay ahead of the market.</h3>
      <p class="text-gray-300">Join 15,000+ real estate professionals receiving our daily market intelligence.</p>
    </div>
    {% if subscribed %}
      <p class="text-[#d4a817] font-bold text-lg">You're subscribed!</p>
    {% else %}
      <form method="POST" action="{% url 'subscribe' %}" class="flex w-full md:w-auto max-w-md gap-2">
        {% csrf_token %}
        <input type="hidden" name="next" value="/" />
        <input type="email" name="email" placeholder="Your email address"
               class="flex-1 px-4 py-3 text-gray-900 rounded-sm focus:outline-none focus:ring-2 focus:ring-[#d4a817]" />
        <button type="submit"
                class="fpr-gold-bg text-black font-bold px-6 py-3 rounded-sm hover:bg-yellow-500 transition-colors shrink-0">
          SUBSCRIBE
        </button>
      </form>
    {% endif %}
  </div>

</main>
{% endblock %}
```

---

## Step 8 — Create template partials

Partials are reusable template fragments included with `{% include %}`. They
share the parent template's context automatically.

Create `backend/templates/partials/top_markets_sidebar.html`:

```html
<div class="bg-white border border-gray-200 rounded-sm p-5 shadow-sm h-fit">
  <div class="flex items-center justify-between mb-4 pb-2 border-b-2 border-[#0d1b2a]">
    <h3 class="font-serif font-bold text-lg">Top Markets</h3>
    <span class="text-xs text-gray-500 uppercase tracking-wider font-semibold">Trend</span>
  </div>
  <div class="flex flex-col gap-4">
    {% for metric in market_metrics %}
    <div class="flex items-center justify-between">
      <div class="flex flex-col">
        <span class="font-semibold text-gray-900">{{ metric.city }}</span>
        <span class="text-sm text-gray-500">{{ metric.value_display }}</span>
      </div>
      <div class="flex items-center gap-1 font-bold {% if metric.is_positive %}fpr-green{% else %}fpr-coral{% endif %}">
        {% if metric.is_positive %}▲{% else %}▼{% endif %}
        {{ metric.change_display }}
      </div>
    </div>
    {% endfor %}
  </div>
  <a href="/notable-sales/" class="mt-6 block w-full text-center text-sm font-bold fpr-navy text-white py-2.5 rounded-sm hover:bg-[#0f4c5c] transition-colors">
    VIEW FULL REPORT →
  </a>
</div>
```

Create `backend/templates/partials/top_agents_sidebar.html`:

```html
<div class="bg-white border border-gray-200 rounded-sm p-5 shadow-sm h-full">
  <div class="flex items-center justify-between mb-4 pb-2 border-b-2 border-[#0d1b2a]">
    <h3 class="font-serif font-bold text-lg">Top Agents This Month</h3>
  </div>
  <div class="flex flex-col gap-5">
    {% for agent in top_agents %}
    <div class="flex items-center gap-3">
      <div class="w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center font-serif font-bold text-lg fpr-navy text-white shrink-0">
        {{ agent.rank }}
      </div>
      <div class="flex flex-col">
        <span class="font-bold text-sm text-gray-900">{{ agent.name }}</span>
        <span class="text-xs text-gray-500">{{ agent.location }} &middot; {{ agent.volume_display }}</span>
      </div>
    </div>
    {% endfor %}
  </div>
</div>
```

**Note:** `top_agents` needs to be added to `_base_context()` (or to each view's
context individually). Add this line to `_base_context()` in `articles/views.py`:

```python
from market.models import MarketMetric, Agent

def _base_context():
    return {
        'market_metrics': MarketMetric.objects.all()[:5],
        'top_agents':     Agent.objects.order_by('rank')[:5],
    }
```

---

## Step 9 — Create `notable_sales.html`

The React version used JavaScript state to filter by region (no page reload).
The Django version uses query strings: `/notable-sales/?region=SOUTH_FLORIDA`.
The page reloads when you change region — this is fine, and simpler.

Create `backend/templates/notable_sales.html`:

```html
{% extends "base.html" %}

{% block title %}Notable Sales — Florida Property Review{% endblock %}

{% block content %}

<!-- Page Header -->
<div class="w-full bg-white border-b border-gray-200 py-8 px-4 md:px-8">
  <div class="max-w-7xl mx-auto">
    <h1 class="font-serif text-4xl md:text-5xl font-bold text-[#0d1b2a]">Notable Sales</h1>
    <p class="text-lg text-gray-500 mt-2">The biggest closings. The most exclusive addresses. Across Florida.</p>
  </div>
</div>

<main class="flex-1 w-full max-w-7xl mx-auto px-4 md:px-8 py-8 flex flex-col gap-8">

  <!-- Region Filter Tabs -->
  <!-- Each button is an <a> tag linking to ?region=VALUE — no JavaScript needed -->
  <div class="flex items-center gap-4 overflow-x-auto pb-2">
    <a href="{% url 'notable_sales' %}"
       class="whitespace-nowrap px-4 py-2 rounded-full text-sm font-bold transition-all
              {% if not active_region %}bg-[#0d1b2a] text-white border-b-2 border-[#d4a817]{% else %}bg-white text-gray-600 border border-gray-200 hover:bg-gray-50{% endif %}">
      All Regions
    </a>
    {% for code, label in region_map.items %}
    <a href="?region={{ code }}"
       class="whitespace-nowrap px-4 py-2 rounded-full text-sm font-bold transition-all
              {% if active_region == code %}bg-[#0d1b2a] text-white border-b-2 border-[#d4a817]{% else %}bg-white text-gray-600 border border-gray-200 hover:bg-gray-50{% endif %}">
      {{ label }}
    </a>
    {% endfor %}
  </div>

  <div class="flex flex-col lg:flex-row gap-10">

    <!-- Main Content -->
    <div class="w-full lg:w-2/3 flex flex-col gap-10">

      <!-- Featured Sale Hero -->
      {% if featured %}
      <div class="relative rounded-sm overflow-hidden shadow-sm group bg-black">
        <img src="{{ featured.hero_image_url|default:'https://images.unsplash.com/photo-1502005229762-cf1b2da7c5d6?w=1200' }}"
             alt="{{ featured.title }}"
             class="w-full h-[450px] object-cover opacity-70 group-hover:opacity-80 group-hover:scale-105 transition-all duration-700" />
        <div class="absolute inset-0 z-20 flex flex-col justify-end p-6 md:p-10 text-white bg-gradient-to-t from-black/90 via-black/40 to-transparent">
          <span class="fpr-coral-bg text-white text-xs font-bold px-3 py-1 uppercase tracking-wider rounded-sm w-fit mb-4">
            FEATURED SALE
          </span>
          <h2 class="font-serif text-3xl md:text-4xl font-bold leading-tight mb-3">{{ featured.title }}</h2>
          <p class="text-gray-200 mb-6 max-w-2xl">{{ featured.price_display }} — {{ featured.city }}, FL</p>
          <a href="{% url 'notable_sales' %}"
             class="flex items-center gap-2 font-bold text-sm bg-white text-black px-6 py-3 w-fit rounded-sm hover:fpr-gold-bg hover:text-white transition-colors">
            READ FULL STORY &rarr;
          </a>
        </div>
      </div>
      {% endif %}

      <!-- Sales Grid -->
      <div>
        <h3 class="font-serif font-bold text-2xl text-[#0d1b2a] mb-6">Recent Notable Sales</h3>
        {% if sales %}
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
          {% for sale in sales %}
          <div class="group relative rounded-sm overflow-hidden bg-white shadow-sm border border-gray-200 flex flex-col h-full">
            <div class="relative h-48 w-full overflow-hidden">
              <div class="absolute top-3 right-3 z-10 fpr-navy text-white text-sm font-bold px-3 py-1 rounded-sm shadow-md">
                {{ sale.price_display }}
              </div>
              <img src="{{ sale.hero_image_url|default:'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=600' }}"
                   alt="{{ sale.title }}"
                   class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105" />
            </div>
            <div class="p-5 flex flex-col flex-1">
              <span class="text-[10px] font-bold tracking-wider fpr-coral uppercase mb-2">
                {{ sale.get_property_type_display }}
              </span>
              <h4 class="font-serif text-lg font-bold leading-tight mb-3">{{ sale.title }}</h4>
              <div class="mt-auto flex items-center justify-between text-xs text-gray-500 pt-3 border-t border-gray-100">
                <span>{{ sale.city }}, FL</span>
                <span>{{ sale.close_date|date:"M j, Y" }}</span>
              </div>
            </div>
          </div>
          {% endfor %}
        </div>
        {% else %}
        <p class="text-gray-400 text-sm py-8 text-center">No sales found for this region.</p>
        {% endif %}
      </div>

    </div>

    <!-- Sidebar -->
    <div class="w-full lg:w-1/3 flex flex-col gap-8">

      <!-- Top Luxury Closings -->
      <div class="bg-white border border-gray-200 rounded-sm p-5 shadow-sm">
        <div class="flex items-center justify-between mb-5 pb-2 border-b-2 border-[#0d1b2a]">
          <h3 class="font-serif font-bold text-lg">Top Luxury Closings</h3>
        </div>
        <div class="flex flex-col gap-4">
          {% for sale in top_closings %}
          <div class="flex items-center gap-3">
            <span class="font-serif font-bold text-2xl text-gray-200 shrink-0 w-6">{{ forloop.counter }}</span>
            <div class="flex flex-col flex-1">
              <span class="font-bold text-sm text-gray-900">{{ sale.title }}</span>
              <span class="text-xs text-gray-500">{{ sale.city }}</span>
            </div>
            <span class="fpr-navy text-white text-xs font-bold px-2 py-1 rounded-sm shrink-0">
              {{ sale.price_display }}
            </span>
          </div>
          {% endfor %}
        </div>
      </div>

      <!-- Fastest Growing Markets -->
      <div class="bg-white border border-gray-200 rounded-sm p-5 shadow-sm">
        <div class="flex items-center justify-between mb-5 pb-2 border-b-2 border-[#0d1b2a]">
          <h3 class="font-serif font-bold text-lg">Fastest Growing Markets</h3>
          <span class="text-xs text-gray-500 uppercase tracking-wider font-semibold">% Change</span>
        </div>
        <div class="flex flex-col gap-4">
          {% for item in fastest_growing %}
          <div class="flex items-center justify-between border-b border-gray-100 last:border-0 pb-3 last:pb-0">
            <div class="flex items-center gap-3">
              <span class="font-serif font-bold text-lg text-[#d4a817] w-4">{{ item.rank }}</span>
              <span class="font-bold text-sm text-gray-800">{{ item.location }}</span>
            </div>
            <span class="font-bold fpr-green">{{ item.change_display }}</span>
          </div>
          {% endfor %}
        </div>
      </div>

      <!-- Subscribe CTA -->
      <div class="bg-[#0f4c5c] text-white rounded-sm p-6 shadow-sm flex flex-col items-center text-center">
        <h3 class="font-serif font-bold text-2xl mb-2">Subscribe for Deal Alerts</h3>
        <p class="text-sm text-gray-200 mb-6 leading-relaxed">
          Get the latest notable sales and market intelligence—delivered weekly.
        </p>
        {% if subscribed %}
          <p class="text-[#d4a817] font-bold">You're subscribed!</p>
        {% else %}
          <form method="POST" action="{% url 'subscribe' %}" class="w-full flex flex-col gap-3">
            {% csrf_token %}
            <input type="hidden" name="next" value="{{ request.path }}" />
            <input type="email" name="email" placeholder="Email address"
                   class="w-full px-4 py-3 text-gray-900 rounded-sm focus:outline-none focus:ring-2 focus:ring-[#d4a817] text-sm" />
            <button type="submit"
                    class="w-full fpr-navy text-white font-bold py-3 rounded-sm hover:bg-gray-800 transition-colors text-sm">
              SUBSCRIBE
            </button>
          </form>
        {% endif %}
        <p class="text-[10px] text-gray-300 mt-4">No spam. Unsubscribe anytime.</p>
      </div>

    </div>
  </div>
</main>
{% endblock %}
```

---

## Step 10 — Create `article_detail.html`

Create `backend/templates/article_detail.html`:

```html
{% extends "base.html" %}

{% block title %}{{ article.headline }} — Florida Property Review{% endblock %}

{% block content %}
<main class="flex-1 w-full max-w-7xl mx-auto px-4 md:px-8 py-8 flex flex-col lg:flex-row gap-10">

  <!-- Article Body Column -->
  <div class="w-full lg:w-2/3 bg-white p-6 md:p-10 shadow-sm border border-gray-200 rounded-sm">

    <div class="mb-6">
      <span class="fpr-coral-bg text-white text-[10px] font-bold px-3 py-1 uppercase tracking-wider rounded-sm w-fit">
        {{ article.get_category_display }}
      </span>
    </div>

    <h1 class="font-serif text-4xl md:text-5xl font-bold leading-tight mb-4 italic text-[#0d1b2a]">
      {{ article.headline }}
    </h1>

    {% if article.subheadline %}
    <p class="text-xl text-gray-600 mb-8 font-medium">{{ article.subheadline }}</p>
    {% endif %}

    <!-- Byline Bar -->
    <div class="flex flex-wrap items-center justify-between gap-4 py-4 border-t border-b border-gray-100 mb-8">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-full bg-gray-200 overflow-hidden shrink-0">
          {% if article.author_avatar_url %}
          <img src="{{ article.author_avatar_url }}" alt="Author" class="w-full h-full object-cover" />
          {% endif %}
        </div>
        <div class="flex flex-col">
          <span class="text-sm font-bold text-gray-900">{{ article.byline }}</span>
          <span class="text-xs text-gray-500">
            {{ article.published_date|date:"M j, Y" }} &middot; {{ article.read_time_minutes }} min read
          </span>
        </div>
      </div>
    </div>

    {% if article.hero_image_url %}
    <div class="w-full mb-10 rounded-sm overflow-hidden">
      <img src="{{ article.hero_image_url }}" alt="{{ article.headline }}"
           class="w-full h-auto object-cover max-h-[500px]" />
    </div>
    {% endif %}

    <!-- Article Body -->
    <!-- |linebreaksbr converts \n\n into <br> tags -->
    <div class="prose prose-lg max-w-none text-gray-800">
      {{ article.body|linebreaksbr }}
    </div>

  </div>

  <!-- Sidebar -->
  <div class="w-full lg:w-1/3 flex flex-col gap-8">

    {% if related %}
    <div class="bg-white border border-gray-200 rounded-sm p-5 shadow-sm">
      <h3 class="font-serif font-bold text-lg mb-4 pb-2 border-b-2 border-[#0d1b2a]">Related Stories</h3>
      <div class="flex flex-col gap-5">
        {% for a in related %}
        {% if not forloop.first %}<div class="w-full h-px bg-gray-100"></div>{% endif %}
        <a href="{% url 'article_detail' a.slug %}" class="flex gap-4 group">
          <img src="{{ a.hero_image_url|default:'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=400' }}"
               class="w-20 h-20 object-cover rounded-sm shrink-0" alt="{{ a.headline }}" />
          <div class="flex flex-col">
            <span class="text-[10px] font-bold text-gray-500 uppercase tracking-wider mb-1">
              {{ a.get_category_display }}
            </span>
            <span class="font-bold text-sm leading-snug group-hover:fpr-gold transition-colors line-clamp-2 mb-1">
              {{ a.headline }}
            </span>
            <span class="text-xs text-gray-400">{{ a.published_date|date:"M j, Y" }}</span>
          </div>
        </a>
        {% endfor %}
      </div>
    </div>
    {% endif %}

    {% include "partials/top_markets_sidebar.html" %}

    <!-- Newsletter compact -->
    <div class="fpr-navy text-white rounded-sm p-6 shadow-sm">
      <h3 class="font-serif font-bold text-xl mb-2 text-center">Stay ahead of the market.</h3>
      <p class="text-sm text-gray-300 text-center mb-4">Get the latest Florida real estate intelligence delivered weekly.</p>
      <form method="POST" action="{% url 'subscribe' %}" class="flex flex-col gap-2">
        {% csrf_token %}
        <input type="hidden" name="next" value="{{ request.path }}" />
        <input type="email" name="email" placeholder="Email address"
               class="w-full px-3 py-2 text-gray-900 rounded-sm focus:outline-none focus:ring-2 focus:ring-[#d4a817]" />
        <button type="submit"
                class="w-full fpr-gold-bg text-black font-bold py-2 rounded-sm hover:bg-yellow-500 transition-colors">
          SUBSCRIBE
        </button>
      </form>
      <p class="text-[10px] text-gray-400 text-center mt-3">No spam. Unsubscribe anytime.</p>
    </div>

  </div>

</main>
{% endblock %}
```

---

## Step 11 — Load seed data and test

```bash
cd backend

# Run migrations (already done, but check)
uv run python manage.py migrate

# Load seed data
uv run python manage.py loaddata fixtures/initial_data.json

# In terminal 1: compile Tailwind
./tailwindcss -i static/css/input.css -o static/css/output.css --watch

# In terminal 2: run Django
uv run python manage.py runserver 8000
```

Visit `http://localhost:8000/` — you should see the homepage with real data.

---

## Testing approach (TDD)

For each view, write a test before wiring the URL. The test pattern for template
views is slightly simpler than API tests — check status code, assert context
variables exist, and check that key strings appear in the rendered HTML.

```python
# articles/tests/test_views.py  — template view tests

from django.test import TestCase
from django.urls import reverse
from articles.models import Article
import datetime


class HomeViewTest(TestCase):

    def setUp(self):
        # Create a featured article to use in tests
        Article.objects.create(
            slug='test-featured',
            headline='Test Featured Article',
            category=Article.Category.MARKET_PULSE,
            body='Body text.',
            byline='Staff Writer',
            published_date=datetime.date.today(),
            is_featured=True,
            is_published=True,
        )

    def test_home_returns_200(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_featured_article_in_context(self):
        response = self.client.get(reverse('home'))
        self.assertIsNotNone(response.context['featured'])

    def test_featured_headline_appears_in_html(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Test Featured Article')


class ArticleDetailViewTest(TestCase):

    def setUp(self):
        self.article = Article.objects.create(
            slug='my-article',
            headline='My Article Headline',
            category=Article.Category.AGENT_WATCH,
            body='Article body.',
            byline='Staff Writer',
            published_date=datetime.date.today(),
            is_published=True,
        )

    def test_article_detail_returns_200(self):
        response = self.client.get(reverse('article_detail', args=['my-article']))
        self.assertEqual(response.status_code, 200)

    def test_article_detail_returns_404_for_missing_slug(self):
        response = self.client.get(reverse('article_detail', args=['does-not-exist']))
        self.assertEqual(response.status_code, 404)

    def test_headline_appears_in_html(self):
        response = self.client.get(reverse('article_detail', args=['my-article']))
        self.assertContains(response, 'My Article Headline')
```

Run tests with:

```bash
cd backend
uv run python manage.py test articles sales subscribers market
```

---

## Summary of what you're building vs. what React built

| Feature | React approach | Django template approach |
|---------|---------------|--------------------------|
| Routing | wouter (client-side JS) | Django URL patterns |
| Data fetching | `useQuery()` → fetch API | View queries ORM directly |
| Newsletter form | `fetch()` POST + JS state | HTML form POST + redirect |
| Region filter tabs | `useState()`, no page reload | `?region=` query string, page reloads |
| Tailwind CSS | Vite PostCSS plugin | Standalone Tailwind binary |
| Template language | JSX | Django template tags (`{{ }}`, `{% %}`) |
| Active nav highlight | `useLocation()` hook | `request.resolver_match.url_name` |

The tradeoff you're accepting: region filtering causes a page reload instead of
an instant tab switch. For an editorial publication this is completely fine.
If you ever want the filter to feel instant without a full reload, HTMX
(`hx-get="?region=X" hx-target="#sales-grid"`) can do it with one attribute
and no JavaScript file.
