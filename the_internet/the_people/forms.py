from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm, UsernameField
from the_people.models import User
from django_countries.fields import CountryField


class UserCreationForm(BaseUserCreationForm):
    # Use username variable to override main in BaseUserCreationForm
    username = UsernameField(label="Email address", widget=forms.TextInput(attrs={"autofocus": True}),  )

    country_of_work = CountryField(blank=True)

    class Meta(BaseUserCreationForm.Meta):
        model = User
        # fields = BaseUserCreationForm.Meta.fields + ("email",)