
from django.db import models

# Create your models here.


class UploadImage(models.Model):
    url = models.ImageField(upload_to='images/')
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)