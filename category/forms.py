from django import forms
from fawayid.blog.models import Post


class PostCategoryForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('publishDate', 'modifyDate', 'slug', 'author', "state", "category")
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control','id': 'title', 'placeholder': 'Title'}),
            'content': forms.Textarea(attrs={'class': 'form-control textarea',"placeholder": 'Post Content'}),
        }