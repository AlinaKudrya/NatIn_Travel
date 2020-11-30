from datetime import datetime

from django import http
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template.context_processors import csrf

from NatIn_Travel.settings import DEFAULT_FROM_EMAIL
from .models import *
from Website_Natin_Travel.forms import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth


def aviatours_view(request):
    aviatours = Tours.objects.filter(category="Авиатуры")
    return render(request, 'aviatours.html', {"aviatours_list": aviatours})


def bus_tours_view(request):
    bus_tours = Tours.objects.filter(category="Автобусные туры")
    return render(request, 'bus_tours.html', {"bus_tours": bus_tours})


def cruises_view(request):
    cruises = Tours.objects.filter(category="Морские круизы")
    return render(request, 'cruises.html', {"cruises": cruises})


def mountains_view(request):
    mountains = Tours.objects.filter(category="Горы")
    return render(request, 'mountains.html', {"mountains": mountains})


def without_night_crossings_view(request):
    tours_without_night_crossings = Tours.objects.filter(category="Без ночных")
    return render(request, 'without_night_crossings.html',
                  {"tours_without_night_crossings": tours_without_night_crossings})


def sea_and_beach_view(request):
    sea_and_beach = Tours.objects.filter(category="Море")
    return render(request, 'sea_and_beach.html',
                  {"sea_and_beach": sea_and_beach})


def weekends_view(request):
    weekends = Tours.objects.filter(category="Выходные")
    return render(request, 'weekends.html', {"weekends": weekends})


def send_message(request):
    if request.POST:
        email = request.POST.get('email', '')
        sender = request.POST.get('sender', '')
        message = request.POST.get('message', '')

        recipients = ['alinka1.98@mail.ru']

        try:
            send_mail(f'Cообщение от: {sender}', f'Имя: {sender}\nE-mail: {email}\nСообщение: {message}',
                      DEFAULT_FROM_EMAIL, recipients)
            HttpResponseRedirect('/')
        except BadHeaderError:
            return HttpResponse('Error')
    return render(request, 'base.html')


def contacts(request):
    if request.POST:
        email = request.POST.get('email', '')
        sender = request.POST.get('sender', '')
        message = request.POST.get('message', '')

        recipients = ['alinka1.98@mail.ru']

        try:
            send_mail(f'Cообщение от: {sender}', f'Имя: {sender}\nE-mail: {email}\nСообщение: {message}',
                      DEFAULT_FROM_EMAIL, recipients)
            HttpResponseRedirect('contacts')
        except BadHeaderError:
            return HttpResponse('Error')
    return render(request, 'contacts.html')


def register(request):
    args = {}
    args.update(csrf(request))
    args['form'] = UserCreationForm()
    if request.POST:
        new_user_form = UserCreationForm(request.POST)
        if new_user_form.is_valid():
            new_user_form.save()
            new_user = auth.authenticate(username=new_user_form.cleaned_data['username'],
                                         password=new_user_form.cleaned_data['password1'])
            auth.login(request, new_user)
            new_user_information = UserInformation(username=request.user, name="", email="", phone="")
            new_user_information.save()
            return redirect('/')
        else:
            args['form'] = new_user_form
    return render(request, 'register.html', args)


def login(request):
    args = {}
    args.update(csrf(request))
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            args['login_error'] = "Пользователь не найден"
            return render(request, 'login.html', args)
    else:
        return render(request, 'login.html', args)


def logout(request):
    auth.logout(request)
    return redirect('/')


def my_information(request):
    my_information = UserInformation.objects.filter(username=request.user)
    if request.POST:
        my_information_edit = get_object_or_404(UserInformation, username=request.user)
        my_information_edit.name = request.POST.get('name', '')
        my_information_edit.email = request.POST.get('email', '')
        my_information_edit.phone = request.POST.get('phone', '')
        my_information_edit.save()
    return render(request, 'account.html', {'my_information': my_information})


def my_applications(request):
    applications = UserApplications.objects.all()
    return render(request, 'my_applications.html', {'applications': applications})


def application(request, pk):
    tour = Tours.objects.get(pk=pk)
    if request.POST:
        tour_title = request.POST.get('tour_title', '')
        sender = request.POST.get('name', '')
        phone = request.POST.get('phone', '')
        message = f'Заявка на тур "{tour_title}"\nОт: {sender}\nНомер телефона: {phone} '
        additionally = 'Дополнительно: ' + request.POST.get('additionally', '')

        recipients = ['alinka1.98@mail.ru']
        try:
            if request.user.is_authenticated:
                new_application = UserApplications(date=datetime.now(),
                                                   tour_title=tour_title, username=request.user)
                new_application.save()
                send_mail('Новая заявка: ' + tour_title, message + '\n' + additionally,
                          DEFAULT_FROM_EMAIL, recipients)
                return redirect('account')
            else:
                new_application = AnonimUserApplications(date=datetime.now(),
                                                         tour_title=tour_title, name=sender)
                new_application.save()
                send_mail('Новая заявка: ' + tour_title, message + '\n' + additionally,
                          DEFAULT_FROM_EMAIL, recipients)
                return redirect('/')
        except BadHeaderError:
            return HttpResponse('Error')
    if request.user.is_authenticated:
        my_information = UserInformation.objects.filter(username=request.user)
        return render(request, 'application.html', {'tour': tour, 'my_information': my_information})
    else:
        return render(request, 'application.html', {'tour': tour})


def featured_tours_list(request):
    if request.user.is_authenticated:
        featured_tours = FeaturedTours.objects.all()
        return render(request, 'featured_tours.html', {'featured_tours': featured_tours})
    else:
        return redirect('/')


def tour_detail(request, pk):
    tour = Tours.objects.get(pk=pk)
    if request.POST:
        if request.user.is_authenticated:
            if not FeaturedTours.objects.filter(tour=tour, username=request.user).exists():
                featured_tour = FeaturedTours(tour=tour, username=request.user)
                featured_tour.save()
        else:
            return redirect('login')
    return render(request, 'tour_detail.html', {'tour': tour})


def delete_featured_tour(request, pk):
    featured_tour = FeaturedTours.objects.get(pk=pk)
    featured_tour.delete()
    return redirect('featured-tours')
