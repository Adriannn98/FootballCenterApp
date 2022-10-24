from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from FootballCenter_app.models import Player, Nationality, Club, PlayerInClub, TypeOfGame


def validate_password(value):
    if len(value) < 8:
        raise ValidationError("Password is too short")


def check_if_has_number(value):
    if not any(x for x in value if x.isdigit()):
        raise ValidationError("Password must have a number")


class CreateUserForm(forms.ModelForm):
    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                validators=[validate_password, check_if_has_number],
                                help_text='Password must have min. 8 charactrs')
    password2 = forms.CharField(label='re-Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        data = super().clean()
        pass1 = data.get('password1')
        if pass1 is not None and pass1 != data.get('password2'):
            raise ValidationError('Hasła nie są identyczne')
        return data


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'username', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password', 'class': 'form-control'}))


class TypeOfGameCreateForm(forms.ModelForm):
    class Meta:
        model = TypeOfGame
        fields = ['name', 'number_of_participants']



class NationalityCreateForm(forms.ModelForm):
    class Meta:
        model = Nationality
        fields = '__all__'


class PlayerCreateForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['name', 'surname', 'dob', 'height', 'value', 'leg', 'sponsor', 'nationality']


class ClubCreateForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = '__all__'


class PlayerInClubCreateForm(forms.ModelForm):
    class Meta:
        model = PlayerInClub
        fields = '__all__'
