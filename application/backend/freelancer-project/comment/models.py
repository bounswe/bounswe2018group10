
from django.db import models

# Create your models here.



class FreelancerComment(models.Model):

    user_id = models.ForeignKey('user.User', on_delete=models.CASCADE)
    freelancer_profile_id = models.ForeignKey('user.FreelancerProfile', on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class ClientComment(models.Model):

    user_id = models.ForeignKey('user.User', on_delete=models.CASCADE)
    freelancer_profile_id = models.ForeignKey('user.ClientProfile', on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)
