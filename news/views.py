import requests
from django.shortcuts import render

IMAGE_BASE_URL = "https://images.prothomalo.com/"  # Base URL for images
BASE_API_URL = "https://en.prothomalo.com/api/v1/collections/{category}?offset=0&limit=200"

DEFAULT_CATEGORY = "international"

def fetch_news(request, category=DEFAULT_CATEGORY):
    api_url = BASE_API_URL.format(category=category)
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        news_items = data.get("items", [])
        news_list = []

        for item in news_items:
            story = item.get("story", {})
            title = story.get("seo", {}).get("meta-title")
            description = story.get("seo", {}).get("meta-description")
            author = story.get("author-name")
            image_key = story.get("hero-image-s3-key")
            published_date = story.get("published-time")
            news_type = story.get("subheadline")

            # Only add news if title, description, and author exist
            if title and description and author:
                image_url = IMAGE_BASE_URL + image_key if image_key else None

                news_list.append({
                    "title": title,
                    "description": description,
                    "author": author,
                    "image": image_url,
                    "published_date": published_date if published_date else "Unknown",
                    "news_type": news_type if news_type else "General News",
                })

    else:
        news_list = []

    return render(request, "news/home.html", {"news": news_list, "category": category})
