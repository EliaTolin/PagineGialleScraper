from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import UserProfile

# Register your models here.
@admin.register(UserProfile)
class CustomerAdmin(UserAdmin):
    list_display = ('username','first_name','last_name','email','region','phone')
    fieldsets = UserAdmin.fieldsets + (('Extra fields', {'fields': ('region', 'phone')}),)