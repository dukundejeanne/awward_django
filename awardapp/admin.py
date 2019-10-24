from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Profile,Comment,Project

admin.site.register(Profile)
admin.site.register(Comment)
# admin.site.register(Followers)
admin.site.register(Project)