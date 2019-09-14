from django import forms


class Message(forms.Form):
    message = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control input-sm chat_input" , "placeholder": "Write your message here...", "id": "btn-input"}))
