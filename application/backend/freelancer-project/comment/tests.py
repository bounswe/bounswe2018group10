from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from .models import FreelancerComment
from tastypie.test import ResourceTestCaseMixin

# Create your tests here.



class FreelancerCommentResourceTest(ResourceTestCaseMixin, TestCase):

    def test_get_api_json(self):
        resp = self.api_client.get('/api/v1/comment/freelancer/', format='json')
        self.assertValidJSONResponse(resp)


class ClientCommentResourceTest(ResourceTestCaseMixin, TestCase):

    def test_get_api_json(self):
        resp = self.api_client.get('/api/v1/comment/client/', format='json')
        self.assertValidJSONResponse(resp)