"""API_SoftDesk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
# Django Libs
from django.contrib import admin
from django.urls import path, include

# Django REST Libs
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

urlpatterns = [
    # Admin part
    path('admin/', admin.site.urls),
    # Authentication
    path("signup/", include('signup.urls')),
    path("login/", TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("login/refresh/", TokenRefreshView.as_view(), name='token-refresh'),
    # API
    path("projects/", include('projects.urls')),
]
