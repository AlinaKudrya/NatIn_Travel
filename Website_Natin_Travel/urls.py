from django.urls import path
from .views import *
from django.views.generic import TemplateView

urlpatterns = [
    path('delete-featured-tour-<int:pk>', delete_featured_tour, name='delete-featured-tour'),
    path('account', my_information, name='account'),
    path('account/applications', my_applications, name='my-applications'),
    path('account/featured-tours', featured_tours_list, name='featured-tours'),
    path('application-<int:pk>', application, name='application'),
    path('<int:pk>', tour_detail, name='tour_detail'),
    path('register', register, name='register'),
    path('logout', logout, name='logout'),
    path('login', login, name='login'),
    path('contacts', contacts, name='contacts'),
    path('aviatours', aviatours_view, name='aviatours_view'),
    path('mountains', mountains_view, name='mountains'),
    path('sea-and-beach', sea_and_beach_view, name='sea_and_beach'),
    path('bus-tours', bus_tours_view, name='bus_tours'),
    path('weekends', weekends_view, name='weekends'),
    path('without-night-crossings', without_night_crossings_view, name='tours_without_night_crossings'),
    path('cruises', cruises_view, name='cruises'),
    path('', send_message, name='send_message'),
    path('', TemplateView.as_view(template_name='base.html'), name='main')
]