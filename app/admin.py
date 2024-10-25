from django.contrib import admin
from .models import Team



class Team_display(admin.ModelAdmin):
    list_display = ('name','score',)



admin.site.register(Team, Team_display)


