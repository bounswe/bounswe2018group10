from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import filters

from .filters import ProjectFilter, BidFilter
from django_filters import rest_framework as filter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json


from . import serializers
from . import models
from . import permissions

# Create your views here.


class ProjectViewSet(viewsets.ModelViewSet):
    '''Handles reading, creating, updating and deleting projects.'''

    serializer_class = serializers.ProjectSerializer    # defines which serializer class will be use for this api
    queryset = models.Project.objects.all()             # tells the viewset how to retrieve data from database
    authentication_classes = (TokenAuthentication,)     # defines which authentication type will be used
    permission_classes = (permissions.UpdateProject, IsAuthenticatedOrReadOnly)   # defines users' permissions
    filter_backends = (filters.SearchFilter, filters.OrderingFilter, filter.DjangoFilterBackend)          # defines which filter type will be used
    search_fields = ('title', 'tags__title', 'category__title', '=user_id__id')  # to filter with a foreign key, field
                                                                                 # name in the related table must be
                                                                                  # written after name of the field
    filterset_class = ProjectFilter

    def perform_create(self, serializer):
        '''Relates the created project to the logged in user.'''
        serializer.save(user_id=self.request.user)




class TagViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TagSerializer
    queryset = models.Tag.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title',)                          # defines by which fields client can search
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title',)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)




class BidViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BidSerializer
    queryset = models.Bid.objects.all()
    filter_backends = (filters.SearchFilter, filters.OrderingFilter, filter.DjangoFilterBackend)
    search_fields = ('=project_id__id',)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateBid, IsAuthenticatedOrReadOnly,)
    filterset_class = BidFilter

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)



class MilestoneViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.MilestoneSerializer
    queryset = models.Milestone.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=bid_id__id',)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateMilestone, IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)






@api_view(['GET', 'POST'])
def semantic_search(request):
    if request.method == 'GET':
        return Response('Send Post request', status=status.HTTP_200_OK)

    if request.method != 'POST':
        return Response('Only POST method is allowed!', status=status.HTTP_405_METHOD_NOT_ALLOWED)

    else:

        saveable = serializers.SemanticSearchSerializer(data=request.data)
        if not saveable.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)


        websites_it_software = ['Django', 'Java', 'React', 'Vue', 'C']
        mobile_phones_computing = []
        translation_languages = []
        engineering_science = []
        writing_content = []
        sales_marketing = []
        photography = []
        design_media_architecture = []
        other = []

        keyword = saveable.validated_data['keyword']
        if keyword in websites_it_software:
            chosen = []
            json_posts = ''

            chosen.append(models.Project.objects.filter(tags__title=keyword).values('id',
                                                                               'title',
                                                                               'description',
                                                                               'budget_min',
                                                                               'budget_max',
                                                                               'category'))
            if json.dumps(list(chosen[0])) == '[]':
                del chosen[0]
            else:
                json_posts = json.dumps(list(chosen[0]))
                del chosen[0]


            chosen.append(models.Project.objects.filter(title__icontains=keyword).exclude(tags__title=keyword)
                                                                                 .values('id',
                                                                                         'title',
                                                                                         'description',
                                                                                         'budget_min',
                                                                                         'budget_max',
                                                                                         'category'))
            if json.dumps(list(chosen[0])) == '[]':
                del chosen[0]
            else:
                json_posts = json_posts + json.dumps(list(chosen[0]))
                del chosen[0]

            chosen.append(models.Project.objects.filter(description__icontains=keyword)
                                                .exclude(tags__title=keyword)
                                                .exclude(title__icontains=keyword)
                                                .values('id',
                                                        'title',
                                                        'description',
                                                        'budget_min',
                                                        'budget_max',
                                                        'category'))
            if json.dumps(list(chosen[0])) == '[]':
                del chosen[0]

            else:
                json_posts = json_posts + json.dumps(list(chosen[0]))
                del chosen[0]

            chosen.append(models.Project.objects.filter(category__title='Software')
                                                .exclude(tags__title=keyword)
                                                .exclude(title__icontains=keyword)
                                                .exclude(description__icontains=keyword)
                                                .values('id',
                                                        'title',
                                                        'description',
                                                        'budget_min',
                                                        'budget_max',
                                                        'category'))

            if json.dumps(list(chosen[0])) == '[]':
                del chosen[0]
            else:
                json_posts = json_posts + json.dumps(list(chosen[0]))
                del chosen[0]



            json_posts = json_posts.replace("\"", "")
            return Response(json_posts)





        return Response({'message':'No related answer is found'})



