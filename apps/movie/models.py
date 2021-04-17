from django.utils import timezone
from django.contrib import admin
from django.conf import settings
from django.db import models


class Movie(models.Model):
    created_at = models.DateTimeField(editable=False, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    title = models.CharField(max_length=255, null=False, blank=False)
    overview = models.TextField(null=True, blank=True)
    runtime = models.IntegerField(null=True, blank=True)
    budget = models.IntegerField(null=True, blank=True)
    release_date = models.DateTimeField(null=True, blank=True)
    tmdb_id = models.IntegerField(null=True, blank=True)
    tmdb_image_path = models.CharField(max_length=255, null=True, blank=True)

    def get_full_image_url(self, size='w500'):
        return '{}{}{}'.format(settings.BASE_TMDB_IMAGE_URL, size, self.tmdb_image_path)

    def get_small_image_url(self):
        return self.get_full_image_url(size='w200')

    def get_medium_image_url(self):
        return self.get_full_image_url(size='w350')


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_per_page = 100
    list_display = ('id', 'created_at', 'title', 'runtime')
    list_display_links = ['id', 'created_at', 'title', 'runtime']
    search_fields = ['id', 'title']
    save_on_top = True
    show_full_result_count = True
