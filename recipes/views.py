from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from django.db.models import Avg, Count

from .models import Recipe, Review, SavedRecipe, Category
from .forms import RecipeForm, ReviewForm

class HomeView(ListView):
    model = Recipe
    template_name = 'recipes/home.html'
    context_object_name = 'recipes'
    ordering = ['-created_at']
    paginate_by = 6
    
    def get_queryset(self):
        # Get recipes with the most reviews
        return Recipe.objects.annotate(
            review_count=Count('reviews'),
            avg_rating=Avg('reviews__rating')
        ).order_by('-review_count', '-avg_rating', '-created_at')[:6]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['recent_recipes'] = Recipe.objects.order_by('-created_at')[:3]
        return context

class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/recipe_list.html'
    context_object_name = 'recipes'
    paginate_by = 9
    
    def get_queryset(self):
        queryset = Recipe.objects.all()
        
        # Filter by category if provided
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(categories__name=category)
            
        # Filter by search query if provided
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(title__icontains=query) | \
                      queryset.filter(description__icontains=query) | \
                      queryset.filter(ingredients__icontains=query)
                      
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/recipe_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_form'] = ReviewForm()
        
        # Check if user has saved this recipe
        if self.request.user.is_authenticated:
            context['is_saved'] = SavedRecipe.objects.filter(
                user=self.request.user, 
                recipe=self.object
            ).exists()
            
        # Get similar recipes (same category)
        similar_recipes = Recipe.objects.filter(
            categories__in=self.object.categories.all()
        ).exclude(id=self.object.id).distinct()[:3]
        context['similar_recipes'] = similar_recipes
        
        return context

class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Recipe created successfully!')
        return super().form_valid(form)

class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_form.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Recipe updated successfully!')
        return super().form_valid(form)
    
    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.author

class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipe
    template_name = 'recipes/recipe_confirm_delete.html'
    success_url = reverse_lazy('recipe-list')
    
    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.author
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Recipe deleted successfully!')
        return super().delete(request, *args, **kwargs)

@login_required
def add_review(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    
    # Check if user already reviewed this recipe
    existing_review = Review.objects.filter(user=request.user, recipe=recipe).first()
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=existing_review)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.recipe = recipe
            review.save()
            messages.success(request, 'Your review has been added!')
            return redirect('recipe-detail', pk=recipe.pk)
    
    return redirect('recipe-detail', pk=recipe.pk)

@login_required
def save_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    saved_recipe, created = SavedRecipe.objects.get_or_create(user=request.user, recipe=recipe)
    
    if created:
        messages.success(request, f'"{recipe.title}" has been saved to your favorites!')
    else:
        saved_recipe.delete()
        messages.info(request, f'"{recipe.title}" has been removed from your favorites.')
    
    return redirect('recipe-detail', pk=recipe.pk)

@login_required
def my_recipes(request):
    recipes = Recipe.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'recipes/my_recipes.html', {'recipes': recipes})

@login_required
def saved_recipes(request):
    saved = SavedRecipe.objects.filter(user=request.user).order_by('-saved_at')
    return render(request, 'recipes/saved_recipes.html', {'saved_recipes': saved})
