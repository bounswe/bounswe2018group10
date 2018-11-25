from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.FreelancerComment)
admin.site.register(models.ClientComment)

