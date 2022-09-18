from django.forms import BooleanField
from django import forms
from .models import *
from django.core.exceptions import ValidationError

class PostForm(forms.ModelForm):
    check_box = BooleanField(label='Согласен!')

    class Meta:
       model = Post
       fields = [
           'title',
           'text',
           'category',
           'author',
       ]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        text = cleaned_data.get("text")

        if title == text:
            raise ValidationError(
                "Заголовок записи и описание должны отличаться!"
            )
        return

class CommentCreateForm(forms.ModelForm):
    text = forms.CharField(label='Text', widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Comment
        fields = ('text',)