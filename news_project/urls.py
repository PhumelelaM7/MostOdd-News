"""
URL configuration for news_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# Import Django admin
from django.contrib import admin

# Import path and include
from django.urls import path, include

# Import JWT views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Import views from the news application
from news import views


# Main URL patterns
urlpatterns = [

    path(
        "",
        views.home,
        name="home",
    ),

    # User registration page
    path(
        "register/",
        views.register,
        name="register"
    ),

    # Django authentication (Login and Logout)
    path(
        "accounts/",
        include("django.contrib.auth.urls"),
    ),

    # Django Admin
    path("admin/", admin.site.urls),

    # News application URLs
    path(
        "news/",
        include("news.urls")
    ),

    # REST API URLs
    path(
        "api/",
        include("news.api_urls")
    ),

    # DRF login/logout for browsable API
    path(
        "api-auth/",
        include("rest_framework.urls")
    ),

    # JWT Authentication
    path(
        "api/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),

    path(
        "api/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
]
