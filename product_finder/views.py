
import google.generativeai as genai
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import requests
import urllib.parse
import os

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

# Function to get real URL from Serper
def get_real_url(query):
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "q": query
    }

    try:
        res = requests.post(url, headers=headers, json=data)
        res.raise_for_status()
        results = res.json().get("organic", [])
        if results:
            return results[0].get("link")
    except Exception as e:
        print("Serper error:", e)

    return None

class ProductPriceFetcher(APIView):
    def post(self, request):
        product = request.data.get("query")
        country = request.data.get("country")

        if not product or not country:
            return Response({"error": "Both 'query' and 'country' are required."}, status=status.HTTP_400_BAD_REQUEST)

        prompt = f"""
        Give me a Python list of ecommerce listings for: '{product}' in country: '{country}'.
        Each item must include:
        - site (e.g., amazon.com, flipkart.com, bestbuy.ca)
        - productName
        - price (numeric)
        - currency (USD, INR, etc)
        Use current pricing where possible
        Only output a valid Python list. No markdown, no explanation.
        """

        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content(prompt)
            raw = response.text.strip()

            if raw.startswith("```python"):
                raw = raw.replace("```python", "").strip()
            if raw.endswith("```"):
                raw = raw[:-3].strip()

            try:
                listings = eval(raw, {"__builtins__": None}, {})
            except Exception:
                return Response({"error": "Gemini response could not be parsed", "raw": raw}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Generate real URLs using Serper
            for item in listings:
                query = f"{item['productName']} site:{item['site']}"
                item['link'] = get_real_url(query)

            return Response({"results": listings}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

