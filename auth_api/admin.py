from django.contrib import admin

from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id','id_no', 'username', 'telecom')



admin.site.register(UserProfile, UserProfileAdmin)
