from urllib import request
from django.contrib.auth.signals import user_logged_out
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Point

@receiver(user_logged_out,sender=User)
def recevier_func(sender,request,user,**kwargs):
    """Docstring: This signal will update the point table at 0000 once the authenticated user is logged out"""
    all_point_table = Point.objects.all()
    all_point_table.update(match_counter=0,win=0,defeat=0,point=0)
    print("Sender:",sender)
    print("Request:",request)
    print("Logout_user:",user.username)
    print("Kwargs:",f"{kwargs}")

