from django.contrib import admin
from .models import User, Diary

# Register your models here.
admin.site.register(User)
admin.site.register(Diary)