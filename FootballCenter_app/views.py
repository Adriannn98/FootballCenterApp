from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views import View

from FootballCenter_app.forms import CreateUserForm, LoginForm, TypeOfGameCreateForm, PlayerCreateForm, \
    NationalityCreateForm, ClubCreateForm, PlayerInClubCreateForm
from FootballCenter_app.models import TypeOfGame, Nationality, Player, Club, PlayerInClub


class IndexView(View):

    def get(self, request):
        return render(request, 'base.html')


class CreateUserView(View):

    def get(self, request):
        form = CreateUserForm()
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save(
                commit=False)
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.save()
            return redirect('/')
        return render(request, 'form.html', {'form': form})


class LoginView(View):

    def get(self, request):
        form = LoginForm()
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is None:
                return render(request, 'form.html', {'form': form, 'message': 'Incorrect data'})
            else:
                login(request, user)
                url = request.GET.get('next', 'index')
                return redirect(url)
        return render(request, 'form.html', {'form': form, 'message': 'Incorrect data'})


class LoginOutView(View):

    def get(self, request):
        logout(request)
        return redirect('index')


class AddTypeOfGameView(UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request):
        form = TypeOfGameCreateForm()
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = TypeOfGameCreateForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('add_type_of_game')
        return render(request, 'form.html', {'form': form})


class TypeOfGameListView(View):

    def get(self, request):
        type_of_games = TypeOfGame.objects.all()
        return render(request, 'type_of_game_list.html', {'type_of_games': type_of_games})


class AddNationality(UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request):
        form = NationalityCreateForm()
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = NationalityCreateForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('add_nationality')
        return render(request, 'form.html', {'form': form})


class NationalityListView(View):

    def get(self, request):
        nationalities = Nationality.objects.all()
        return render(request, 'nationalities_list.html', {'nationalities': nationalities})


class AddPlayerView(UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request):
        form = PlayerCreateForm()
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = PlayerCreateForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('add_player')
        return render(request, 'form.html', {'form': form})


class AddClubView(UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request):
        form = ClubCreateForm()
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = ClubCreateForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('add_club')
        return render(request, 'form.html', {'form': form})


class ClubDetailView(View):

    def get(self, request, id_club):
        club = Club.objects.get(pk=id_club)
        club.player_set.all()

        return render(request, 'club_detail.html', {'club': club})


class AddPlayerInClubView(UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request):
        form = PlayerInClubCreateForm()
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = PlayerInClubCreateForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('add_player_in_club')
        return render(request, 'form.html', {'form': form})


class PlayerDetailView(View):

    def get(self, request, id_player):
        player = Player.objects.all().get(pk=id_player)
        return render(request, 'player_detail.html', {'player': player})


class TypeOfGameDetailView(View):

    def get(self, request, id_type_of_game):
        type_of_game = TypeOfGame.objects.get(pk=id_type_of_game)
        clubs = type_of_game.club.all()
        return render(request, 'type_of_game_detail.html', {'clubs': clubs, 'type_of_game': type_of_game})


class AddClubToTypeOfGameView(UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, id_type_of_game):
        type_of_game = TypeOfGame.objects.get(pk=id_type_of_game)
        clubs = Club.objects.all()

        return render(request, 'club_list.html', {'clubs': clubs, 'type_of_game': type_of_game})

    def post(self, request, id_type_of_game):
        club_id = request.POST.get('club_id')

        type_of_game = TypeOfGame.objects.get(pk=id_type_of_game)
        type_of_game.club.add(club_id)

        url = reverse('type_of_game_detail', args=(type_of_game.id,))
        return redirect(url)


class DeleteClubFromTypeOfGameView(UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, type_of_game_id, club_id):
        type_of_game = TypeOfGame.objects.get(pk=type_of_game_id)
        club = Club.objects.get(pk=club_id)

        return render(request, 'delete_club_from_tog.html', {'type_of_game': type_of_game, 'club': club})

    def post(self, request, type_of_game_id, club_id):
        type_of_game = TypeOfGame.objects.get(pk=type_of_game_id)
        club = Club.objects.get(pk=club_id)
        type_of_game.club.remove(club)

        url = reverse('type_of_game_detail', args=(type_of_game.id,))
        return redirect(url)


class ModifyPlayerView(UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, player_id):
        player = Player.objects.get(pk=player_id)
        form = PlayerCreateForm(instance=player)
        return render(request, 'form.html', {'form': form})

    def post(self, request, player_id):
        player = Player.objects.get(pk=player_id)
        form = PlayerCreateForm(request.POST, instance=player)
        if form.is_valid():
            form.save()
            url = reverse('player_detail', args=(player_id,))
            return redirect(url)


class DeleteTypeOfGameView(UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, type_of_game_id):
        type_of_game = TypeOfGame.objects.get(pk=type_of_game_id)

        return render(request, 'delete_type_of_game.html', {'type_of_game': type_of_game})

    def post(self, request, type_of_game_id):
        type_of_game = TypeOfGame.objects.get(pk=type_of_game_id)
        type_of_game.delete()

        url = reverse('type_of_game_list')
        return redirect(url)


class ModifyTypeOfGameView(UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, type_of_game_id):
        type_of_game = TypeOfGame.objects.get(pk=type_of_game_id)
        form = TypeOfGameCreateForm(instance=type_of_game)
        return render(request, 'form.html', {'form': form})

    def post(self, request, type_of_game_id):
        type_of_game = TypeOfGame.objects.get(pk=type_of_game_id)
        form = TypeOfGameCreateForm(request.POST, instance=type_of_game)
        if form.is_valid():
            form.save()
            url = reverse('type_of_game_list')
            return redirect(url)
