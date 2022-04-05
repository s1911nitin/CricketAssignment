
from django.shortcuts import render
from django.views.generic.base import TemplateView
from .forms import TeamCreateForm, PlayerCreateForm, MatchCreateForm, MatchUpdateForm
from django.contrib import messages
from .models import Team, History, Player, Match, Point
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
import random

# Create your views here.

@method_decorator(login_required, name="dispatch")
class TeamCreateAndView(TemplateView):
    template_name = "cricket/team_create_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = TeamCreateForm()
        form.order_fields(field_order=["team_name","team_state","team_logo"])
        teams = Team.objects.all()
        context["form"] = form
        context["teams"] = teams
        return context

    def post(self,request):
        form = TeamCreateForm(request.POST,request.FILES)
        form.order_fields(field_order=["team_name","team_state","team_logo"])    
        if form.is_valid():
            form.save()
            messages.success(request,"Your team data has been saved !!")
        teams = Team.objects.all()
        return render(request,self.template_name,{"form":form,"teams":teams})



@method_decorator(staff_member_required, name="dispatch")
class PlayerCreateView(CreateView):
    template_name = "cricket/player_create.html"
    form_class = PlayerCreateForm
    success_url = "/player/"

    def get_form(self, form_class=PlayerCreateForm):
        form = super().get_form(form_class)
        form.order_fields(field_order=[
            "team",
            "player_first_name",
            "player_last_name",
            "player_jersey_number",
            "player_country",
            "player_role",
            "matches",
            "runs",
            "fifties",
            "hundreds",
            "highest_score",
        ])
        return form

    def form_valid(self, form):
        form = super().form_valid(form)
        messages.success(self.request,"Your player has been created !!")
        return form
        

@method_decorator(login_required, name="dispatch")
class AllPlayerView(ListView):
    template_name = "cricket/allplayers_view.html"
    model = Player
    context_object_name = "players"
    paginate_by = 11



@method_decorator(login_required, name="dispatch")
class TeamPlayersView(TemplateView):
    template_name = "cricket/team_players_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = kwargs["id"]
        team = Team.objects.prefetch_related('iplteam').get(pk=id)
        players = team.iplteam.all()
        context["players"] = players
        context["team"] = team
        return context


@method_decorator(login_required, name="dispatch")
class PlayerDetailView(DetailView):
    model = Player

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(kwargs)
        id = kwargs["object"].id
        player = Player.objects.select_related('history','team').get(pk=id)
        context["player"] = player
        return context

        

@method_decorator(staff_member_required, name="dispatch")
class MatchCreateView(CreateView):
    template_name = "cricket/match_create.html"
    form_class = MatchCreateForm
    success_url = "/creatematch/"

    def form_valid(self, form):
        form = super().form_valid(form)
        messages.success(self.request,"Match has been created !!")
        return form

    
@method_decorator(login_required, name="dispatch")
class MatchUpdateView(TemplateView):
    template_name = "cricket/matches_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if kwargs["id"]==1:
            current_match = Match.objects.select_related('team1','team2').get(pk=kwargs['id'])
            form = MatchUpdateForm(instance=current_match)
            fixtures = Match.objects.select_related('team1','team2').filter(id__range=(1,((current_match.id)-1)))
            self.request.session["next_match_id"]=current_match.id
            next_match_id = self.request.session["next_match_id"]
        elif kwargs["id"]>=2 and kwargs["id"]<29:
            current_match = Match.objects.select_related('team1','team2').get(pk=kwargs['id'])
            form = MatchUpdateForm(instance=current_match)
            fixtures = Match.objects.select_related('team1','team2').filter(id__range=(1,((current_match.id)-1)))
            self.request.session["next_match_id"]=current_match.id
            next_match_id = self.request.session["next_match_id"]
        elif kwargs["id"]>=29:
            current_match = None
            fixtures = None
            form = None
            self.request.session["next_match_id"]=kwargs["id"]
            next_match_id = self.request.session["next_match_id"]
        context["form"] = form
        context["current_match"]=current_match
        context["next_match_id"]=next_match_id
        context["fixtures"]=fixtures
        return context

    def post(self,request,id):
        current_match = Match.objects.select_related('team1','team2').get(pk=id)
        form = MatchUpdateForm(instance=current_match,data=request.POST)
        if form.is_valid():
            match_number = form.cleaned_data["match_number"]
            team1 = form.cleaned_data['team1']
            team2 = form.cleaned_data['team2']
            winner = random.choice([team1.team_name,team2.team_name])
            if winner == team1.team_name:
                looser = team2.team_name
            else:
                looser = team1.team_name
            Match.objects.filter(pk=current_match.id).update(match_number=match_number,team1=team1,team2=team2,winner=winner,looser=looser)
            fixtures = Match.objects.select_related('team1','team2').filter(id__range=(1,current_match.id))
            winning_team = Team.objects.get(team_name=winner)
            winning_team_obj = Point.objects.get(team=winning_team)
            winning_team_obj_match_counter = winning_team_obj.match_counter
            winning_team_obj_win_counter = winning_team_obj.win
            winning_team_obj_point_counter = winning_team_obj.point
            loosing_team = Team.objects.get(team_name=looser)
            loosing_team_obj = Point.objects.get(team=loosing_team)
            loosing_team_obj_match_counter = loosing_team_obj.match_counter
            loosing_team_obj_defeat_counter = loosing_team_obj.defeat
            if winning_team_obj_match_counter<7 and loosing_team_obj_match_counter<7:
                Point.objects.filter(team=winning_team).update(match_counter=winning_team_obj_match_counter+1,win=winning_team_obj_win_counter+1,point=winning_team_obj_point_counter+2)
                Point.objects.filter(team=loosing_team).update(match_counter=loosing_team_obj_match_counter+1,defeat=loosing_team_obj_defeat_counter+1)
            request.session["next_match_id"]=(current_match.id)+1
            next_match_id = request.session["next_match_id"]
            form = None
            if next_match_id==29:
                form = None
            messages.success(self.request,f"Your {current_match.match_number} has been played !!")
            messages.success(self.request,f"Winner is {winner}")
        else:
            fixtures = Match.objects.select_related('team1','team2').filter(id__range=(1,((current_match.id)-1)))
            request.session["next_match_id"]=None
            next_match_id = request.session["next_match_id"]
        context = {"form":form,"current_match":current_match,"fixtures":fixtures,"next_match_id":next_match_id}
        return render(request,self.template_name,context)



@method_decorator(login_required, name="dispatch")
class PointTableView(ListView):
    template_name = "cricket/point_table_view.html"
    model = Point
    context_object_name = "all_point_table"

    def get_queryset(self):
        return super().get_queryset().order_by('-point')
    









    





