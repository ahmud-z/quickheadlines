import requests
from django.shortcuts import render
from datetime import datetime

IMAGE_BASE_URL = "https://images.assettype.com/"

BASE_API_URL = (
    "https://en.prothomalo.com/api/v1/collections/{category}?offset=0&limit=200"
)

DEFAULT_CATEGORY = "bangladesh"


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
            published_timestamp = story.get("published-at")  # Timestamp
            category_name = category.replace("-", " ").title()  # Category

            # Convert timestamp to readable datetime format
            if published_timestamp:
                published_date = datetime.utcfromtimestamp(
                    int(published_timestamp) / 1000
                ).strftime(
                    "%B %d, %Y, %I:%M:%S %p"
                )  # Example: "March 4, 2025, 02:24:40 AM UTC"
            else:
                published_date = "Unknown"

            # Construct image URL
            image_url = IMAGE_BASE_URL + image_key if image_key else None

            # Only add news if title, description, and author exist
            if title and description and author:
                news_list.append(
                    {
                        "title": title,
                        "description": description,
                        "author": author,
                        "image": image_url,
                        "published_date": published_date,  # Converted Date-Time
                        "category": category_name if category_name else "General News",
                    }
                )

    else:
        news_list = []

    return render(request, "news/home.html", {"news": news_list, "category": category})
