from django.utils import timezone
from django.contrib import admin
from django.db import models


class MovieCredit(models.Model):
    created_at = models.DateTimeField(editable=False, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    person = models.ForeignKey('person.Person', on_delete=models.SET_NULL, blank=True, null=True)
    movie = models.ForeignKey('movie.Movie', on_delete=models.SET_NULL, blank=True, null=True)
    role = models.CharField(max_length=255, null=True, blank=True)
    tmdb_id = models.IntegerField(null=True, blank=True)
    tmdb_image_path = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return 'Credit for {} as {} in {}'.format(self.person, self.movie, self.role)


@admin.register(MovieCredit)
class MovieCreditAdmin(admin.ModelAdmin):
    list_per_page = 100
    list_display = ('id', 'created_at', 'person', 'movie', 'role')
    list_display_links = ['id', 'created_at', 'person', 'movie', 'role']
    search_fields = ['person__name', 'movie__title', 'role']
    autocomplete_fields = ['person', 'movie']
    save_on_top = True
    show_full_result_count = True
