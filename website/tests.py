from django.test import TestCase, RequestFactory
from website.models import State, City, Complex, Posts, Comments
from website.views import home, cityLookup, complexLookup, postLookup, add_post, join, user_login, user_logout, createComplex,update_latlng, extract_lat_long_via_address, load_cities, init_testSet
from django.urls import reverse


# Create your tests here.

class StateTest(TestCase):
    def setUp(self):
        State.objects.create(name = "California")
    def test_StateObject(self):
        CA = State.objects.get(name = "California")
        self.assertIsNotNone(CA)

# class TestCityModel(TestCase):
#     pass

# class TestComplexModel(TestCase):
#     pass

# class TestPostsModel(TestCase):
#     pass

# class TestCommetsModel(TestCase):
#     pass


# class TestHomeView(TestCase):
#     pass
#     # @classmethod
#     # def setUpTestData(cls):
#     #     # Create 13 authors for pagination tests
#     #     number_of_authors = 13

#     #     for author_id in range(number_of_authors):
#     #         Author.objects.create(
#     #             first_name=f'Dominique {author_id}',
#     #             last_name=f'Surname {author_id}',
#     #         )

#     # def test_view_url_exists_at_desired_location(self):
#     #     response = self.client.get('/catalog/authors/')
#     #     self.assertEqual(response.status_code, 200)

#     # def test_view_url_accessible_by_name(self):
#     #     response = self.client.get(reverse('authors'))
#     #     self.assertEqual(response.status_code, 200)

#     # def test_view_uses_correct_template(self):
#     #     response = self.client.get(reverse('authors'))
#     #     self.assertEqual(response.status_code, 200)
#     #     self.assertTemplateUsed(response, 'catalog/author_list.html')


# class TestcityLookupView(TestCase):
#     pass
# class TestComplexLookupView(TestCase):
#     pass
# class TestPostLookupView(TestCase):
#     pass
# class TestAdd_PostView(TestCase):
#     pass
# class TestJoinView(TestCase):
#     pass
# class TestUser_LoginView(TestCase):
#     pass
# class TestUser_LogoutView(TestCase):
#     pass
# class TestCreateComplexView(TestCase):
#     pass
# class TestUpdate_LatlngView(TestCase):
#     pass
# class TestExtract_lat_long_via_addressView(TestCase):
#     pass
class LoadCityTest(TestCase):
    def setUp(self):
        state = State.objects.create(name = "California")
        City.objects.create(name = 'Chico', state = state)
        City.objects.create(name = 'Roseville', state = state)
        self.id = State.objects.get(name = 'California').pk

    def test_LoadCities(self):
        response = self.client.get(reverse('ajax_load_cities'), data={'state':self.id,})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('cities' in response.context)
        self.assertEqual(len(response.context['cities']), 2)


