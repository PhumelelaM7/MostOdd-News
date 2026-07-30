# Import Django's base command class
from django.core.management.base import BaseCommand

# Import Django's Group and Permission models
from django.contrib.auth.models import Group, Permission

# Import the ContentType model
from django.contrib.contenttypes.models import ContentType

# Import application models
from news.models import Article, Newsletter


class Command(BaseCommand):
    """
    Create the default user groups and assign the
    required permissions for the News Application.
    """

    help = "Creates the Reader, Journalist and Editor groups."

    def handle(self, *args, **kwargs):

        # ------------------------------------
        # Create the groups
        # ------------------------------------
        reader_group, _ = Group.objects.get_or_create(name="Reader")
        journalist_group, _ = Group.objects.get_or_create(name="Journalist")
        editor_group, _ = Group.objects.get_or_create(name="Editor")

        # ------------------------------------
        # Get content types
        # ------------------------------------
        article_type = ContentType.objects.get_for_model(Article)
        newsletter_type = ContentType.objects.get_for_model(Newsletter)

        # ------------------------------------
        # Reader permissions
        # Can only view articles and newsletters
        # ------------------------------------
        reader_permissions = Permission.objects.filter(
            content_type__in=[article_type, newsletter_type],
            codename__in=[
                "view_article",
                "view_newsletter",
            ]
        )

        reader_group.permissions.set(reader_permissions)

        # ------------------------------------
        # Journalist permissions
        # Create, view, update and delete
        # ------------------------------------
        journalist_permissions = Permission.objects.filter(
            content_type__in=[article_type, newsletter_type],
            codename__in=[
                "add_article",
                "change_article",
                "delete_article",
                "view_article",
                "add_newsletter",
                "change_newsletter",
                "delete_newsletter",
                "view_newsletter",
            ]
        )

        journalist_group.permissions.set(journalist_permissions)

        # ------------------------------------
        # Editor permissions
        # View, update and delete
        # ------------------------------------
        editor_permissions = Permission.objects.filter(
            content_type__in=[article_type, newsletter_type],
            codename__in=[
                "change_article",
                "delete_article",
                "view_article",
                "change_newsletter",
                "delete_newsletter",
                "view_newsletter",
            ]
        )

        editor_group.permissions.set(editor_permissions)

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully created groups and assigned permissions."
            )
        )