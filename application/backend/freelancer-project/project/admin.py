from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Project)    # add project model to admin panel
admin.site.register(models.Tag)
admin.site.register(models.Category)
admin.site.register(models.Bid)
admin.site.register(models.Milestone)