from django.contrib import admin
from pages.models import *
from pages.forms import *

class SitePostAdmin(admin.ModelAdmin):
    form = SitePostForm
    
# Register your models here.
admin.site.register(MinecraftUser)
admin.site.register(DutyShiftSource)
admin.site.register(DutyShift)
admin.site.register(MinecraftServerPing)
admin.site.register(SitePost, SitePostAdmin)