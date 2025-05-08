"""
URL configuration for mhWorldBuilder project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("weapons/", views.weapon_list, name="weapon_list"),
    path("armor/", views.armor_list, name="armor_list"),
    path("", views.buildmaker, name='buildmaker'),
    path('search/', views.search, name='searchengine'),
    path('weapon_search/', views.weapon_search, name='weapon_search'),
    path('armor_search/', views.armor_search, name='weapon_search'),
    path('charm_search/', views.charm_search, name='charm_search'),
    path('decoration_search/', views.decoration_search, name='decoration_search'),
    path('weapon/<int:weapon_id>/', views.weapon, name='weapon'),
    path('armor/<int:armor_id>/', views.armor, name='armor'),
    path('charm/<int:charm_id>/', views.charm, name='charm'),
    path('decoration/<int:decoration_id>/', views.decoration, name='decoration'),
    path('motion/', views.motion, name='motion'),
    path('skills/', views.skills, name='skills'),
]
