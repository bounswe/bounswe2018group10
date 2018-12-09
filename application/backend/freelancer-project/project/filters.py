import django_filters

from .models import Project, Bid


class ProjectFilter(django_filters.FilterSet):
    class Meta:
        model = Project
        fields = {
            'budget_min': ['lt', 'gt'],
            'budget_max': ['lt', 'gt'],
            'deadline': ['lt', 'gt' ,'year__lt', 'year__gt'],
        }


class BidFilter(django_filters.FilterSet):
    class Meta:
        model = Bid
        fields = {
            'amount': ['lt', 'gt'],
        }