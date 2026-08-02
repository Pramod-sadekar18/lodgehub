"""
URL configuration for lodgehub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from lodge.views import property_detail_page

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("accounts.urls")),
    path("plan-trip/", include("plan_trip.page_urls")),
    path("api/", include("lodge.urls")),
    path("book_api/", include("booking.urls")),
    path("api/plan-trip/", include("plan_trip.urls")),
    path("property/<int:id>/", property_detail_page, name="property_detail_short"),
    path("property/<int:id>/<slug:slug>/", property_detail_page, name="property_detail"),
]
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)