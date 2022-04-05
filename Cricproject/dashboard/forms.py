from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, UserChangeForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm

# SignupForm

class SignupForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control"}),label="Email", required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}),label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}),label="Confirm Password")
    class Meta:
        model = User
        fields = ["username","email"]
        widgets = {
            "username":forms.TextInput(attrs={"class":"form-control"})
        }

    def clean_email(self):
        val = self.cleaned_data["email"]
        if User.objects.filter(email=val).exists():
            raise forms.ValidationError("Email is already exist !")
        else:
            return val


# LoginForm

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))



# ProfileForm

class ProfileForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ["username","email","date_joined","last_login"]
        labels = {
            "email":"Email"
        }
        widgets = {
            "username":forms.TextInput(attrs={"class":"form-control"}),
            "email":forms.EmailInput(attrs={"class":"form-control"}),
            "date_joined":forms.DateTimeInput(attrs={"class":"form-control"}),
            "last_login":forms.DateTimeInput(attrs={"class":"form-control"}),
        }


# Change Password With Old Password


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}),label="Old Password")
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}),label="New Password")
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}),label="Confirm Password")


# Reset Password

class ResetPasswordForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={"class":"form-control"}))


# Reset Password Confirm

class ResetPasswordConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}),label="New Password")
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}),label="Confirm Password")
    