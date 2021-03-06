from django.contrib import admin
from .models import Genre

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ["name", "active", "color"]
    list_editable = ["active", "color"]

