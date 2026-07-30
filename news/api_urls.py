# Import Django path function
from django.urls import path

# Import application views
from . import views

# Import API views
from .views import (
    ArticleListAPIView,
    ArticleDetailAPIView,
    SubscribedArticlesAPIView,
    NewsletterListAPIView,
    NewsletterDetailAPIView,
)


# ---------------------------------------------------------
# API URL Patterns
# ---------------------------------------------------------
urlpatterns = [

    # List all approved articles
    # Create a new article
    path(
        "articles/",
        ArticleListAPIView.as_view(),
        name="api_articles",
    ),

    # Retrieve a single approved article
    path(
        "articles/<int:pk>/",
        ArticleDetailAPIView.as_view(),
        name="api_article_detail",
    ),

    # List approved articles from subscriptions
    path(
        "articles/subscribed/",
        SubscribedArticlesAPIView.as_view(),
        name="subscribed_articles",
    ),

    # List and create newsletters
    path(
        "newsletters/",
        NewsletterListAPIView.as_view(),
        name="newsletter-list"
    ),

    # Retrieve, update, and delete a single newsletter
    path(
        "newsletters/<int:pk>/",
        NewsletterDetailAPIView.as_view(),
        name="newsletter-detail"
    ),

    # List and create approved article logs
    path(
        "approved/",
        views.ApprovedArticleLogAPIView.as_view(),
        name="approved-articles",
    ),
]


