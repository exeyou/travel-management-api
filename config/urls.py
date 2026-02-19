"""
URL configuration for config project.

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

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from travel.views import TravelProjectViewSet, ProjectPlaceViewSet

router = DefaultRouter()
router.register(r'projects', TravelProjectViewSet, basename='projects')

project_places = ProjectPlaceViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

project_place_detail = ProjectPlaceViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),

    path(
        'api/projects/<int:project_pk>/places/',
        project_places,
        name='project-places'
    ),
    path(
        'api/projects/<int:project_pk>/places/<int:pk>/',
        project_place_detail,
        name='project-place-detail'
    ),
]
