"""
Forms used throughout the MostOdd News application.
"""


# Import Django forms
from django import forms

# Import Django's password validation helper
from django.contrib.auth.forms import UserCreationForm

# Import our custom user model
from .models import (
    Article,
    CustomUser,
    Newsletter,
    Publisher,
)


class RegistrationForm(UserCreationForm):
    """
    Allows new users to create an account.

    Users select their role during registration.
    The post_save signal will automatically assign
    the correct Django Group.
    """

    class Meta:
        """Meta options for the RegistrationForm."""

        # Use our CustomUser model
        model = CustomUser

        # Fields displayed on the registration page
        fields = [
            "username",
            "email",
            "role",
            "password1",
            "password2",
        ]

    # ---------------------------------------------------------
    # Validate Email Address
    # ---------------------------------------------------------
    def clean_email(self):
        """
        Prevent users from registering with an email
        address that already exists.
        """

        # Get the email entered by the user
        email = self.cleaned_data.get("email")

        # Check whether another account already uses this email
        if CustomUser.objects.filter(email=email).exists():

            # Display a validation error if the email already exists
            raise forms.ValidationError(
                "An account with this email address already exists."
            )

        # Return the validated email address
        return email


# ---------------------------------------------------------
# Article Form
# ---------------------------------------------------------
class ArticleForm(forms.ModelForm):
    """
    Form used by journalists and editors
    to create or edit news articles.
    """

    class Meta:
        """ Meta options for the RegistrationForm. """

        # Use the Article model
        model = Article

        # Fields shown on the HTML form
        fields = [
            "title",
            "content",
            "publisher",
        ]


# ---------------------------------------------------------
# Newsletter Form
# ---------------------------------------------------------
class NewsletterForm(forms.ModelForm):
    """
    Form for creating and editing newsletters.
    """

    class Meta:
        """ Meta options for the News Letter. """

        # Use the Newsletter model
        model = Newsletter

        # Fields displayed on the form
        fields = [
            "title",
            "description",
            "articles",
        ]

    # ---------------------------------------------------------
    # Initialise the newsletter form
    # ---------------------------------------------------------
    def __init__(self, *args, **kwargs):
        """
        Only approved articles can be selected
        when creating or editing a newsletter.
        """

        # Initialise the parent ModelForm
        super().__init__(*args, **kwargs)

        # Only show approved articles
        self.fields["articles"].queryset = (
            Article.objects.filter(
                approved=True
            )
        )


# ---------------------------------------------------------
# Publisher Form 
# ---------------------------------------------------------
class PublisherForm(forms.ModelForm):
    """
    Form for creating and editing publishers.
    """

    class Meta:
        """ Meta options for the PublisherForm. """

        # Use the Publisher model
        model = Publisher

        # Fields displayed on the form
        fields = [
            "name",
            "description",
            "journalists",
            "editors",
        ]
