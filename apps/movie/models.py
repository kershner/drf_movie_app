from movie_app.apps.movie_credit.models import MovieCredit
from django.templatetags.static import static
from django.utils import timezone
from django.contrib import admin
from django.conf import settings
from django.db.models import Q
from django.db import models
import locale


class Movie(models.Model):
    created_at = models.DateTimeField(editable=False, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    title = models.CharField(max_length=255, null=False, blank=False)
    genres = models.ManyToManyField('genre.Genre', blank=True)
    overview = models.TextField(null=True, blank=True)
    runtime = models.IntegerField(null=True, blank=True)
    budget = models.IntegerField(null=True, blank=True)
    release_date = models.DateTimeField(null=True, blank=True)
    popularity = models.FloatField(null=True, blank=True)
    tmdb_id = models.IntegerField(null=True, blank=True)
    tmdb_image_path = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_full_image_url(self, size='w500'):
        if self.tmdb_image_path:
            return '{}{}{}'.format(settings.BASE_TMDB_IMAGE_URL, size, self.tmdb_image_path)
        return static(settings.NO_IMAGE_FILENAME)

    def get_small_image_url(self):
        if self.tmdb_image_path:
            return self.get_full_image_url(size='w200')
        return static(settings.NO_IMAGE_FILENAME)

    def get_medium_image_url(self):
        if self.tmdb_image_path:
            return self.get_full_image_url(size='w400')
        return static(settings.NO_IMAGE_FILENAME)

    def get_cast(self):
        movie_credits = MovieCredit.objects.filter(Q(movie=self) | Q(movie_title=self.title)).order_by('-release_date').all()
        return movie_credits

    def get_budget_display(self):
        return '${:,}'.format(self.budget)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_per_page = 100
    list_display = ('id', 'created_at', 'title', 'runtime')
    list_display_links = ['id', 'created_at', 'title', 'runtime']
    autocomplete_fields = ['genres']
    search_fields = ['id', 'title']
    save_on_top = True
    show_full_result_count = True
