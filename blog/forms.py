from django import forms
from doc.utility import post_status
from .models import Post

"""
class ControlForm(forms.Form):
    state = forms.ChoiceField(widget=forms.select(attrs={
        'class': 'controlls custom-select custom-select-sm', 'id': 'state'}),
        choices=post_status)

"""


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('publishDate', 'modifyDate', 'slug', 'author', "state")
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control','id': 'title', 'placeholder': 'Title'}),
            'content': forms.Textarea(attrs={'class': 'form-control textarea',"placeholder": 'Post Content'}),
        }

class CommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={
        "name":"comment", "rows":"5", "class": "form-control", "id": "message", "placeholder": "Comment", "required":"required"
    }))