
from django.db import models

# Create your models here.

class Team(models.Model):
    team_name = models.CharField(max_length=100,unique=True)
    team_logo = models.ImageField(upload_to="teamimages")
    team_state = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.team_name

class History(models.Model):
    matches = models.PositiveIntegerField()
    runs = models.PositiveIntegerField()
    fifties = models.CharField(max_length=50)
    hundreds = models.CharField(max_length=50)
    highest_score = models.CharField(max_length=50)

    def __str__(self):
        return str(self.id)


class Player(History):
    history = models.OneToOneField(History,on_delete=models.CASCADE,parent_link=True,related_name='playerhistory',primary_key=True)
    team = models.ForeignKey(Team,on_delete=models.SET_NULL,null=True,related_name='iplteam')
    player_first_name = models.CharField(max_length=100)
    player_last_name = models.CharField(max_length=100)
    player_jersey_number = models.PositiveIntegerField(unique=True)
    player_country = models.CharField(max_length=50)
    player_role = models.CharField(max_length=50,default="Batsman")
    player_image = models.ImageField(upload_to="playerimages")

    def full_name(self):
        return f"{self.player_first_name} {self.player_last_name}"




class Match(models.Model):
    match_number = models.CharField(max_length=50)
    team1 = models.ForeignKey(Team,on_delete=models.CASCADE,related_name='matchteam1')
    team2 = models.ForeignKey(Team,on_delete=models.CASCADE,related_name='matchteam2')
    winner = models.CharField(max_length=50)
    looser = models.CharField(max_length=50)



class Point(models.Model):
    team = models.OneToOneField(Team,on_delete=models.CASCADE,primary_key=True,related_name='iplteampoint')
    match_counter = models.PositiveIntegerField(default=7)
    win = models.PositiveIntegerField()
    defeat = models.PositiveIntegerField()
    point = models.PositiveIntegerField()

