

## 📦 BharatX – E-commerce Price API

`BharatX` is a Django-based API that fetches real-time product listings from major e-commerce websites using Gemini LLM and enhances accuracy using Serper.dev's Google Search API.

---

### ✅ Features

* Accepts product and country as input
* Uses Gemini for generating site and product listing
* Uses Serper API to correct prices and fetch real URLs
* Supports any product/country
* Built as a RESTful POST API using Django REST Framework
* Deployable on [Render](https://render.com)

---

## 🚀 API Endpoint

```
POST /api/fetch-prices/
```

### 🔸 Request Body

```json
{
  "query": "iPhone 16 Pro 128GB",
  "country": "AU"
}
```

### 🔸 Response

```json
{
    "results": [
        {
            "site": "apple.com/au",
            "productName": "iPhone 16 Pro, 128GB - Natural Titanium",
            "price": 1999.0,
            "currency": "AUD",
            "link": "https://www.apple.com/au/iphone-16-pro/"
        },
        {
            "site": "jbhifi.com.au",
            "productName": "Apple iPhone 16 Pro 128GB - Blue Titanium",
            "price": 1949.0,
            "currency": "AUD",
            "link": "https://www.jbhifi.com.au/collections/mobile-phones/iphone-16-pro"
        },
        {
            "site": "amazon.com.au",
            "productName": "New Apple iPhone 16 Pro (128 GB) - Black Titanium",
            "price": 1989.0,
            "currency": "AUD",
            "link": "https://www.amazon.com.au/Apple-iPhone-16-Pro-128/dp/B0DGJH6ZSW"
        },
        {
            "site": "telstra.com.au",
            "productName": "iPhone 16 Pro 128GB - White Titanium",
            "price": 2029.0,
            "currency": "AUD",
            "link": "https://www.telstra.com.au/mobile-phones/mobiles-on-a-plan/apple/iphone-16-pro"
        },
        {
            "site": "kogan.com",
            "productName": "Apple iPhone 16 Pro 128GB (Space Black)",
            "price": 1919.0,
            "currency": "AUD",
            "link": "https://www.kogan.com/au/buy/mobile-guru-australia-apple-iphone-16-pro-128gb-black-titanium-excellent-refurbished-ip16p128bktb/"
        }
    ]
}
```

---

## 🧠 How It Works

1. The API receives a `query` (product) and `country`.
2. Gemini 2.5 Flash model generates a Python list of site suggestions with product names, prices, currency.
3. Each listing is refined by querying Serper.dev (Google Search API).
4. Real URLs and snippet-based prices are extracted and updated in the result.
5. A clean JSON response is returned.

---

## ⚙️ Setup & Local Development

### 1. Clone the Repo

```bash
git clone https://github.com/ananttyagi004/bharatx.git
cd bharatx
```

### 2. Create Virtual Environment

```bash
python3 -m venv env
source env/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Add `.env` File

```ini
GEMINI_API_KEY=your_gemini_api_key
SERPER_API_KEY=your_serper_api_key
```

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Run Server

```bash
python manage.py runserver
```

Test locally:

```bash
curl -X POST http://localhost:8000/api/fetch-prices/ \
  -H "Content-Type: application/json" \
  -d '{"query": "iPhone 16 Pro", "country": "UK"}'
```

---

