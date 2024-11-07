from django.contrib import admin
from .models import Registration
 
class Register_Admin(admin.ModelAdmin):
    list_display = ['name','department','campus']
admin.site.register(Registration,Register_Admin)
