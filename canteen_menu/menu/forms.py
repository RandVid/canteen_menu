from django import forms
from .models import Comment, Meal, MealCategory


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['description']


class SearchForm(forms.Form):
    class Meta:
        pass


class MealForm(forms.ModelForm):

    class Meta:
        model = Meal
        exclude = ["id",]


class CategoryForm(forms.ModelForm):

    class Meta:
        model = MealCategory
        exclude = ["id",]
