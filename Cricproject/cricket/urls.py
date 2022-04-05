
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.TeamCreateAndView.as_view(), name='home'),
    path('team/', views.TeamCreateAndView.as_view(), name='team'),
    path('player/', views.PlayerCreateView.as_view(), name='player'),
    path('allplayer/', views.AllPlayerView.as_view(), name='allplayer'),
    path('teamplayers/<int:id>/', views.TeamPlayersView.as_view(), name='teamplayers'),
    path('playerdetail/<int:pk>/', views.PlayerDetailView.as_view(), name='playerdetail'),
    path('matchcreate/', views.MatchCreateView.as_view(), name='matchcreate'),
    path('matchupdate/<int:id>/', views.MatchUpdateView.as_view(), name='matchupdate'),
    path('pointtable/', views.PointTableView.as_view(), name='pointtable'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)