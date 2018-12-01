from django.db import models

# Create your models here.

class Wallet(models.Model):
    user_id = models.ForeignKey('user.User', on_delete=models.CASCADE)
    budget = models.IntegerField(default=0, blank=True)


class Payment(models.Model):
    acceptedproject_id = models.ForeignKey('acceptedProject.AcceptedProject', on_delete=models.CASCADE)
    amount = models.IntegerField()