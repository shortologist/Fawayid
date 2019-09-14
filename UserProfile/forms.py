from django import forms
from django.contrib.auth.models import User
from .models import Profile


class LogInForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'id': 'username', 'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'id': 'password', 'placeholder': 'Password'
    }))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        ex = User.objects.filter(username=username).exists()
        if not ex:
            raise forms.ValidationError("username %(username)s does't exists.",
                                        params={'username': username})
        else:
            return username

    def clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError("incorrect password.")
        if not user.check_password(password):
            raise forms.ValidationError("incorrect password.")
        else:
            return password


class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'id': 'username', 'placeholder': 'username'
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control', 'id': 'email', 'placeholder': 'email'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'id': 'password', 'placeholder': 'Password'
    }))
    confirm = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'id': 'confirm',
        'placeholder': ' Confirm Password'
    }))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        ex = User.objects.filter(username=username).exists()
        if ex:
            raise forms.ValidationError("username %(username)s is taken.",
                                        params={'username': username})
        else:
            return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        ex = User.objects.filter(username=email).exists()
        if ex:
            raise forms.ValidationError("email %(email)s is taken.",
                                        params={'email': email})
        else:
            return email

    def clean_confirm(self):
        confirm = self.cleaned_data["confirm"]
        if self.password != confirm:
            raise forms.ValidationError("Passwords Doesn't match.")
        return confirm

    def clean_password(self):
        self.password = self.cleaned_data.get('password')
        if len(self.password) < 8:
            raise forms.ValidationError("Password must be more than 7 character.")
        return self.password


class ProfileForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', "placeholder": 'Username'}), required=False)
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control', "placeholder": 'Email'}), required=False)
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', "placeholder": 'First Name'}), required=False)
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', "placeholder": 'Last Name'}), required=False)
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', "placeholder": 'Enter password'}))

    def clean_password(self):
        id = self.instance.user.id
        user = User.objects.get(id=id)
        password = self.cleaned_data.get('password')
        if not user.check_password(password):
            raise forms.ValidationError("Password not valid.")
        return password

    class Meta:
        model = Profile
        exclude = ('user', 'slug', 'auther')
        widgets = {
            "address": forms.TextInput(attrs={'class': 'form-control', "placeholder": 'Home Address'}),
            "city": forms.TextInput(attrs={'class': 'form-control', "placeholder": 'City'}),
            "about": forms.Textarea(attrs={'class': 'form-control textarea',"placeholder": 'About Me'}),
            "country": forms.TextInput(attrs={'class': 'form-control', "placeholder": 'Country'}),
            "postalCode": forms.TextInput(attrs={'class': 'form-control', "placeholder": 'Postal Code'})
        }


class ChangePasswordForm(forms.Form):

    current = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Current Password',
        'id': 'current'}))
    new = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'New Password',
        'id': 'new'}))
    confirm = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'confirm Password',
        'id': 'confirm'}))

    user = 0

    def set_user(self, user):
        self.user = user

    def clean_current(self):
        password = self.cleaned_data.get('current')
        if self.user.check_password(password):
            return password
        raise forms.ValidationError('Incorrect current Password.')

    def clean(self):
        data = self.cleaned_data
        new, confirm = data.get('new'), data.get('confirm')
        if new != confirm:
            raise forms.ValidationError('Password not match.')
        return data
