from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.edit import CreateView
from .forms import SignupForm, LoginForm, ProfileForm, ChangePasswordForm, ResetPasswordForm, ResetPasswordConfirmForm
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import urls
# Create your views here.


# SignupFormView

class SignupFormView(CreateView):
    template_name = "dashboard/signup.html"
    form_class = SignupForm
    success_url = "/signup/"

    def form_valid(self, form):
        messages.success(self.request,"You are successfully registered !!")
        return super().form_valid(form)


# LoginFormView

class LoginFormView(LoginView):
    template_name = "dashboard/login.html"
    form_class = LoginForm
    success_url = "/profile/"

    def get(self,request):
        if not request.user.is_authenticated:
            form = LoginForm()
            return render(request,self.template_name,{"form":form})
        else:
            return HttpResponseRedirect("/profile/")
        



# ProfileFormView

@method_decorator(login_required,name='dispatch')
class ProfileFormView(TemplateView):
    template_name = "dashboard/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = ProfileForm(instance=self.request.user)
        context["form"] = form
        return context

    def post(self,request):
        form = ProfileForm(instance=request.user, data=request.POST)
        print(form)
        if form.is_valid():
            form.save()
            messages.success(self.request,"Your profile has been updated successfully !!")
        return HttpResponseRedirect("/profile/")


# LogoutFormView

@method_decorator(login_required,name='dispatch')
class LogoutFormView(LogoutView):
    template_name = "dashboard/logout.html"


# ChangePasswordFormView

@method_decorator(login_required,name='dispatch')
class ChangePasswordFormView(PasswordChangeView):
    template_name = "dashboard/changepassword.html"
    form_class = ChangePasswordForm
    success_url = "/changepassworddone/"

    def form_valid(self, form):
        messages.success(self.request,"Your password is changed now !!")
        return super().form_valid(form)


# ChangePasswordDoneFormView

@method_decorator(login_required,name='dispatch')
class ChangePasswordDoneFormView(PasswordChangeDoneView):
    template_name = "dashboard/changepassworddone.html"


# ResetPasswordFormView

class ResetPasswordFormView(PasswordResetView):
    template_name = "dashboard/resetpassword.html"
    form_class = ResetPasswordForm
    success_url = "/resetpassworddone/"


# ResetPasswordDoneFormView

class ResetPasswordDoneFormView(PasswordResetDoneView):
    template_name = "dashboard/resetpassworddone.html"


# ResetPasswordConfirmFormView

class ResetPasswordConfirmFormView(PasswordResetConfirmView):
    template_name = "dashboard/resetpasswordconfirm.html"
    form_class = ResetPasswordConfirmForm
    success_url = "/resetpasswordcomplete/"

    def form_valid(self, form):
        messages.success(self.request,"Your password is reset now !!")
        return super().form_valid(form)

# ResetPasswordCompleteFormView

class ResetPasswordCompleteFormView(PasswordResetCompleteView):
    template_name = "dashboard/resetpasswordcomplete.html"


