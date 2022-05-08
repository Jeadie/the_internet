from http.client import ImproperConnectionState
from django.contrib import admin

from the_people.models import User

admin.site.register(User)
