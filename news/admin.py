"""
Admin configuration for the MostOdd News application.
"""


# Import Django's admin module
from django.contrib import admin

# Import application models
from .models import (
    CustomUser,
    Publisher,
    Article,
    Newsletter,
    ApprovedArticleLog,

)

# ---------------------------------------------------------
# Register models without custom admin configuration
# ---------------------------------------------------------
admin.site.register(CustomUser)
admin.site.register(Publisher)
admin.site.register(ApprovedArticleLog)

# ---------------------------------------------------------
# Article Admin
# ---------------------------------------------------------


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """
    Configure how articles appear in the Django Admin.
    """

    # Display these fields in the article list
    list_display = (
        "title",
        "author",
        "publisher",
        "approved",
        "created_at",
    )

    # Allow filtering by approval status and publisher
    list_filter = (
        "approved",
        "publisher",
    )

    # Add a search bar
    search_fields = (
        "title",
        "content",
    )


# ---------------------------------------------------------
# Newsletter Admin
# ---------------------------------------------------------
@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    """
    Configure how newsletters appear in the Django Admin.
    """

    # Display these columns
    list_display = (
        "title",
        "author",
        "created_at",
    )

    # Enable searching
    search_fields = (
        "title",
        "description",
    )

    # Allow filtering by creation date
    list_filter = (
        "created_at",
    )

    # Improve the article selection interface
    filter_horizontal = (
        "articles",
    )
