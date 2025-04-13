from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('recipes/', views.RecipeListView.as_view(), name='recipe-list'),
    path('recipe/<int:pk>/', views.RecipeDetailView.as_view(), name='recipe-detail'),
    path('recipe/new/', views.RecipeCreateView.as_view(), name='recipe-create'),
    path('recipe/<int:pk>/update/', views.RecipeUpdateView.as_view(), name='recipe-update'),
    path('recipe/<int:pk>/delete/', views.RecipeDeleteView.as_view(), name='recipe-delete'),
    path('recipe/<int:pk>/review/', views.add_review, name='add-review'),
    path('recipe/<int:pk>/save/', views.save_recipe, name='save-recipe'),
    path('my-recipes/', views.my_recipes, name='my-recipes'),
    path('saved-recipes/', views.saved_recipes, name='saved-recipes'),
]