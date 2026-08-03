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
    """
    Automated tests for the News Application API.
    """

    def setUp(self):
        """
        Create reusable test data.
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

        self.publisher.journalists.add(self.journalist)

        # -----------------------------
        # Approved Article
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

        self.newsletter.articles.add(self.article)

    # =====================================================
    # Authentication Tests
    # =====================================================

    def test_reader_can_login(self):

        response = self.client.post(
            "/api/token/",
            {
                "username": "TestReader",
                "password": "Password123!",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

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

    def test_editor_can_login(self):

        response = self.client.post(
            "/api/token/",
            {
                "username": "TestEditor",
                "password": "Password123!",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_invalid_login(self):

        response = self.client.post(
            "/api/token/",
            {
                "username": "TestJournalist",
                "password": "WrongPassword",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    # =====================================================
    # Journalist Tests
    # =====================================================

    def test_journalist_can_create_article(self):

        self.client.force_authenticate(user=self.journalist)

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

        self.client.force_authenticate(user=self.journalist)

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

    def test_journalist_cannot_approve_article(self):

        article = Article.objects.create(
            title="Pending",
            content="Pending",
            author=self.journalist,
            publisher=self.publisher,
            approved=False,
        )

        self.client.force_login(self.journalist)

        response = self.client.post(
            f"/news/approve/{article.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    # =====================================================
    # Reader Tests
    # =====================================================

    def test_reader_cannot_create_article(self):

        self.client.force_authenticate(user=self.reader)

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

    def test_reader_cannot_update_article(self):

        self.client.force_authenticate(user=self.reader)

        response = self.client.put(
            f"/api/articles/{self.article.id}/",
            {
                "title": "Updated",
                "content": "Updated",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_reader_cannot_delete_article(self):

        self.client.force_authenticate(user=self.reader)

        response = self.client.delete(
            f"/api/articles/{self.article.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_reader_can_only_view_subscribed_articles(self):

        self.reader.subscribed_publishers.add(
            self.publisher
        )

        self.client.force_authenticate(user=self.reader)

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
    # Anonymous Access
    # =====================================================

    def test_anonymous_user_cannot_view_subscribed_articles(self):

        response = self.client.get(
            "/api/articles/subscribed/"
        )

        self.assertIn(
            response.status_code,
            [
                status.HTTP_401_UNAUTHORIZED,
                status.HTTP_403_FORBIDDEN,
            ],
        )

    # =====================================================
    # Editor Tests
    # =====================================================

    def test_editor_can_delete_article(self):

        self.client.force_authenticate(user=self.editor)

        response = self.client.delete(
            f"/api/articles/{self.article.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

    # =====================================================
    # API Retrieval
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
        Editors should be able to approve articles,
        send email notifications,
        and trigger the API integration.
        """

        # Create a pending article
        article = Article.objects.create(
            title="Pending",
            content="Pending article",
            author=self.journalist,
            publisher=self.publisher,
            approved=False,
        )

        # -------------------------------------------------
        # Create a Reader who subscribes to the article
        # -------------------------------------------------
        reader = CustomUser.objects.create_user(
            username="reader_test",
            password="password123",
            email="reader@example.com",
            role="reader",
        )

        # Subscribe to the publisher
        reader.subscribed_publishers.add(self.publisher)

        # Subscribe to the journalist
        reader.subscribed_journalists.add(self.journalist)

        # Log in as the Editor
        self.client.force_login(self.editor)

        # Approve the article
        response = self.client.post(
            f"/news/approve/{article.id}/"
        )

        # Should redirect after approval
        self.assertEqual(
            response.status_code,
            status.HTTP_302_FOUND,
        )

        # Refresh from database
        article.refresh_from_db()

        # Article should now be approved
        self.assertTrue(
            article.approved
        )

        # Email notification should be sent
        mock_send_mail.assert_called_once()

        # Internal API should be called
        mock_post.assert_called_once()

    # =====================================================
    # Newsletter Tests
    # =====================================================

    def test_newsletter_exists(self):

        self.assertEqual(
            Newsletter.objects.count(),
            1,
        )
