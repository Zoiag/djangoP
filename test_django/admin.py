from django.contrib import admin

from test_django.models import *
''''''
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(School)
admin.site.register(Subject)

# Register your models here.
