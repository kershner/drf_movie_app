from movie_app.apps.person.views import PersonViewSet
import movie_app.apps.movie.views as movie_views
from rest_framework.routers import DefaultRouter
from movie_app import views as main_views
from django.urls import include, path
from django.contrib import admin


api_router = DefaultRouter()
api_router.register(r'movies', movie_views.MovieViewSet)
api_router.register(r'people', PersonViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_views.home, name='home'),
    path('api/', include(api_router.urls)),
    path('movies/', movie_views.MovieListView.as_view(), name='movies'),
    path('movies/<int:pk>', movie_views.MovieDetailView.as_view(), name='movie')
]

