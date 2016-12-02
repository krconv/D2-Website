from django.contrib import admin
from pages.models import MinecraftUser, DutyShiftSource, DutyShift

# Register your models here.
admin.site.register(MinecraftUser)
admin.site.register(DutyShiftSource)
admin.site.register(DutyShift)