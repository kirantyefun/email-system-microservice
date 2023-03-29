from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.UserRegistration.as_view(), name='register'),
    path('login/', views.CustomAuthToken.as_view(), name='login'),
    # path('login/', views.UserLogin.as_view(), name='login'),
    path('logout/', views.UserLogout.as_view(), name='logout'),
]
