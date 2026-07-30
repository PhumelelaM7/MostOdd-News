"""
Views for the MostOdd News application.

Contains standard Django views and REST API views for
user registration, article management, newsletters,
and article approval.
"""

# Third-party imports
import requests

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db import models
from django.http import HttpResponseForbidden
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.contrib import messages
from django.core.mail import send_mail

from rest_framework import generics
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly
)

# Local application imports
from .forms import (
    ArticleForm,
    NewsletterForm,
    PublisherForm,
    RegistrationForm,
)
from .models import (
    Article,
    Newsletter,
    CustomUser,
    Publisher,
    ApprovedArticleLog,
)
from .permissions import (
    IsJournalistOrEditorOrReadOnly,
    IsArticleRolePermission,
)
from .serializers import (
    ApprovedArticleLogSerializer,
    ArticleSerializer,
    NewsletterSerializer,
)


# ---------------------------------------------------------
# Display all articles waiting for editor approval
# ---------------------------------------------------------
@login_required
def pending_articles(request):
    """
    Display all articles that have not yet been approved.
    Only Editors are allowed to access this page.
    """

    # Allow access for superusers, users with the Editor role,
    # or users who belong to the Editor group.
    if not (
        request.user.is_superuser
        or request.user.role == "editor"
        or request.user.groups.filter(name="Editor").exists()
    ):
        return HttpResponseForbidden("Access denied.")

    # Retrieve all unapproved articles
    articles = Article.objects.filter(approved=False)

    # Render the template with the list of pending articles
    return render(
        request,
        "news/pending_articles.html",
        {
            "articles": articles,
        },
    )


# ---------------------------------------------------------
# Approve an article
# ---------------------------------------------------------
@login_required
def approve_article(request, article_id):
    """
    Allow an Editor to approve an article.
    """

    # Allow access for superusers, users with the Editor role,
    # or users who belong to the Editor group.
    if not (
        request.user.is_superuser
        or request.user.role == "editor"
        or request.user.groups.filter(name="Editor").exists()
    ):
        return HttpResponseForbidden("Access denied.")

    # Retrieve the selected article
    article = get_object_or_404(
        Article,
        id=article_id,
    )

    # Check whether the editor clicked the Approve button
    if request.method == "POST":

        # Mark the article as approved
        article.approved = True

        # Save the updated article
        article.save()

        # ---------------------------------------------------------
        # Send approved article information to internal API
        # This records the approval through REST API
        # ---------------------------------------------------------
        try:

            # Send POST request to our own API endpoint
            response = requests.post(
                "http://127.0.0.1:8000/api/approved/",
                json={

                    # Approved article ID
                    "article": article.id,

                    # Article title for logging
                    "title": article.title,

                    # Editor who approved the article
                    "approved_by": request.user.id,
                },

                # Stop request hanging indefinitely
                timeout=5,
            )

            # Display API response during development
            print(
                "Approved article log response:",
                response.status_code
            )

        except requests.exceptions.RequestException as error:

            # Handle API connection problems safely
            print(
                "Approved article logging failed:",
                error
            )

        # ---------------------------------------------------------
        # Retrieve publisher subscribers
        # ---------------------------------------------------------
        publisher_subscribers = CustomUser.objects.none()

        # Only retrieve publisher subscribers when
        # the article belongs to a publisher
        if article.publisher:

            publisher_subscribers = CustomUser.objects.filter(
                subscribed_publishers=article.publisher
            )

        # ---------------------------------------------------------
        # Retrieve journalist subscribers
        # ---------------------------------------------------------
        journalist_subscribers = CustomUser.objects.filter(
            subscribed_journalists=article.author
        )

        # ---------------------------------------------------------
        # Combine both subscriber lists
        # ---------------------------------------------------------
        subscribers = (
            publisher_subscribers |
            journalist_subscribers
        ).distinct()

        # ---------------------------------------------------------
        # Send an email notification to each subscriber
        # ---------------------------------------------------------
        for subscriber in subscribers:

            # Skip users who do not have an email address
            if not subscriber.email:
                continue

            # Display publisher name when available
            if article.publisher:
                publisher_name = article.publisher.name
            else:
                publisher_name = "Independent Journalist"

            # Send the email notification
            send_mail(

                # Email subject
                subject=f"New Article Approved: {article.title}",

                # Email message sent to subscribers
                message=(
                    f"Hello {subscriber.username},\n\n"
                    "Great news! A new article has just been "
                    "approved.\n\n"
                    f"Title: {article.title}\n"
                    f"Author: {article.author.username}\n"
                    f"Publisher: {publisher_name}\n\n"
                    "Log in to the News Application to read the "
                    "full article.\n\n"
                    "Thank you for using the News Application!"
                ),

                # Sender email
                from_email=None,

                # Recipient email
                recipient_list=[subscriber.email],

                # Raise any email errors during development
                fail_silently=False,
            )

        # Redirect back to the pending articles page
        return redirect("pending_articles")

    # Display the approval page
    return render(
        request,
        "news/approve_article.html",
        {
            "article": article,
        },
    )


# ---------------------------------------------------------
# API - List all approved articles
# ---------------------------------------------------------
class ArticleListAPIView(generics.ListCreateAPIView):
    """
    API endpoint for viewing all approved articles
    and creating new articles.
    """

    # Only approved articles are returned
    queryset = Article.objects.filter(approved=True)

    # Serializer used by this endpoint
    serializer_class = ArticleSerializer

    # Anyone can read, authenticated users can create
    permission_classes = [
    IsArticleRolePermission,
]


# ---------------------------------------------------------
# API - Retrieve, Update and Delete a single Article
# ---------------------------------------------------------
class ArticleDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating
    and deleting a single article.
    """

    # Only approved articles can be retrieved
    queryset = Article.objects.filter(approved=True)

    # Serializer used by this endpoint
    serializer_class = ArticleSerializer

    # Read for everyone, edit for authenticated users
    permission_classes = [
    IsArticleRolePermission,
]


# ---------------------------------------------------------
# API - Articles from subscriptions
# ---------------------------------------------------------
class SubscribedArticlesAPIView(generics.ListAPIView):
    """
    Return approved articles from publishers
    and journalists that the logged-in reader
    subscribes to.
    """

    serializer_class = ArticleSerializer

    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]

    def get_queryset(self):
        """
        Return approved articles from the current
        user's subscriptions.
        """

        # Get the logged-in user
        user = self.request.user

        # User must be authenticated
        if not user.is_authenticated:
            return Article.objects.none()

        # Get subscribed publishers
        publishers = user.subscribed_publishers.all()

        # Get subscribed journalists
        journalists = user.subscribed_journalists.all()

        # Return approved articles matching either subscription
        return Article.objects.filter(
            approved=True,
        ).filter(
            models.Q(publisher__in=publishers) |
            models.Q(author__in=journalists)
        ).distinct()


# ---------------------------------------------------------
# API - Newsletter List and Create
# ---------------------------------------------------------
class NewsletterListAPIView(generics.ListCreateAPIView):
    """
    API endpoint for viewing newsletters
    and creating new newsletters.
    """

    # Return all newsletters
    queryset = Newsletter.objects.all()

    # Convert newsletters to JSON
    serializer_class = NewsletterSerializer

    # Readers can view.
    # Journalists and Editors can create.
    permission_classes = [
        IsJournalistOrEditorOrReadOnly,
    ]


# ---------------------------------------------------------
# API - Newsletter Detail
# ---------------------------------------------------------
class NewsletterDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for viewing, updating,
    and deleting a single newsletter.
    """

    # Work with all newsletters
    queryset = Newsletter.objects.all()

    # Convert newsletter data into JSON
    serializer_class = NewsletterSerializer

    # Readers can view.
    # Journalists and Editors can edit.
    permission_classes = [
        IsJournalistOrEditorOrReadOnly,
    ]


# ---------------------------------------------------------
# Approved Article Log API
# Allows viewing and creating approval records.
# ---------------------------------------------------------

class ApprovedArticleLogAPIView(generics.ListCreateAPIView):
    """
    API endpoint for viewing and creating
    approved article log records.
    """

    # Retrieve all approved article logs
    queryset = ApprovedArticleLog.objects.all()

    # Convert approved logs into JSON
    serializer_class = ApprovedArticleLogSerializer

    # Only authenticated users can access this endpoint
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]


# ---------------------------------------------------------
# Landing page
# ---------------------------------------------------------
def home(request):
    """
    Displays the application landing page.
    """

    return render(
        request,
        "news/home.html"
    )


# ---------------------------------------------------------
# User Registration View
# ---------------------------------------------------------
def register(request):
    """
    Allows new users to create an account.

    The user's role is selected during registration.
    The CustomUser post_save signal will automatically
    assign the correct Django Group.
    """

    # Check if the form was submitted
    if request.method == "POST":

        # Create form using submitted data
        form = RegistrationForm(request.POST)

        # Validate the form
        if form.is_valid():

            # Save the new user
            user = form.save()

            # Log the user in automatically after registration
            login(request, user)

            # Redirect user to homepage
            return redirect("home")

    else:

        # Display an empty registration form
        form = RegistrationForm()

    # Display registration page
    return render(
        request,
        "news/register.html",
        {
            "form": form
        }
    )


# ---------------------------------------------------------
# Display all approved articles
# ---------------------------------------------------------
def article_list(request):
    """
    Display all approved news articles.

    Readers can browse published articles
    from this page.
    """

    # Retrieve only approved articles
    articles = Article.objects.filter(approved=True)

    # Display the article list template
    return render(
        request,
        "news/article_list.html",
        {
            "articles": articles,
        },
    )


# ---------------------------------------------------------
# Display a single approved article
# ---------------------------------------------------------
def article_detail(request, article_id):
    """
    Display the full details of a single approved article.
    """

    # Retrieve the requested approved article.
    # Return a 404 page if it does not exist.
    article = get_object_or_404(
        Article,
        id=article_id,
        approved=True,
    )

    # Render the article detail template
    return render(
        request,
        "news/article_detail.html",
        {
            "article": article,
        },
    )


# ---------------------------------------------------------
# Create a new article
# ---------------------------------------------------------
@login_required
def article_create(request):
    """
    Allow journalists to create a new article.
    Superusers may also create articles.
    """

    # Only journalists, editors and superusers may create articles
    if not (
        request.user.is_superuser
        or request.user.role == "journalist"
    ):
        return HttpResponseForbidden(
            "You do not have permission to create articles."
        )

    # Check whether the form was submitted
    if request.method == "POST":

        # Populate the form with submitted data
        form = ArticleForm(request.POST)

        # Validate the submitted data
        if form.is_valid():

            # Create the article without saving yet
            article = form.save(commit=False)

            # Automatically assign the logged-in user
            article.author = request.user

            # New articles require editor approval
            article.approved = False

            # Save the article
            article.save()

            # Return to the article list
            return redirect("article_list")

    else:

        # Display an empty form
        form = ArticleForm()

    # Display the article creation page
    return render(
        request,
        "news/article_form.html",
        {
            "form": form,
            "page_title": "Create Article",
        },
    )


# ---------------------------------------------------------
# Edit an existing article
# ---------------------------------------------------------
@login_required
def article_update(request, article_id):
    """
    Allow journalists and editors to edit an article.
    """

    # Retrieve the selected article
    article = get_object_or_404(
        Article,
        id=article_id,
    )

    # Only the article author, an editor or a superuser may edit
    if not (
        request.user.is_superuser
        or request.user.role == "editor"
        or article.author == request.user
    ):
        return HttpResponseForbidden(
            "You do not have permission to edit this article."
        )

    # Check whether the form was submitted
    if request.method == "POST":

        # Populate the form with the submitted data
        form = ArticleForm(
            request.POST,
            instance=article,
        )

        # Validate the form
        if form.is_valid():

            # Save the updated article
            form.save()

            # Return to the article list
            return redirect("article_list")

    else:

        # Display the form with the current article data
        form = ArticleForm(instance=article)

    # Display the article form
    return render(
        request,
        "news/article_form.html",
        {
            "form": form,
            "page_title": "Edit Article",
        },
    )


# ---------------------------------------------------------
# Delete an existing article
# ---------------------------------------------------------
@login_required
def article_delete(request, article_id):
    """
    Allow the author, an editor or a superuser
    to delete an article.
    """

    # Retrieve the selected article
    article = get_object_or_404(
        Article,
        id=article_id,
    )

    # Check whether the user has permission
    if not (
        request.user.is_superuser
        or request.user.role == "editor"
        or article.author == request.user
    ):
        return HttpResponseForbidden(
            "You do not have permission to delete this article."
        )

    # Delete the article after confirmation
    if request.method == "POST":

        # Remove the article from the database
        article.delete()

        # Return to the article list
        return redirect("article_list")

    # Display the confirmation page
    return render(
        request,
        "news/article_confirm_delete.html",
        {
            "article": article,
        },
    )


# ---------------------------------------------------------
# Display all newsletters
# ---------------------------------------------------------
@login_required
def newsletter_list(request):
    """
    Display all newsletters.
    """

    # Retrieve every newsletter
    newsletters = Newsletter.objects.all()

    # Display the newsletter list page
    return render(
        request,
        "news/newsletter_list.html",
        {
            "newsletters": newsletters,
        },
    )


# ---------------------------------------------------------
# Display a single newsletter
# ---------------------------------------------------------
def newsletter_detail(request, newsletter_id):
    """
    Display the details of a single newsletter.
    """

    # Retrieve the selected newsletter
    newsletter = get_object_or_404(
        Newsletter,
        id=newsletter_id,
    )

    # Display the newsletter detail page
    return render(
        request,
        "news/newsletter_detail.html",
        {
            "newsletter": newsletter,
        },
    )


# ---------------------------------------------------------
# Create a new newsletter
# ---------------------------------------------------------
@login_required
def newsletter_create(request):
    """
    Allow journalists and editors
    to create a new newsletter.
    """

    # Only journalists, and superusers
    # may create newsletters.
    if not (
        request.user.is_superuser
        or request.user.role in ["journalist", "editor"]
    ):
        return HttpResponseForbidden(
            "You do not have permission to create newsletters."
        )

    # Check whether the form was submitted
    if request.method == "POST":

        # Populate the form with submitted data
        form = NewsletterForm(request.POST)

        # Validate the submitted data
        if form.is_valid():

            # Create the newsletter without saving yet
            newsletter = form.save(commit=False)

            # Automatically assign the logged-in user
            newsletter.author = request.user

            # Save the newsletter
            newsletter.save()

            # Save the selected articles
            form.save_m2m()

            # Return to the newsletter list
            return redirect("newsletter_list")

    else:

        # Display an empty form
        form = NewsletterForm()

    # Display the newsletter creation page
    return render(
        request,
        "news/newsletter_form.html",
        {
            "form": form,
            "page_title": "Create Newsletter",
        },
    )


# ---------------------------------------------------------
# Edit a newsletter
# ---------------------------------------------------------
@login_required
def newsletter_update(request, newsletter_id):
    """
    Edit a newsletter.
    """

    # Retrieve the selected newsletter
    newsletter = get_object_or_404(
        Newsletter,
        id=newsletter_id,
    )

    # Allow only the author, editors or superusers
    if not (
        request.user == newsletter.author
        or request.user.role == "editor"
        or request.user.is_superuser
    ):
        return HttpResponseForbidden(
            "Access denied."
        )

    # Check whether the form was submitted
    if request.method == "POST":

        # Populate the form with submitted data
        form = NewsletterForm(
            request.POST,
            instance=newsletter,
        )

        # Validate the form
        if form.is_valid():

            # Save the updated newsletter
            form.save()

            # Return to the newsletter list
            return redirect(
                "newsletter_list"
            )

    else:

        # Display the existing newsletter
        form = NewsletterForm(
            instance=newsletter,
        )

    # Display the newsletter form
    return render(
        request,
        "news/newsletter_form.html",
        {
            "form": form,
            "page_title": "Edit Newsletter",
        },
    )


# ---------------------------------------------------------
# Delete a newsletter
# ---------------------------------------------------------
@login_required
def newsletter_delete(request, newsletter_id):
    """
    Delete a newsletter.
    """

    # Retrieve the selected newsletter
    newsletter = get_object_or_404(
        Newsletter,
        id=newsletter_id,
    )

    # Allow only the author, editors or superusers
    if not (
        request.user == newsletter.author
        or request.user.role == "editor"
        or request.user.is_superuser
    ):
        return HttpResponseForbidden(
            "Access denied."
        )

    # Check whether the user confirmed deletion
    if request.method == "POST":

        # Delete the newsletter
        newsletter.delete()

        # Return to the newsletter list
        return redirect(
            "newsletter_list"
        )

    # Display the confirmation page
    return render(
        request,
        "news/newsletter_confirm_delete.html",
        {
            "newsletter": newsletter,
        },
    )


# ---------------------------------------------------------
# Create a publisher
# ---------------------------------------------------------
@login_required
def publisher_create(request):
    """
    Allow Editors to create publishers.
    """

    # Allow access for superusers and editors only
    if not (
        request.user.is_superuser
        or request.user.role == "editor"
        or request.user.groups.filter(
            name="Editor"
        ).exists()
    ):
        return HttpResponseForbidden(
            "Access denied."
        )

    # Check whether the form was submitted
    if request.method == "POST":

        # Populate the form with submitted data
        form = PublisherForm(request.POST)

        # Validate the submitted form
        if form.is_valid():

            # Save the publisher
            form.save()

            # Return to the article list
            return redirect("article_list")

    else:

        # Display an empty form
        form = PublisherForm()

    # Display the publisher form
    return render(
        request,
        "news/publisher_form.html",
        {
            "form": form,
            "page_title": "Create Publisher",
        },
    )


# ---------------------------------------------------------
# Subscribe to a publisher
# ---------------------------------------------------------
@login_required
def subscribe_publisher(request, publisher_id):
    """
    Allow a Reader to subscribe to a publisher.
    """

    # Only Readers may subscribe
    if request.user.role != "reader":
        return HttpResponseForbidden("Access denied.")

    # Retrieve the selected publisher
    publisher = get_object_or_404(
        Publisher,
        id=publisher_id,
    )

    # Save the subscription
    request.user.subscribed_publishers.add(
        publisher
    )

    # Display a confirmation message
    messages.success(
        request,
        f"You have successfully subscribed to publisher "
        f"{publisher.name}."
    )

    # Send a confirmation email
    if request.user.email:

        send_mail(

            # Email subject
            subject="Publisher Subscription Confirmed",

            # Email body
            message=(
                f"Hello {request.user.username},\n\n"
                f"You have successfully subscribed to publisher "
                f"{publisher.name}.\n\n"
                "You will now receive notifications whenever "
                "new approved articles are published by this "
                "publisher.\n\n"
                "Thank you for using MostOdd News!"
            ),

            # Sender email
            from_email=None,

            # Recipient email
            recipient_list=[request.user.email],

            # Raise email errors during development
            fail_silently=False,
        )

    # Return to the previous page
    return redirect(
        request.META.get(
            "HTTP_REFERER",
            "article_list",
        )
    )


# ---------------------------------------------------------
# Subscribe to a journalist
# ---------------------------------------------------------
@login_required
def subscribe_journalist(request, journalist_id):
    """
    Allow a Reader to subscribe to a journalist.
    """

    # Only Readers may subscribe
    if request.user.role != "reader":
        return HttpResponseForbidden("Access denied.")

    # Retrieve the selected journalist
    journalist = get_object_or_404(
        CustomUser,
        id=journalist_id,
        role="journalist",
    )

    # Save the subscription
    request.user.subscribed_journalists.add(
        journalist
    )

    # Display a confirmation message
    messages.success(
        request,
        f"You have successfully subscribed to journalist "
        f"{journalist.username}."
    )

    # Send a confirmation email
    if request.user.email:

        send_mail(

            # Email subject
            subject="Journalist Subscription Confirmed",

            # Email body
            message=(
                f"Hello {request.user.username},\n\n"
                f"You have successfully subscribed to "
                f"{journalist.username}.\n\n"
                "You will now receive notifications whenever "
                "their approved articles are published.\n\n"
                "Thank you for using MostOdd News!"
            ),

            # Sender email
            from_email=None,

            # Recipient email
            recipient_list=[request.user.email],

            # Raise email errors during development
            fail_silently=False,
        )

    # Return to the previous page
    return redirect(
        request.META.get(
            "HTTP_REFERER",
            "article_list",
        )
    )
