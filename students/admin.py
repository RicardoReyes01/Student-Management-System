from django.contrib import admin
from .models import Student, Announcement, Grade

# Register your models here.
admin.site.register(Student)
admin.site.register(Announcement)
admin.site.register(Grade)