from django.contrib import admin
from .models import Category, Recipe, Review, SavedRecipe

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'average_rating')
    list_filter = ('created_at', 'categories')
    search_fields = ('title', 'description', 'ingredients')
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('categories',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('comment', 'user__username', 'recipe__title')

@admin.register(SavedRecipe)
class SavedRecipeAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe', 'saved_at')
    list_filter = ('saved_at',)
    search_fields = ('user__username', 'recipe__title')
