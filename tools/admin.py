from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Category, Tool, ToolImage

class ToolImageInline(admin.TabularInline):
    model = ToolImage
    extra = 3

class ToolAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'owner', 'price_per_day', 'available', 'created_at')
    list_filter = ('category', 'available', 'condition')
    search_fields = ('name', 'description', 'owner__username')
    inlines = [ToolImageInline]

admin.site.register(Category)
admin.site.register(Tool, ToolAdmin)
