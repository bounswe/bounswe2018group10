from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):

        if not email:
            raise ValueError('Users must have an email address.')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):

        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)
        return user



class User(AbstractBaseUser, PermissionsMixin):
    # Definition of different user roles, we have 'freelancer' and 'client'
    FREELANCER = 0
    CLIENT = 1
    ROLE_CHOICES = (
        (FREELANCER, 'Freelancer'),
        (CLIENT, 'Client'),
    )

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255, default="")
    username = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.IntegerField(choices=ROLE_CHOICES, default=FREELANCER)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.email


class FreelancerProfile(models.Model):
    """Profile information for freelancers"""
    type = 'FREELANCER'
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='images/', blank=True)
#    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=0)

class ClientProfile(models.Model):
    """Profile information for clients"""
    type = 'CLIENT'
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='images/', null=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=0)


    def __str__(self):
        return self.name

