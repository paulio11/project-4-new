# Django imports
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

# My imports
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


# User sign up
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


# Edit user profile
class EditProfile(UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'edit-profile.html'

    def get_success_url(self):
        return reverse_lazy('user', kwargs={
            'user': self.object
        })


# User settings
class UserSettings(UpdateView):
    model = CustomUser
    template_name = 'user-settings.html'
    fields = ['username', 'email']
    success_url = reverse_lazy('feed')


# Change user password
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('settings', form.user.id)
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'password.html', {'form': form})
