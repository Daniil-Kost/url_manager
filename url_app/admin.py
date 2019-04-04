from django.contrib import admin
from url_app.models import Url, UserProfile

# Register your models here.
admin.site.register(Url)
admin.site.register(UserProfile)