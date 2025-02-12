from django.urls import path
from users.views import RegisterView, LoginUserView, ProfileView, LogoutView


urlpatterns = [
    path('registration/', RegisterView.as_view(), name='register'),
    path('authorization/', LoginUserView.as_view(), name='auth'),
    path('profile/', ProfileView.as_view(), name='account'),
    path('logout/', LogoutView.as_view(), name='logout'),

]