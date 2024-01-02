"""assignment1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import include, path
from django.views.generic import TemplateView
from geo_app1 import views as geo_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("updatedb/", geo_views.update_location, name="updatedb"),
    path("search_data/", geo_views.search_name, name="search_data"),
    path("nearest_data/", geo_views.nearest_data, name="nearest_data"),
    path('get_location_data/', geo_views.get_location_data, name="get_location_data"),
    path("offline/", geo_views.offline, name="offline"),
    path('', include('pwa.urls')),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("", TemplateView.as_view(template_name="home.html"), name="home")
    # path('', include('world.urls'))

]
