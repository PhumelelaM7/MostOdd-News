"""
Admin configuration for the MostOdd News application.
"""


# Import Django admin
from django.contrib import admin

# Import Django's built-in UserAdmin
from django.contrib.auth.admin import UserAdmin

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
admin.site.register(Publisher)
admin.site.register(ApprovedArticleLog)


# ---------------------------------------------------------
# Custom User Admin
# ---------------------------------------------------------
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Custom admin for the CustomUser model.
    """

    # Display these columns
    list_display = (
        "username",
        "email",
        "role",
        "is_staff",
        "is_active",
    )

    # Allow filtering
    list_filter = (
        "role",
        "is_staff",
        "is_active",
    )

    # Add the custom role and subscriptions
    fieldsets = UserAdmin.fieldsets + (
        (
            "MostOdd News",
            {
                "fields": (
                    "role",
                    "subscribed_publishers",
                    "subscribed_journalists",
                ),
            },
        ),
    )

    # Show these fields when creating a new user
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            None,
            {
                "fields": (
                    "role",
                ),
            },
        ),
    )

    # Search fields
    search_fields = (
        "username",
        "email",
    )

    # ---------------------------------------------------------
    # Display role-specific fields
    # ---------------------------------------------------------
    def get_fieldsets(self, request, obj=None):
        """
        Only Readers should see the subscription fields.
        """

        # Start with the default fieldsets
        fieldsets = list(super().get_fieldsets(request, obj))

        # New user being created
        if obj is None:
            return fieldsets

        # Hide reader-only fields for non-readers
        if obj.role != "reader":

            updated_fieldsets = []

            for title, options in fieldsets:

                fields = list(options.get("fields", ()))

                fields = [
                    field
                    for field in fields
                    if field not in (
                        "subscribed_publishers",
                        "subscribed_journalists",
                    )
                ]

                updated_fieldsets.append(
                    (
                        title,
                        {
                            **options,
                            "fields": tuple(fields),
                        },
                    )
                )

            return updated_fieldsets

        return fieldsets

    # ---------------------------------------------------------
    # Save related objects
    # ---------------------------------------------------------
    def save_related(self, request, form, formsets, change):
        """
        After Django saves the ManyToMany fields,
        remove subscriptions for non-readers.
        """

        # Save the related objects first
        super().save_related(
            request,
            form,
            formsets,
            change,
        )

        # Get the saved user
        user = form.instance

        # Only Readers may keep subscriptions
        if user.role != "reader":

            # Remove Publisher subscriptions
            user.subscribed_publishers.clear()

            # Remove Journalist subscriptions
            user.subscribed_journalists.clear()
    

    # ------------------------------------
    # Save related objects
    # ------------------------------------
    def save_related(self, request, form, formsets, change):
        """
        After Django saves the ManyToMany fields,
        remove subscriptions for non-readers.
        """

        super().save_related(request, form, formsets, change)

        user = form.instance

        if user.role != "reader":
            user.subscribed_publishers.clear()
            user.subscribed_journalists.clear()


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
