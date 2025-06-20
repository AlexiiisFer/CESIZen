from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(UserProfile)

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_active', 'created_at')
    list_filter = ('is_active', 'category')
    search_fields = ('title', 'description')


@admin.register(FavoriteActivity)
class FavoriteActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity')
    search_fields = ('user__username', 'activity__title')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')
    search_fields = ('name',)

@admin.register(Information)
class InformationAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'created_at')
    search_fields = ('title',)
