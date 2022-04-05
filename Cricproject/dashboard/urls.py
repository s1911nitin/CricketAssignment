
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignupFormView.as_view(), name='signup'),
    path('login/', views.LoginFormView.as_view(), name='login'),
    path('profile/', views.ProfileFormView.as_view(), name='profile'),
    path('logout/', views.LogoutFormView.as_view(), name='logout'),
    path('changepassword/', views.ChangePasswordFormView.as_view(), name='changepassword'),
    path('changepassworddone/', views.ChangePasswordDoneFormView.as_view(), name='changepassworddone'),
    path('resetpassword/', views.ResetPasswordFormView.as_view(), name='resetpassword'),
    path('resetpassworddone/', views.ResetPasswordDoneFormView.as_view(), name='resetpassworddone'),
    path('reset/<uidb64>/<token>/', views.ResetPasswordConfirmFormView.as_view(),name='password_reset_confirm'),
    path('resetpasswordcomplete/', views.ResetPasswordCompleteFormView.as_view(),name='resetpasswordcomplete'),
]