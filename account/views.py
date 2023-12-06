from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.forms import ValidationError
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, "Вы успешно прошли аутентификацию")
                    return redirect('shop:product_list')
                else:
                    return render(request, 'account/login.html',
                                  {'form': form, 'errors': 'Этот аккаунт отключен'})
            else:
                messages.error(request, "Не удалось войти в аккаунт, введены неверные логин или пароль")
                return render(request, 'account/login.html',
                              {'form': form, 'errors': 'Неверный логин или пароль'})
        else:
            messages.error(request, "Не удалось войти в аккаунт, форма заполнена неверно")
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form, 'errors': ""})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = get_user_model()()
            if user_form.cleaned_data['first_name']:
                new_user.first_name = user_form.cleaned_data['first_name']
            new_user.username = user_form.cleaned_data['username']
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.email = user_form.cleaned_data['email']
            new_user.save()
            Profile.objects.create(user=new_user)
            messages.success(request, "Вы успешно зарегистрировались")
            return redirect('account:login')
        else:
            messages.error(request, "Не удалось зарегистрироваться, неправильно заполнена форма.")
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            new_user = user_form.save(commit=False)
            if user_form.cleaned_data['password']:
                new_user.set_password(user_form.cleaned_data['password'])
            if get_user_model().objects.filter(email=user_form.cleaned_data['email']). \
                    exclude(username=request.user.username).count() > 0:
                raise ValidationError('Пользователь с данной электронной почтой уже зарегистрирован')
            new_user.save()
            profile_form.save()
            messages.success(request, "Вы успешно изменили профиль своего аккунта")
        else:
            messages.error(request, "Не удалось изменить профиль аккаунта, неправильно заполнена форма")
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    user_profile = Profile.objects.get(user=request.user)
    return render(request, 'account/edit_profile.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'profile': user_profile})
