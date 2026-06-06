
# Register your models here.
from django.contrib import admin
from .models import URLMapping



@admin.register(URLMapping)
class URLMappingAdmin(admin.ModelAdmin):
    list_display = ["original_url","short_url","click_count","created_at"]
    search_fields = ["original_url","short_url"]