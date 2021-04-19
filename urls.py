import movie_app.apps.movie_credit.views as movie_credit_views
import movie_app.apps.person.views as person_views
import movie_app.apps.movie.views as movie_views
import movie_app.apps.genre.views as genre_views
from rest_framework.routers import DefaultRouter
from movie_app import views as main_views
from django.urls import include, path
from django.contrib import admin


api_router = DefaultRouter()
api_router.register(r'movies', movie_views.MovieViewSet)
api_router.register(r'people', person_views.PersonViewSet)
api_router.register(r'movie-credits', movie_credit_views.MovieCreditViewSet)
api_router.register(r'genres', genre_views.GenreViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_views.home, name='home'),
    path('data/', main_views.about_the_data, name='about_the_data'),
    path('search/', main_views.search_results, name='search_results'),
    path('api/', include(api_router.urls)),
    path('movies/', movie_views.MovieListView.as_view(), name='movies'),
    path('movies/<int:pk>', movie_views.MovieDetailView.as_view(), name='movie'),
    path('people/', person_views.PersonListView.as_view(), name='people'),
    path('people/<int:pk>', person_views.PersonDetailView.as_view(), name='person'),
    path('genre/<int:pk>', genre_views.GenreDetailView.as_view(), name='genre')
]
