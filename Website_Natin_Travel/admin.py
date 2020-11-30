from django.contrib import admin
from .models import *

admin.site.register(Tours)
admin.site.register(FeaturedTours)
admin.site.register(UserApplications)
admin.site.register(AnonimUserApplications)
admin.site.register(UserInformation)