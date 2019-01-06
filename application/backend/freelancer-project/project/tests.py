from django.test import TestCase
from .models import Tag


# Create your tests here.
# models test
class TagTest(TestCase):

    def create_tag(self, title="Photography"):
        return Tag.objects.create(title=title)

    def test_tag(self):
        t = self.create_tag()
        self.assertTrue(isinstance(t, Tag))
        self.assertEqual(t.__str__(), t.title)