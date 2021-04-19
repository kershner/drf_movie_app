from movie_app.apps.movie.models import MovieCredit
from movie_app.apps.person.models import Person
from movie_app.apps.movie.models import Movie
from movie_app.apps.genre.models import Genre
from movie_app.forms import SearchForm
from django.db.models import Count
from django.shortcuts import render
import random


def home(request):
    num_results = 20
    min_credits = 10
    movie_pks = Movie.objects.annotate(c=Count('moviecredit')).filter(tmdb_image_path__isnull=False, c__gte=min_credits).values_list('pk', flat=True)
    random_movie_pks = [random.choice(movie_pks) for num in range(num_results)]
    popular_movies = Movie.objects.filter(pk__in=random_movie_pks).order_by('-popularity').all()

    people_pks = Person.objects.annotate(c=Count('moviecredit')).filter(tmdb_image_path__isnull=False, c__gte=min_credits).values_list('pk', flat=True)
    random_people_pks = [random.choice(people_pks) for num in range(num_results)]
    popular_people = Person.objects.filter(pk__in=random_people_pks).order_by('-popularity').all()

    character_pks = MovieCredit.objects.values_list('pk', flat=True)
    random_character_pks = [random.choice(character_pks) for num in range(num_results)]
    popular_characters = MovieCredit.objects.filter(pk__in=random_character_pks).all().order_by('-person__popularity')

    genres = Genre.objects.all()

    ctx = {
        'form': SearchForm(),
        'popular_movies': popular_movies,
        'popular_people': popular_people,
        'popular_characters': popular_characters,
        'genres': genres
    }
    return render(request, 'home/home.html', ctx)


def search_results(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            q = form.cleaned_data['q']
            movie_results = Movie.objects.filter(title__icontains=q).annotate(c=Count('moviecredit')).order_by('-c').all()
            person_results = Person.objects.filter(name__icontains=q).order_by('-popularity').all()
            character_results = MovieCredit.objects.filter(role__icontains=q).order_by('-person__popularity').all()
            ctx = {
                'form': form,
                'q': q,
                'movie_results': movie_results,
                'person_results': person_results,
                'character_results': character_results
            }
            return render(request, 'home/search_results.html', ctx)

    return render(request, 'home/search_results.html')


def about_the_data(request):
    ctx = {
        'total_movies': Movie.objects.count(),
        'total_people': Person.objects.count(),
        'total_genres': Genre.objects.count(),
        'total_movie_credits': MovieCredit.objects.count()
    }
    return render(request, 'home/data.html', ctx)
