from django.contrib.auth.models import User
from django.test import TestCase
import pytest
from django.test import Client
# Create your tests here.
from django.urls import reverse

from FootballCenter_app.forms import TypeOfGameCreateForm, NationalityCreateForm, PlayerCreateForm, ClubCreateForm, \
    CreateUserForm, PlayerInClubCreateForm, LoginForm
from FootballCenter_app.models import TypeOfGame, Club, Nationality, Player, PlayerInClub


@pytest.mark.django_db
def test_index(client):
    client.login(username='skoq', password='password1')
    url = '/'
    response = client.get(url)
    assert response.status_code == 200
    assert 'Football Center' in str(response.content)


def test_create_user_get():
    client = Client()
    url = reverse('create_user')
    response = client.get(url)
    assert response.status_code == 200
    create_user_form_in_view = response.context['form']
    assert isinstance(create_user_form_in_view, CreateUserForm)

@pytest.mark.django_db
def test_create_user_post(user):
    client = Client()
    url = reverse('create_user')
    data = {
        'username': 'Adrian99',
        'first_name': 'Adrian',
        'last_name': 'Skoczylas',
        'password1': 'strongpwd1',
        'password2': 'strongpwd1',
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url.startswith('/')
    assert User.objects.get(username='Adrian99')


@pytest.mark.django_db
def test_login_get(user):
    client = Client()
    url = reverse('login')
    response = client.get(url)
    assert response.status_code == 200
    login_form_in_view = response.context['form']
    assert isinstance(login_form_in_view, LoginForm)


@pytest.mark.django_db
def test_login_post(user):
    client = Client()
    url = reverse('login')
    data = {
        'username': user.username,
        'password': 'pass'
    }
    response = client.post(url, data)
    assert response.status_code == 200

@pytest.mark.django_db
def test_logout(user):
    client = Client()
    client.force_login(user)
    url = reverse('logout')
    url_red = reverse('index')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(url_red)


@pytest.mark.django_db
def test_add_tog_get(superuser):
    client = Client()
    client.force_login(superuser)
    url = reverse('add_type_of_game')
    response = client.get(url)
    assert response.status_code == 200
    form_in_view = response.context['form']
    assert isinstance(form_in_view, TypeOfGameCreateForm)



@pytest.mark.django_db
def test_add_tog_post(superuser, type_of_game):
    client = Client()
    client.force_login(superuser)
    url = reverse('add_type_of_game')
    data = {
        'name': 'Type2',
        'number_of_participants': 10,
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url.startswith(url)
    assert TypeOfGame.objects.get(name='Type2')


@pytest.mark.django_db
def test_type_of_game_list(togs):
    client = Client()
    url = reverse('type_of_game_list')
    response = client.get(url)
    assert response.status_code == 200
    type_of_games_form_view = response.context['type_of_games']
    assert type_of_games_form_view.count() == len(togs)


@pytest.mark.django_db
def test_add_nationality_get(superuser):
    client = Client()
    client.force_login(superuser)
    url = reverse('add_nationality')
    response = client.get(url)
    assert response.status_code == 200
    form_in_view = response.context['form']
    assert isinstance(form_in_view, NationalityCreateForm)


@pytest.mark.django_db
def test_add_nationality_post(superuser, nationality):
    client = Client()
    client.force_login(superuser)
    url = reverse('add_nationality')
    data = {
        'name': 'Poland',
        'world_cup': 1,
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url.startswith(url)
    assert Nationality.objects.get(name='Poland')


@pytest.mark.django_db
def test_nationalities_list(nationalities):
    client = Client()
    url = reverse('nationality_list')
    response = client.get(url)
    assert response.status_code == 200
    nationalities = response.context['nationalities']
    assert nationalities.count() == len(nationalities)


@pytest.mark.django_db
def test_add_player_get(superuser):
    client = Client()
    client.force_login(superuser)
    url = reverse('add_player')
    response = client.get(url)
    assert response.status_code == 200
    form_in_view = response.context['form']
    assert isinstance(form_in_view, PlayerCreateForm)


@pytest.mark.django_db
def test_add_player_post(superuser, nationality):
    client = Client()
    client.force_login(superuser)
    url = reverse('add_player')
    data = {
        'name': 'Marek',
        'surname': 'Koniarek',
        'dob': '1995-04-04',
        'height': 180,
        'value': 30,
        'leg': '1',
        'sponsor': 'Nike',
        'nationality': nationality.id,


    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert Player.objects.get(name='Marek')


@pytest.mark.django_db
def test_add_club_get(superuser):
    client = Client()
    client.force_login(superuser)
    url = reverse('add_club')
    response = client.get(url)
    assert response.status_code == 200
    form_in_view = response.context['form']
    assert isinstance(form_in_view, ClubCreateForm)


@pytest.mark.django_db
def test_add_club_post(superuser, club):
    client = Client()
    client.force_login(superuser)
    url = reverse('add_club')
    data = {
        'name': 'Real Madryd',
        'country': 'Hiszpania',
        'number_of_players': 25,
        'average_age': 26,

    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url.startswith(url)
    assert Club.objects.get(name='Real Madryd')

@pytest.mark.django_db
def test_player_in_club_get(superuser, client):
    client = Client()
    client.force_login(superuser)
    url = reverse('add_player_in_club')
    response = client.get(url)
    assert response.status_code == 200
    form_in_view = response.context['form']
    assert isinstance(form_in_view, PlayerInClubCreateForm)


@pytest.mark.django_db
def test_player_in_club_post(superuser, club, player, players_in_club):
    client = Client()
    client.force_login(superuser)
    url = reverse('add_player_in_club', args=(players_in_club.id,))
    data = {
        'player': player.id,
        'club': club.id,
        'start_date': '2020-05-05',
        'end_date': 1,
        'value_of_transfer': 50,
    }
    response = client.post(url, data)
    assert response.status_code == 200
    assert PlayerInClub.objects.get(player=player.id)


@pytest.mark.django_db
def test_player_detail(player):
    client = Client()
    url = reverse('player_detail', args=(player.id,))
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['player'] == player


@pytest.mark.django_db
def test_club_detail(players_in_club):
    client = Client()
    club = players_in_club[0].club.first()
    url = reverse('club_detail', args=(club.id,))
    response = client.get(url)
    assert response.status_code == 200
    club_resp = response.context['club']
    players = club_resp.player_set.all()
    assert club_resp == club
    assert players.count() == club.player_set.all().count()


@pytest.mark.django_db
def test_type_of_game_detail(type_of_game):
    client = Client()
    url = reverse('type_of_game_detail', args=(type_of_game.id,))
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['type_of_game'] == type_of_game

@pytest.mark.django_db
def test_delete_tog_get(superuser, type_of_game):
    client = Client()
    client.force_login(superuser)
    url = reverse('delete_type_of_game', args=(type_of_game.id, ))
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['type_of_game']


@pytest.mark.django_db
def test_delete_tog_post(superuser, type_of_game):
    client = Client()
    client.force_login(superuser)
    url = reverse('delete_type_of_game', args=(type_of_game.id, ))
    response = client.post(url)
    assert type_of_game.delete()
    assert response.status_code == 302


@pytest.mark.django_db
def test_delete_club_from_tog_get(superuser, type_of_game, club):
    client = Client()
    client.force_login(superuser)
    url = reverse('delete_club_from_type_of_game', args=(type_of_game.id, club.id, ))
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['type_of_game']
    assert response.context['club']


@pytest.mark.django_db
def test_delete_club_from_tog_post(superuser, type_of_game, club):
    client = Client()
    client.force_login(superuser)
    url = reverse('delete_club_from_type_of_game', args=(type_of_game.id, club.id, ))
    response = client.post(url)
    assert response.status_code == 302
    # assert type_of_game.club.remove(club)



@pytest.mark.django_db
def test_modify_type_of_game_get(superuser, type_of_game):
    client = Client()
    client.force_login(superuser)
    url = reverse('modify_tog', args=(type_of_game.id,))
    response = client.get(url)
    assert response.status_code == 200
    form_in_view = response.context['form']
    assert isinstance(form_in_view, TypeOfGameCreateForm)




