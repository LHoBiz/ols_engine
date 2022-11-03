from django.contrib import admin

from .models import Aerodrome
admin.site.register(Aerodrome)

from .models import Runway
admin.site.register(Runway)

