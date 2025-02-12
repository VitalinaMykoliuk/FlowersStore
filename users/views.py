from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.contrib.auth import login
from django.contrib import auth
from .forms import UserRegistrationForm, UserLoginForm, UserAccountForm
from django.urls import reverse_lazy
from django.contrib.auth.models import AnonymousUser


class RegisterView(View):
    template_name = 'users/registration.html'

    def get(self, request):
        form = UserRegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse('product_cat'))
        else:
            print(form.errors)
        return render(request, self.template_name, {'form': form})


class LoginUserView(View):

    template_name = 'users/authorization.html'

    def get(self, request):
        form = UserLoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserLoginForm(data=request.POST)
        print(form)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = auth.authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect(reverse('product_cat'))
            else:
                # Если аутентификация не удалась, отображаем форму с сообщением об ошибке
                return render(request, self.template_name,
                              {'form': form, 'error_message': 'Неверное имя пользователя или пароль'})
        else:
            form = UserLoginForm()

        return render(request, self.template_name, {'form': form})


class ProfileView(View):
    template_name = 'users/personal_account.html'
    login_url = reverse_lazy('register')

    def get(self, request):
        user = request.user
        if isinstance(user, AnonymousUser):
            user = None
        form = UserAccountForm(instance=user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        user = request.user
        print(user)
        if isinstance(user, AnonymousUser):
            user = None
        form = UserAccountForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()
            user_name = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            print(f'user_name{user_name}, email{email}')
            return HttpResponseRedirect(reverse('product_cat'))
        return render(request, self.template_name, {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('main')