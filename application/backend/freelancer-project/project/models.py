
from django.db import models

# Create your models here.



class Project(models.Model):
    '''Database fields for our projects'''
    user_id = models.ForeignKey('user.User', on_delete=models.CASCADE)          # creates a foreign key between a project and user.
                                                                                # If a user is deleted than all projects connected to
                                                                                # him/her will also deleted because of second parameter.
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)                        # auto_now_add, automatically set the field to now when the
                                                                                # object is first created. Useful for creation of timestamps.

    updated_at = models.DateTimeField(auto_now=True)                            # auto_now, automatically set the field to now every time the
                                                                                # object is saved. Useful for “last-modified” timestamps.

    tags = models.ManyToManyField('Tag', related_name='projects')               # creates a many-to-many relationship between tags and projects.
    categories = models.ManyToManyField('Category', related_name='projects')    # creates a many-to-many relationship between tags and projects.
    budget_min = models.IntegerField()
    budget_max = models.IntegerField()
    deadline = models.DateTimeField()


    def __str__(self):          # thanks to this in admin panel projects are seen with their title
        return self.title



class Tag(models.Model):
    '''Database fields for our tags'''

    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Category(models.Model):
    '''Database fields for our categories'''

    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

