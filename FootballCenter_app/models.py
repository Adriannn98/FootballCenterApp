from datetime import date

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
#null=true - pusta wartość

LEGS = [
    (1, 'left-footed'),
    (2, 'right-footed'),
    (3, 'both')
]

class Player(models.Model):
    name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)
    dob = models.DateField()
    height = models.IntegerField()
    value = models.IntegerField()
    leg = models.IntegerField(choices=LEGS) #get_leg_display aby uzyskać nazwę a nie liczbę z krotki
    sponsor = models.CharField(max_length=64)
    nationality = models.ForeignKey('Nationality', on_delete=models.CASCADE)
    club = models.ManyToManyField('Club', through='PlayerInClub')

    def __str__(self):
        return f"{self.name}{self.surname}"

    def calculate_age(self):
        today = date.today()

        delta = today.year - self.dob.year

        return delta

    def active_club(self):
        return PlayerInClub.objects.get(player=self, end_date__isnull=True).club

        # try:
        #     birthday = self.dob.replace(year=today.year)
        # except ValueError:
        #     birthday = self.dob.replace(year=today.year, day=dob.day-1)
        #
        # if birthday > today:
        #     return today.year - self.dob.year - 1
        # else:
        #     return today.year - born.year

class Nationality(models.Model):
    name = models.CharField(max_length=64)
    world_cup = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"

class Club(models.Model):
    name = models.CharField(max_length=64)
    country = models.CharField(max_length=64)
    number_of_players = models.IntegerField()
    average_age = models.FloatField()

    def __str__(self):
        return f"{self.name}"


class PlayerInClub(models.Model):
    player = models.ForeignKey('Player', on_delete=models.CASCADE)
    club = models.ForeignKey('Club', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    value_of_transfer = models.IntegerField()


class TypeOfGame(models.Model):
    name = models.CharField(max_length=100)
    number_of_participants = models.IntegerField()
    club = models.ManyToManyField(Club)

    def __str__(self):
        return f"{self.name}"


# class Stadium(models.Model):
#     name = models.CharField(max_length=64)
#     capacity = models.IntegerField()
#     build_year = models.DateField()
#     size_of_the_pith = models.CharField(max_length=64)
#     club = models.ForeignKey(Club, on_delete=models.CASCADE)
#
# class Coach(models.Model):
#     name = models.CharField(max_length=64, required=True)
#     surname = models.CharField(max_length=64, required=True)
#     dob = models.DateField(required=True)
#     nationality = models.CharField(max_length=64)
#     preferred_formation = models.CharField(max_length=15)
#     type_of_coaching_license = models.CharField(max_length=64)
#     date_of_employment = models.DateField()
#     contract_term = models.DateField()
#     club = models.ForeignKey(Club, on_delete=models.CASCADE)
#
#     def calculate_age(self):
#         today = date.today()
#
#         delta = today.year - self.dob.year
#
#         return delta
#
#         # try:
#         #     birthday = self.dob.replace(year=today.year)
#         # except ValueError:
#         #     birthday = self.dob.replace(year=today.year, day=born.day-1)
#         #
#         # if birthday > today:
#         #     return today.year - born.year - 1
#         # else:
#         #     return today.year - born.year
#
#     def calculate_employment_time(self):
#         today = date.today()
#
#         delta = (today - self.date_of_employment)
#
#         if int(delta) < 2:    # chcę policzyć liczbę dni bycia zatrudnionym
#             return f"{delta} day"
#         else:
#             return f"{delta} days"
#
# class Comment(models.Model):
#     text = models.TextField(max_length=500)
#     date = models.DateField() # czy cos musi byc tu wiecej? Czy poda nam date wraz z godziną?
#     likes = models.IntegerField()
#     dislikes = models.IntegerField()
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     player = models.ForeignKey(User, on_delete=models.CASCADE)
#     club = models.ForeignKey(User, on_delete=models.CASCADE)
#     coach = models.ForeignKey(User, on_delete=models.CASCADE)
#     nationality = models.ForeignKey(User, on_delete=models.CASCADE)
#     stadium = models.ForeignKey(User, on_delete=models.CASCADE)
#     TypeOfGame = models.ForeignKey(User, on_delete=models.CASCADE)
#     #czy tu nalezy wszystko łaczyć?
#     # jak zrobić możliwość odpowiedzi na komentarz? Kolejny model i połączenie relacja OneToMany z tym modelem?
#     #gdzie powinna być informacja o sezonach? np. statystki danego zawodnika z seoznu 2016/2017
