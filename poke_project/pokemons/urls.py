from django.urls import path

from pokemons import views

urlpatterns = [
    path('', views.index, name="home"),
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutUser, name="logout"),
]