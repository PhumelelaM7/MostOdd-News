"""
Database models for the MostOdd News application.
"""


# Import Django's database models
from django.db import models

# Import AbstractUser so we can extend Django's default User model
from django.contrib.auth.models import AbstractUser


# ------------------------------------
# Custom User Model
# ------------------------------------
class CustomUser(AbstractUser):
    """
    Custom user model for the MostOdd News application.
    """

    # ------------------------------------
    # Available user roles
    # ------------------------------------
    ROLE_CHOICES = [
        ("reader", "Reader"),
        ("journalist", "Journalist"),
        ("editor", "Editor"),
    ]

    # Store the user's role
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="reader",
    )

    # ------------------------------------
    # Reader subscriptions
    # ------------------------------------

    # Publishers that a reader follows
    subscribed_publishers = models.ManyToManyField(
        "Publisher",
        blank=True,
        related_name="subscribers",
    )

    # Journalists that a reader follows
    subscribed_journalists = models.ManyToManyField(
        "self",
        blank=True,
        symmetrical=False,
        limit_choices_to={"role": "journalist"},
        related_name="journalist_subscribers",
    )

    # ------------------------------------
    # Save the user
    # ------------------------------------
    def save(self, *args, **kwargs):
        """
        Save the user.

        If the user is not a Reader,
        remove all reader subscriptions
        so that only Readers may subscribe
        to Publishers and Journalists.
        """

        # Save the user first
        super().save(*args, **kwargs)

        # Only Readers may keep subscriptions
        if self.role != "reader":

            # Remove Publisher subscriptions
            self.subscribed_publishers.clear()

            # Remove Journalist subscriptions
            self.subscribed_journalists.clear()


# ---------------------------------------------------------
# Publisher model
# ---------------------------------------------------------
class Publisher(models.Model):
    """
    Represents a news publisher.

    A publisher can have multiple journalists and editors.
    Journalists create articles and editors approve articles.
    """

    # Publisher name
    name = models.CharField(
        max_length=100
    )

    # Publisher description
    description = models.TextField()

    # Users with journalist role linked to this publisher
    journalists = models.ManyToManyField(
        CustomUser,
        related_name="publisher_journalists",
        limit_choices_to={
            "role": "journalist"
        },
        blank=True,
    )

    # Users with editor role linked to this publisher
    editors = models.ManyToManyField(
        CustomUser,
        related_name="publisher_editors",
        limit_choices_to={
            "role": "editor"
        },
        blank=True,
    )

    def __str__(self):
        return self.name


# ------------------------------------
# Article Model
# ------------------------------------
class Article(models.Model):
    """
    Represents a news article.

    Articles are written by journalists and may optionally belong
    to a publisher. Editors will review and approve articles before
    they become publicly available.
    """

    # Article headline
    title = models.CharField(max_length=200)

    # Main article body
    content = models.TextField()

    # Journalist who wrote the article
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="articles"
    )

    # Publisher that owns the article.
    # Blank/Null allows independent journalists to publish.
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="articles"
    )

    # Date and time the article was created
    created_at = models.DateTimeField(auto_now_add=True)

    # Editors change this to True when approving an article
    approved = models.BooleanField(default=False)

    class Meta:
        """ Meta options for the Article model. """

        # Display newest articles first
        ordering = ["-created_at"]

        # Improve naming in Django Admin
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    # Display the article title in the admin panel
    def __str__(self):
        return self.title


# ------------------------------------
# Newsletter Model
# ------------------------------------
class Newsletter(models.Model):
    """
    Represents a curated newsletter.

    A newsletter is created by a journalist and contains
    one or more published articles.
    """

    # Newsletter title
    title = models.CharField(max_length=200)

    # Short description of the newsletter
    description = models.TextField()

    # Journalist who created the newsletter
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="newsletters"
    )

    # Articles included in this newsletter
    articles = models.ManyToManyField(
        Article,
        related_name="newsletters",
        blank=True
    )

    # Date and time the newsletter was created
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """ Meta options for the Newsletter model.
        """

        # Show newest newsletters first
        ordering = ["-created_at"]

        # Friendly names for the Django Admin
        verbose_name = "Newsletter"
        verbose_name_plural = "Newsletters"

    # Display the newsletter title
    def __str__(self):
        return self.title


# ------------------------------------
# Approved Article Log Model
# ------------------------------------
class ApprovedArticleLog(models.Model):
    """
    Stores a record whenever an article
    is approved by an editor.
    """

    # Original article reference
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="approval_logs"
    )

    # Article title at approval time
    title = models.CharField(
        max_length=200
    )

    # User who approved the article
    approved_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="approved_articles"
    )

    # Approval timestamp
    approved_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title
