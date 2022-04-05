
from django.contrib import admin
from .models import Team, History, Player, Match, Point

# Register your models here.

@admin.register(Team)
class TeamAdminClass(admin.ModelAdmin):
    list_display = ["id","team_name","team_logo","team_state"]

@admin.register(History)
class HistoryAdminClass(admin.ModelAdmin):
    list_display = ["id","matches","runs","fifties","hundreds","highest_score"]

@admin.register(Player)
class PlayerAdminClass(admin.ModelAdmin):
    list_display = ["player_first_name","player_last_name","player_jersey_number","player_country","player_image","team","history"]

@admin.register(Match)
class MatchAdminClass(admin.ModelAdmin):
    list_display = ["match_number","team1","team2","winner","looser"]


@admin.register(Point)
class PointAdminClass(admin.ModelAdmin):
    list_display = ["team","match_counter","win","defeat","point"]




