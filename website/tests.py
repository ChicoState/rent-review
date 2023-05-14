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
        self.assertTrue(True)

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
        number_of_cities = 13
        print(City.objects.all())
        print(State.objects.all())

        CA = State.objects.create(name = "California")
        

        
        for city_id in range(number_of_cities):
            City.objects.create(
                name=f'City{city_id}',
                state=CA,
            )

    def test_view_url_exists_at_desired_location(self):
        number_of_cities = 13
        for city_id in range(number_of_cities):
            response = self.client.get(f'/City{city_id}/')
            self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
    
    def test_lists_all_cities(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('cities' in response.context)
        print("City Lookup Context")
        print(response.context['cities'])
        self.assertEqual(len(response.context['cities']), 13)


class TestcityLookupView(TestCase):
    pass
    # @classmethod
    # def setUpTestData(cls):
    #     # Create 13 authors for pagination tests
    #     city_lat = 100
    #     city_lng = 200
    #     CA = State.objects.create(name = "Arizona")
        

        
    #     for city_id in range(number_of_cities):
    #         City.objects.create(
    #             name=f'City{city_id}',
    #             state=CA,
    #         )

    # def test_view_url_exists_at_desired_location(self):
    #     number_of_cities = 13
    #     for city_id in range(number_of_cities):
    #         response = self.client.get(f'/City{city_id}/')
    #         self.assertEqual(response.status_code, 200)

    # def test_view_url_accessible_by_name(self):
    #     response = self.client.get(reverse('home'))
    #     self.assertEqual(response.status_code, 200)

    # def test_view_uses_correct_template(self):
    #     response = self.client.get(reverse('home'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'home.html')
    
    # def test_lists_all_cities(self):
    #     # Get second page and confirm it has (exactly) remaining 3 items
    #     response = self.client.get(reverse('home'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue('cities' in response.context)
    #     self.assertEqual(len(response.context['cities']), 13)



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
