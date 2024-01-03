from django import forms
from .models import Comment, Meal


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
