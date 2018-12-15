from rest_framework import filters
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from django_filters import rest_framework as filter

from project.models import Project, Milestone, Bid
from user.models import User
from . import models
from . import permissions
from . import serializers


# Create your views here.


@api_view(['GET', 'POST'])
def acceptProject(request):
    if request.method == 'GET':
        return Response(status=status.HTTP_200_OK)

    if request.method != 'POST':
        return Response('Only POST method is allowed!', status=status.HTTP_405_METHOD_NOT_ALLOWED)

    saveable = serializers.ModelForBackendSerializer(data=request.data)
    if not saveable.is_valid():
        return Response(status=status.HTTP_400_BAD_REQUEST)


    accepted_bid = saveable.validated_data['accepted_bid']
    chosen_bid = Bid.objects.filter(id=accepted_bid)
    price = chosen_bid.values_list('amount',flat=True)[0]
    freelancer = User.objects.get(id=chosen_bid.values_list('user_id', flat=True)[0])
    accepted_project = Project.objects.get(id=chosen_bid.values_list('project_id', flat=True)[0])


    transferrable = [
        'user_id',
        'title',
        'description',
        'created_at',
        'updated_at',
        'deadline',
        'file',
        'latitude',
        'longitude',
    ]

    accepted_data = {key: getattr(accepted_project, key)
                     for key in transferrable}

    accepted_data.update(freelancer_id=freelancer,
                         price=price,
                         accepted_bid=accepted_bid)

    accepted = models.AcceptedProject.objects.create(**accepted_data)




    accepted_milestones = Milestone.objects.filter(bid_id=accepted_bid)
    number_of_accepted_milestones = len(accepted_milestones)
    for x in range(number_of_accepted_milestones):
        transferrable_milestone = [
            'user_id',
            'description',
            'amount',
            'created_at',
            'updated_at',
            'deadline',
        ]
        accepted_milestone_data = {key: getattr(accepted_milestones[x], key)
                              for key in transferrable_milestone}

        accepted_milestone_data.update(acceptedproject_id=accepted)
        models.AcceptedMilestone.objects.create(**accepted_milestone_data)


    serialized = serializers.AcceptedProjectSerializer(accepted)
    return Response(serialized.data, status=status.HTTP_201_CREATED)



class AcceptedProjectViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AcceptedProjectSerializer
    queryset = models.AcceptedProject.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateAcceptedProject, IsAuthenticatedOrReadOnly)
    #filter_backends = (filters.SearchFilter,)
    #search_fields = ('title', '=user_id__id', '=freelancer_id__id')
    filter_backends = (filter.DjangoFilterBackend,)
    filter_fields = ('deadline', 'price', 'user_id__id', 'freelancer_id__id')

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)


class AcceptedMilestoneViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AcceptedMilestoneSerializer
    queryset = models.AcceptedMilestone.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=acceptedproject_id__id',)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateAcceptedMilestone, IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)
