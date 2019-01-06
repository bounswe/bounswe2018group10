from django.test import TestCase
from .models import Tag
from tastypie.test import ResourceTestCaseMixin

# Create your tests here.


class TagTest(TestCase):

    def create_tag(self, title="Photography"):
        return Tag.objects.create(title=title)

    def test_tag(self):
        t = self.create_tag()
        self.assertTrue(isinstance(t, Tag))
        self.assertEqual(t.__str__(), t.title)


class CatagoryResourceTest(ResourceTestCaseMixin, TestCase):

    def test_get_api_json(self):
        resp = self.api_client.get('/api/v1/project/category/', format='json')
        self.assertValidJSONResponse(resp)


class ProjectResourceTest(ResourceTestCaseMixin, TestCase):

    def test_get_api_json(self):
        resp = self.api_client.get('/api/v1/project/create/', format='json')
        self.assertValidJSONResponse(resp)


