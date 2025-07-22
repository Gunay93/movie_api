from django.urls import path
from .views import LoginView, RegisterView, LogoutView, SliderView, MovieView, ProfileView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('slider/', SliderView.as_view(), name='slider'),
    path('movie/', MovieView.as_view(), name='movie'),
    path('profile/', ProfileView.as_view(), name='profile'),
]