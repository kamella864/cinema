from django.urls import path
from .views import *


urlpatterns = [
    path('', LoginUser.as_view(), name = 'login'),
    path('register', RegistrationUser.as_view(), name = 'register'),
    path('exit', logout_user, name = 'exit'),
    path('home', home, name = 'home'),
    path('favorites', favorites, name='favorites'),
    path('history', history, name='history')
]
