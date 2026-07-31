"""
URL configuration for the News application.
"""


# Import Django's path function
from django.urls import path

# Import application views
from . import views


# URL patterns for the News application
urlpatterns = [

    # User registration page
    path(
        "register/",
        views.register,
        name="register"
    ),

    # Display articles awaiting approval
    path(
        "pending/",
        views.pending_articles,
        name="pending_articles",
    ),

    # Approve an individual article
    path(
        "approve/<int:article_id>/",
        views.approve_article,
        name="approve_article",
    ),

    # Display all approved articles
    path(
        "articles/",
        views.article_list,
        name="article_list",
    ),

    # Display a single article
    path(
        "articles/<int:article_id>/",
        views.article_detail,
        name="article_detail",
    ),

    # Create a new article
    path(
        "articles/create/",
        views.article_create,
        name="article_create",
    ),

    # Edit an existing article
    path(
        "articles/<int:article_id>/edit/",
        views.article_update,
        name="article_update",
    ),

    # Delete an article
    path(
        "articles/<int:article_id>/delete/",
        views.article_delete,
        name="article_delete",
    ),

    # Display all newsletters
    path(
        "newsletters/",
        views.newsletter_list,
        name="newsletter_list",
    ),

    # Display a single newsletter
    path(
        "newsletters/<int:newsletter_id>/",
        views.newsletter_detail,
        name="newsletter_detail",
    ),

    # Create a new newsletter
    path(
        "newsletters/create/",
        views.newsletter_create,
        name="newsletter_create",
    ),

    # Edit an existing newsletter
    path(
        "newsletters/<int:newsletter_id>/edit/",
        views.newsletter_update,
        name="newsletter_update",
    ),

    # Delete a newsletter
    path(
        "newsletters/<int:newsletter_id>/delete/",
        views.newsletter_delete,
        name="newsletter_delete",
    ),

    # View all publishers
    path(
        "publishers/",
        views.publisher_list,
        name="publisher_list",
    ),

    # Create a new publisher
    path(
        "publishers/create/",
        views.publisher_create,
        name="publisher_create",
    ),

    # Subscribe to a publisher
    path(
        "publishers/<int:publisher_id>/subscribe/",
        views.subscribe_publisher,
        name="subscribe_publisher",
    ),

    # Subscribe to a journalist
    path(
        "journalists/<int:journalist_id>/subscribe/",
        views.subscribe_journalist,
        name="subscribe_journalist",
    ),
]
