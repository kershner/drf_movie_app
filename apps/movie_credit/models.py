from django.utils import timezone
from django.conf import settings
from django.contrib import admin
from django.db import models


class MovieCredit(models.Model):
    created_at = models.DateTimeField(editable=False, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    person = models.ForeignKey('person.Person', on_delete=models.SET_NULL, blank=True, null=True)
    movie = models.ForeignKey('movie.Movie', on_delete=models.SET_NULL, blank=True, null=True)
    actor_name = models.CharField(max_length=255, null=True, blank=True)
    movie_title = models.CharField(max_length=255, null=True, blank=True)
    release_date = models.DateTimeField(null=True, blank=True)
    role = models.CharField(max_length=255, null=True, blank=True)
    tmdb_id = models.IntegerField(null=True, blank=True)
    tmdb_image_path = models.CharField(max_length=255, null=True, blank=True)

    def get_full_image_url(self, size='w500'):
        if self.tmdb_image_path:
            return '{}{}{}'.format(settings.BASE_TMDB_IMAGE_URL, size, self.tmdb_image_path)
        return None

    def get_small_image_url(self):
        if self.tmdb_image_path:
            return self.get_full_image_url(size='w200')
        return None

    def get_medium_image_url(self):
        if self.tmdb_image_path:
            return self.get_full_image_url(size='w400')
        return None

    def __str__(self):
        return 'Credit for {} as {} in {}'.format(self.person, self.movie, self.role)


@admin.register(MovieCredit)
class MovieCreditAdmin(admin.ModelAdmin):
    list_per_page = 100
    list_display = ('id', 'created_at', 'person', 'actor_name', 'movie_title', 'role')
    list_display_links = ['id', 'created_at', 'person', 'actor_name', 'movie_title', 'role']
    search_fields = ['id', 'person__name', 'actor_name', 'movie_title', 'movie__title', 'role']
    autocomplete_fields = ['person', 'movie']
    save_on_top = True
    show_full_result_count = True
