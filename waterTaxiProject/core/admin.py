# myapp/admin.py
from django.contrib import admin
from .models import Ticket, Emergency, Schedule

admin.site.register(Ticket)
admin.site.register(Emergency)
admin.site.register(Schedule)
