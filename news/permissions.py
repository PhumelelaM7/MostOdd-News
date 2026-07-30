"""
Custom permissions for the MostOdd News API.
"""

# Import DRF permission classes
from rest_framework.permissions import (
    BasePermission,
    SAFE_METHODS,
)


# ---------------------------------------------------------
# Article API permission
# ---------------------------------------------------------
class IsJournalistOrEditorOrReadOnly(BasePermission):
    """
    Control access to article endpoints.
    """

    def has_permission(self, request, view):
        """
        Check whether the user has permission.
        """

        # Allow safe requests for everyone
        if request.method in SAFE_METHODS:
            return True

        # User must be authenticated
        if not request.user.is_authenticated:
            return False

        # Allow only Journalists and Editors
        return request.user.role in [
            "journalist",
            "editor",
        ]


# ---------------------------------------------------------
# Article API Permission
# ---------------------------------------------------------
class IsArticleRolePermission(BasePermission):
    """
    Permission rules for the Article API.

    - Everyone may view approved articles.
    - Only Journalists may create articles.
    - Journalists and Editors may update or delete articles.
    """

    def has_permission(self, request, view):
        """
        Check whether the current user
        has permission for the request.
        """

        # Anyone can view
        if request.method in SAFE_METHODS:
            return True

        # User must be logged in
        if not request.user.is_authenticated:
            return False

        # Only Journalists may create
        if request.method == "POST":
            return request.user.role == "journalist"

        # Journalists and Editors may edit/delete
        if request.method in [
            "PUT",
            "PATCH",
            "DELETE",
        ]:
            return request.user.role in [
                "journalist",
                "editor",
            ]

        return False