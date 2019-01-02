from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.TextAnnotation)
admin.site.register(models.ImageAnnotation)
admin.site.register(models.Body)
admin.site.register(models.Target)
admin.site.register(models.ImageTarget)
admin.site.register(models.Selector)
admin.site.register(models.FragmentSelector)
admin.site.register(models.StartEndSelector)
admin.site.register(models.RefinedBy)

