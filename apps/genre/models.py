from django.utils import timezone
from django.contrib import admin
from django.db import models


class Genre(models.Model):
    created_at = models.DateTimeField(editable=False, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    name = models.CharField(max_length=255, null=False, blank=False)
    tmdb_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_per_page = 100
    list_display = ('id', 'created_at', 'name')
    list_display_links = ['id', 'created_at', 'name']
    search_fields = ['id', 'name']
    save_on_top = True
    show_full_result_count = True
