
from django import forms
from .models import Team, Player, Match
from django.db.models import Q

class TeamCreateForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = "__all__"
        widgets = {
            "team_name":forms.TextInput(attrs={"class":"form-control"}),
            "team_logo":forms.ClearableFileInput(attrs={"class":"form-control"}),
            "team_state":forms.TextInput(attrs={"class":"form-control"})
        }
        labels = {
            "team_name":"Team",
            "team_logo":"",
            "team_state":"State"
        }


class PlayerCreateForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = "__all__"
        widgets = {
            "player_first_name":forms.TextInput(attrs={"class":"form-control"}),
            "player_last_name":forms.TextInput(attrs={"class":"form-control"}),
            "player_jersey_number":forms.NumberInput(attrs={"class":"form-control"}),
            "player_country":forms.TextInput(attrs={"class":"form-control"}),
            "player_role":forms.TextInput(attrs={"class":"form-control"}),
            "player_image":forms.ClearableFileInput(attrs={"class":"form-control"}),
            "matches":forms.NumberInput(attrs={"class":"form-control"}),
            "runs":forms.NumberInput(attrs={"class":"form-control"}),
            "fifties":forms.TextInput(attrs={"class":"form-control"}),
            "hundreds":forms.TextInput(attrs={"class":"form-control"}),
            "highest_score":forms.TextInput(attrs={"class":"form-control"}),
        }
        labels = {
            "player_first_name":"First Name",
            "player_last_name":"Last Name",
            "player_jersey_number":"Jersey Number",
            "player_country":"Country",
            "player_role":"Role"
        }


class MatchCreateForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = "__all__"

        widgets = {
            "match_number":forms.TextInput(attrs={"class":"form-control"}),
            "winner":forms.TextInput(attrs={"class":"form-control"}),
            "looser":forms.TextInput(attrs={"class":"form-control"}),
        }
        
class MatchUpdateForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ["match_number","team1","team2"]
        widgets = {
            "match_number":forms.HiddenInput()
        }


    def clean(self):
        cleaned_data = super().clean()
        val = cleaned_data["match_number"]
        val1 = cleaned_data["team1"]
        val2 = cleaned_data["team2"]
        id = int(val.split("h")[1])
        Queryset_team1 = Match.objects.filter(id__range=(1,id)).filter(Q(team1=val1)|Q(team2=val1))
        Queryset_team2 = Match.objects.filter(id__range=(1,id)).filter(Q(team1=val2)|Q(team2=val2))
        Already_done_match = Match.objects.filter(id__range=(1,id-1)).filter((Q(team1=val1)&Q(team2=val2))|(Q(team1=val2)&Q(team2=val1)))
        if val1 == val2:
            raise forms.ValidationError("Please make sure not to select the same team !!")
        elif Already_done_match.exists():
            if (Queryset_team1.exists() and len(Queryset_team1)==7) and (Queryset_team2.exists() and len(Queryset_team2)==7):
                raise forms.ValidationError(f"This match has been played & {val1} and {val2} have already played their 7 matches, so choose diff teams !!")
            elif Queryset_team1.exists() and len(Queryset_team1)==7:
                raise forms.ValidationError(f"This match has been played & {val1} has played 7 matches already, please choose diff team !!")
            elif Queryset_team2.exists() and len(Queryset_team2)==7:
                raise forms.ValidationError(f"This match has been played & {val2} has played 7 matches already, please choose diff team !!")
            else:
                raise forms.ValidationError("This match has been played already !!")
        
