"""footballCenter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the included() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from FootballCenter_app import views

urlpatterns = [
        path('admin/', admin.site.urls),
        path('', views.IndexView.as_view(), name='index'),
        path('add_type_of_game/', views.AddTypeOfGameView.as_view(), name='add_type_of_game'),
        path('type_of_game_list/', views.TypeOfGameListView.as_view(), name='type_of_game_list'),
        path('add_player/', views.AddPlayerView.as_view(), name='add_player'),

        path('add_nationality/', views.AddNationality.as_view(), name='add_nationality'),
        path('nationalities_list/', views.NationalityListView.as_view(), name='nationality_list'),
        path('add_club/', views.AddClubView.as_view(), name='add_club'),

        path('add_player_in_club/', views.AddPlayerInClubView.as_view(), name='add_player_in_club'),
        path('player_detail/<int:id_player>/', views.PlayerDetailView.as_view(), name='player_detail'),
        path('type_of_game_detail/<int:id_type_of_game>/', views.TypeOfGameDetailView.as_view(), name='type_of_game_detail'),
        path('club_detail/<int:id_club>/', views.ClubDetailView.as_view(), name='club_detail'),
        path('type_of_game/<int:id_type_of_game>/add_club/', views.AddClubToTypeOfGameView.as_view(), name='add_club_to_type_of_game'),
        path('delete_club_from_tog/<int:type_of_game_id>/<int:club_id>/', views.DeleteClubFromTypeOfGameView.as_view(), name='delete_club_from_type_of_game'),
        path('modify_player/<int:player_id>/',views.ModifyPlayerView.as_view(), name='modify_player'),
        path('delete_tog/<int:type_of_game_id>/', views.DeleteTypeOfGameView.as_view(), name='delete_type_of_game'),
        path('modify_tog/<int:type_of_game_id>/', views.ModifyTypeOfGameView.as_view(), name='modify_tog'),

        path('create_user/', views.CreateUserView.as_view(), name='create_user'),
        path('login/', views.LoginView.as_view(), name='login'),
        path('logout/', views.LoginOutView.as_view(), name='logout'),
]
