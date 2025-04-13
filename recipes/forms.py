from django import forms
from .models import Recipe, Review, Category

class RecipeForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'ingredients', 'instructions', 
                  'cooking_time', 'servings', 'image', 'categories']
        widgets = {
            'ingredients': forms.Textarea(attrs={'placeholder': 'Enter each ingredient on a new line'}),
            'instructions': forms.Textarea(attrs={'placeholder': 'Enter each step on a new line'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4}),
        }