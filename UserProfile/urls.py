from django.urls import path
from .views import signUp, LogIn, logOut, changePassword, userProfile

urlpatterns = [
    path('signup', signUp, name="signup"),
    path('login', LogIn, name="login"),
    path('logout', logOut, name="logout"),
    path('change', changePassword, name="change"),
    path('edit', userProfile, name="profile")
]
