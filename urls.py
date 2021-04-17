from movie_app.apps.person.views import PersonViewSet
from movie_app.apps.movie.views import MovieViewSet
from rest_framework.routers import DefaultRouter
from movie_app import views as main_views
from django.urls import include, path
from django.contrib import admin


api_router = DefaultRouter()
api_router.register(r'movies', MovieViewSet)
api_router.register(r'people', PersonViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_views.home),
    path('api/', include(api_router.urls))
]
