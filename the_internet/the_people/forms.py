from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm, UsernameField
from the_people.models import User


class UserCreationForm(BaseUserCreationForm):
    username = UsernameField(label="Email address", widget=forms.TextInput(attrs={"autofocus": True}),  )

    class Meta(BaseUserCreationForm.Meta):
        model = User
        # fields = BaseUserCreationForm.Meta.fields + ("email",)