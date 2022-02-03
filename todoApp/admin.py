from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Department)
admin.site.register(Master)
admin.site.register(Profile)
admin.site.register(Connection)
admin.site.register(ToDo)
admin.site.register(ToDoMember)

admin.site.site_header = admin.site.site_title =  'ToDo Manager'
