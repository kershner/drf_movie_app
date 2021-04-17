from movie_app.apps.movie_credit.models import MovieCredit
from django.utils import timezone
from django.contrib import admin
from django.conf import settings
from django.db import models


class Person(models.Model):
    created_at = models.DateTimeField(editable=False, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    name = models.CharField(max_length=255, null=False, blank=False)
    bio = models.TextField(null=True, blank=True)
    place_of_birth = models.CharField(max_length=255, null=True, blank=True)
    birthday = models.DateTimeField(null=True, blank=True)
    deathday = models.DateTimeField(null=True, blank=True)
    tmdb_id = models.IntegerField(null=True, blank=True)
    tmdb_image_path = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_full_image_url(self, size='w500'):
        return '{}{}{}'.format(settings.BASE_TMDB_IMAGE_URL, size, self.tmdb_image_path)

    def get_small_image_url(self):
        return self.get_full_image_url(size='w200')

    def get_medium_image_url(self):
        return self.get_full_image_url(size='w400')

    def get_movie_credits(self):
        movie_credits = MovieCredit.objects.filter(person=self).order_by('-release_date').all()
        return movie_credits


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_per_page = 100
    list_display = ('id', 'created_at', 'name')
    list_display_links = ['id', 'created_at', 'name']
    search_fields = ['id', 'name']
    save_on_top = True
    show_full_result_count = True
