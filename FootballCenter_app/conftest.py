from datetime import datetime

import pytest
from django.test import Client
from django.contrib.auth.models import User

from FootballCenter_app.models import TypeOfGame, Nationality, Player, Club, PlayerInClub


@pytest.fixture
def type_of_game():
    return TypeOfGame.objects.create(name='Type1', number_of_participants=10)


@pytest.fixture
def togs():
    lst = []
    for x in range(5):
        lst.append(TypeOfGame.objects.create(name=x, number_of_participants=x * 4))
    return lst


@pytest.fixture
def nationality():
    return Nationality.objects.create(name='Portugal')


@pytest.fixture
def nationalities():
    lst = []
    for x in range(5):
        lst.append(Nationality.objects.create(name=x, world_cup='1'))
    return lst


@pytest.fixture
def player(nationality):
    return Player.objects.create(name='Marekkk', surname='Koniarek', dob='1995-04-04', height=180, value=30, leg='1',
                                 sponsor='Nike', nationality=nationality)

@pytest.fixture
def players_in_club(nationality, club):
    lst = []
    for x in range(10):
        p  =Player.objects.create(name=f'Marekkk{x}', surname='Koniarek', dob='1995-04-04', height=180, value=30, leg='1',
                                 sponsor='Nike', nationality=nationality)
        PlayerInClub.objects.create(
            player=p,
            club=club,
            start_date=datetime.now().date(),
            value_of_transfer=1
        )
        lst.append(p)
    return lst

@pytest.fixture
def club():
    return Club.objects.create(name='Real Madryt', country='Hiszpania', number_of_players= 25, average_age=26)


@pytest.fixture
def user():
    return User.objects.create(username='Adrian98', first_name='Adrian', last_name='Skoczylas', password='strongpwd1',)


@pytest.fixture
def superuser():
    return User.objects.create(username='super10', password='12345678', is_superuser= '1')