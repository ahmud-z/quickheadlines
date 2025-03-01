import requests
from django.shortcuts import render

PROTHOM_ALO_API = "https://en.prothomalo.com/api/v1/collections/cricket-sports?offset=20&limit=100"

def fetch_news(request):
    response = requests.get(PROTHOM_ALO_API)
    if response.status_code == 200:
        data = response.json()
        news_items = data.get("items", [])  # Get the items list
        news_list = []

        for item in news_items:
            story = item.get("story", {})
            news_list.append({
                "title": story.get("seo", {}).get("meta-title", "No Title"),
                "description": story.get("seo", {}).get("meta-description", "No Description"),
                "author": story.get("author-name", "Unknown"),
            })

    else:
        news_list = []

    return render(request, 'news/home.html', {"news": news_list})