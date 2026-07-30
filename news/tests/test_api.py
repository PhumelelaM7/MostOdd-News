"""
Automated API tests for the MostOdd News application.
"""

from unittest.mock import patch

from rest_framework import status
from rest_framework.test import APITestCase

from news.models import (
    Article,
    CustomUser,
    Newsletter,
    Publisher,
)


class NewsAPITestCase(APITestCase):

    def setUp(self):
        """
        Create test data used throughout the API tests.
        """

        # -----------------------------
        # Reader
        # -----------------------------
        self.reader = CustomUser.objects.create_user(
            username="TestReader",
            password="Password123!",
            role="reader",
            email="reader@test.com",
        )

        # -----------------------------
        # Journalist
        # -----------------------------
        self.journalist = CustomUser.objects.create_user(
            username="TestJournalist",
            password="Password123!",
            role="journalist",
            email="journalist@test.com",
        )

        # -----------------------------
        # Editor
        # -----------------------------
        self.editor = CustomUser.objects.create_user(
            username="TestEditor",
            password="Password123!",
            role="editor",
            email="editor@test.com",
            is_staff=True,
        )

        # -----------------------------
        # Publisher
        # -----------------------------
        self.publisher = Publisher.objects.create(
            name="Test Publisher",
            description="Testing Publisher",
        )

        self.publisher.journalists.add(
            self.journalist
        )

        # -----------------------------
        # Approved article
        # -----------------------------
        self.article = Article.objects.create(
            title="Approved Article",
            content="Testing article.",
            author=self.journalist,
            publisher=self.publisher,
            approved=True,
        )

        # -----------------------------
        # Newsletter
        # -----------------------------
        self.newsletter = Newsletter.objects.create(
            title="Weekly News",
            description="Newsletter",
            author=self.journalist,
        )

        self.newsletter.articles.add(
            self.article
        )

    # =====================================================
    # Authentication
    # =====================================================

    def test_journalist_can_login(self):

        response = self.client.post(
            "/api/token/",
            {
                "username": "TestJournalist",
                "password": "Password123!",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    # =====================================================
    # Journalist Tests
    # =====================================================

    def test_journalist_can_create_article(self):

        self.client.force_authenticate(
            user=self.journalist
        )

        response = self.client.post(
            "/api/articles/",
            {
                "title": "New Article",
                "content": "Article Content",
                "publisher": self.publisher.id,
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_journalist_can_create_newsletter(self):

        self.client.force_authenticate(
            user=self.journalist
        )

        response = self.client.post(
            "/api/newsletters/",
            {
                "title": "API Newsletter",
                "description": "Testing",
                "articles": [],
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    # =====================================================
    # Reader Tests
    # =====================================================

    def test_reader_cannot_create_article(self):

        self.client.force_authenticate(
            user=self.reader
        )

        response = self.client.post(
            "/api/articles/",
            {
                "title": "Invalid",
                "content": "Reader",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_reader_can_only_view_subscribed_articles(self):

        self.reader.subscribed_publishers.add(
            self.publisher
        )

        self.client.force_authenticate(
            user=self.reader
        )

        response = self.client.get(
            "/api/articles/subscribed/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

    # =====================================================
    # Editor Tests
    # =====================================================

    def test_editor_can_delete_article(self):

        self.client.force_authenticate(
            user=self.editor
        )

        response = self.client.delete(
            f"/api/articles/{self.article.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

    def test_reader_cannot_delete_article(self):

        self.client.force_authenticate(
            user=self.reader
        )

        response = self.client.delete(
            f"/api/articles/{self.article.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    # =====================================================
    # API Retrieval Tests
    # =====================================================

    def test_get_all_approved_articles(self):

        response = self.client.get(
            "/api/articles/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

    def test_get_single_article(self):

        response = self.client.get(
            f"/api/articles/{self.article.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_get_newsletters(self):

        response = self.client.get(
            "/api/newsletters/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    # =====================================================
    # Approval Workflow
    # =====================================================

    @patch("news.views.requests.post")
    @patch("news.views.send_mail")
    def test_editor_can_approve_article(
        self,
        mock_send_mail,
        mock_post,
    ):
        """
        Verify that editors can approve
        an article and trigger the
        integration logic.
        """

        article = Article.objects.create(
            title="Pending",
            content="Pending article",
            author=self.journalist,
            publisher=self.publisher,
            approved=False,
        )

        self.client.force_login(
            self.editor
        )

        response = self.client.post(
            f"/news/approve/{article.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_302_FOUND,
        )

        article.refresh_from_db()

        self.assertTrue(
            article.approved
        )

        mock_post.assert_called()

    # =====================================================
    # Newsletter Retrieval
    # =====================================================

    def test_newsletter_exists(self):

        self.assertEqual(
            Newsletter.objects.count(),
            1,
        )