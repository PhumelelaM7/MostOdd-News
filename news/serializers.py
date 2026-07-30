""" Serializers for the MostOdd News application. """


# Import Django REST Framework serializers
from rest_framework import serializers

# Import application models
from .models import (
    Article,
    Publisher,
    Newsletter,
    CustomUser,
    ApprovedArticleLog,
)


# ---------------------------------------------------------
# Article Serializer
# ---------------------------------------------------------
class ArticleSerializer(serializers.ModelSerializer):
    """
    Converts Article objects to and from JSON.
    """

    class Meta:
        """
        Meta options for the ArticleSerializer.
        """

        model = Article

        fields = [
            "id",
            "title",
            "content",
            "author",
            "publisher",
            "created_at",
            "approved",
        ]

        # These fields are controlled by the system
        read_only_fields = [
            "id",
            "author",
            "created_at",
            "approved",
        ]

    def create(self, validated_data):

        # Automatically assign logged-in user as author
        validated_data["author"] = self.context["request"].user

        # New articles require editor approval
        validated_data["approved"] = False

        return Article.objects.create(**validated_data)


# ---------------------------------------------------------
# Newsletter Serializer
# ---------------------------------------------------------


class NewsletterSerializer(serializers.ModelSerializer):
    """
    Converts Newsletter model data into JSON
    and validates incoming newsletter data.
    """

    class Meta:
        """
        Meta options for the NewsletterSerializer.
        """

        # Model being converted
        model = Newsletter

        # Fields exposed through the API
        fields = [
            "id",
            "title",
            "description",
            "author",
            "articles",
            "created_at",
        ]

        # Automatically controlled fields
        read_only_fields = [
            "id",
            "author",
            "created_at",
        ]

    def create(self, validated_data):
        """ Create a new newsletter instance. """

        # Remove many-to-many data temporarily
        articles = validated_data.pop("articles", [])

        # Assign logged-in user as author
        validated_data["author"] = self.context["request"].user

        # Create newsletter first
        newsletter = Newsletter.objects.create(**validated_data)

        # Add articles after creation
        newsletter.articles.set(articles)

        return newsletter


# ---------------------------------------------------------
# Publisher Serializer
# ---------------------------------------------------------

class PublisherSerializer(serializers.ModelSerializer):
    """
    Converts Publisher model data into JSON.
    """

    class Meta:
        """
        Meta options for the PublisherSerializer.
        """

        model = Publisher

        fields = [
            "id",
            "name",
            "description",
            "journalists",
            "editors",
        ]


# ---------------------------------------------------------
# User Serializer
# ---------------------------------------------------------

class UserSerializer(serializers.ModelSerializer):
    """
    Converts CustomUser data into JSON.
    """

    class Meta:
        """
        Meta options for the UserSerializer.
        """

        model = CustomUser

        fields = [
            "id",
            "username",
            "email",
            "role",
        ]


# ---------------------------------------------------------
# Approved Article Log Serializer
# ---------------------------------------------------------

class ApprovedArticleLogSerializer(serializers.ModelSerializer):
    """
    Converts approved article logs into JSON.
    """

    class Meta:
        """
        Meta options for the ApprovedArticleLogSerializer.
        """

        model = ApprovedArticleLog

        fields = [
            "id",
            "article",
            "title",
            "approved_by",
            "approved_at",
        ]

        read_only_fields = [
            "id",
            "approved_at",
        ]
