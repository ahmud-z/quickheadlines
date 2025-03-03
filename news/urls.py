from django.urls import path
from .views import fetch_news

urlpatterns = [
    path('', fetch_news, name='home'),
    path('<str:category>/', fetch_news, name='category_news'),
]
