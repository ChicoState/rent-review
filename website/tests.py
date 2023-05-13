from django.test import TestCase
from website.models import State, City, Complex, Posts, Comments
from website.views import home, cityLookup, complexLookup, postLookup, add_post, join, user_login, user_logout, createComplex,update_latlng, extract_lat_long_via_address, load_cities
from django.urls import reverse
# Create your tests here.

class StateTestCase(TestCase):
    def setUp(self):
        State.objects.create(name = "California")
        
    def test_State_Object(self):
        CA = State.objects.get(name = "California")
        self.assertIsNotNone(CA)
        
    def test_smokefail(self):
        self.assertTrue(False)

class TestCityModel(TestCase):
    pass

class TestComplexModel(TestCase):
    pass

class TestPostsModel(TestCase):
    pass

class TestCommetsModel(TestCase):
    pass


class TestHomeView(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create 13 authors for pagination tests
        number_of_authors = 13

        for author_id in range(number_of_authors):
            Author.objects.create(
                first_name=f'Dominique {author_id}',
                last_name=f'Surname {author_id}',
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/catalog/authors/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/author_list.html')


class TestcityLookupView(TestCase):
    pass
class TestComplexLookupView(TestCase):
    pass
class TestPostLookupView(TestCase):
    pass
class TestAdd_PostView(TestCase):
    pass
class TestJoinView(TestCase):
    pass
class TestUser_LoginView(TestCase):
    pass
class TestUser_LogoutView(TestCase):
    pass
class TestCreateComplexView(TestCase):
    pass
class TestUpdate_LatlngView(TestCase):
    pass
class TestExtract_lat_long_via_addressView(TestCase):
    pass
class TestLoad_citiesView(TestCase):
    pass
