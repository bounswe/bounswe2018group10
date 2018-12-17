import django_filters

from .models import Project, Bid


class ProjectFilter(django_filters.FilterSet):
    class Meta:
        model = Project
        fields = {
            'budget_min': ['lte', 'gte'],
            'budget_max': ['lte', 'gte'],
            'deadline': ['lte', 'gte' ,'year__lte', 'year__gte'],
        }


class BidFilter(django_filters.FilterSet):
    class Meta:
        model = Bid
        fields = {
            'amount': ['lte', 'gte'],
        }
