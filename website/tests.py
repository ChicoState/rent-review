from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import User
from website.models import State, City, Complex, Posts, Comments
from website.views import home, cityLookup, complexLookup, postLookup, add_post, join, user_login, user_logout, createComplex,update_latlng, extract_lat_long_via_address, load_cities, init_testSet
from django.urls import reverse
from django.contrib import auth



# Create your tests here.

class StateTest(TestCase):
    def setUp(self):
        State.objects.create(name = "California")
    def test_StateObject(self):
        CA = State.objects.get(name = "California")
        self.assertIsNotNone(CA)
        
    def test_smokefail(self):
        self.assertTrue(True)

# class TestCityModel(TestCase):
#     pass

# class TestComplexModel(TestCase):
#     pass

# class TestPostsModel(TestCase):
#     pass

# class TestCommetsModel(TestCase):
#     pass



class TestHomeView(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create 13 authors for pagination tests
        number_of_cities = 13

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
    
    def test_post_with_valid_city(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.post(reverse('home'), data={"city_input":"City0"})
        self.assertRedirects(response, '/City0/', status_code=302, 
            target_status_code=200, fetch_redirect_response=True)
    
    def test_post_with_invalid_city(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.post(reverse('home'), data={"city_input":"NOTACITY"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_invalid_post(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.post(reverse('home'), data={"city_input":""})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

class TestcityLookupView(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 authors for pagination tests
        number_of_complexs = 3

        CA = State.objects.create(name = "California")
        city = City.objects.create(name = "TestCity", state=CA)

        
        for complex_id in range(number_of_complexs):
            Complex.objects.create(
                complex_name=f'Complex{complex_id}',
                city_name=city,
                address=f'62{complex_id} Pomona Ave',
                url = 'https://forums.linuxmint.com/viewtopic.php?t=306206',
                zipcode=95928,

            )

    def test_view_url_exists_at_desired_location(self):
        
        response = self.client.get('/TestCity/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('city_lookup', args=['TestCity']))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('city_lookup', args=['TestCity']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'complexDisplay.html')
    
    def test_lists_all_cities(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse('city_lookup', args=['TestCity']))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('cities' in response.context)
        print("City Lookup Context")
        print(response.context['cities'])
        self.assertEqual(len(response.context['cities']), 3)
    
    def test_no_city_input(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse('city_lookup', args=['NotACity']))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('cities' in response.context)
        self.assertTrue('city_center' in response.context)
        print("City Lookup Context")
        print(response.context['cities'])
        self.assertEqual(response.context['city_center'][0], 0)
        self.assertEqual(response.context['city_center'][1], 0)
        self.assertEqual(len(response.context['cities']), 0)
class TestComplexLookupView(TestCase):
    @classmethod
    def setUpTestData(self):
        # Create 13 authors for pagination tests
        number_of_posts = 3

        CA = State.objects.create(name = "California")
        city = City.objects.create(name = "TestCity", state=CA)

        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user1.save()

        complex = Complex.objects.create(
                complex_name='TestComplex',
                city_name=city,
                address='622 Pomona Ave',
                url = 'https://forums.linuxmint.com/viewtopic.php?t=306206',
                zipcode=95928,

            )
        
        self.complex_id = complex.id
        

        for complex_id in range(number_of_posts):
            Posts.objects.create(
                user = test_user1,
                complex = complex,
                post_title = "TEsting",
                post_text = "TEsting",
                likes = complex_id*2,
                strictness = complex_id*2,
                amennities = complex_id*2,
                accessibility = complex_id*2,
                maintenence = complex_id*2,
                grace_period = complex_id*2,
                staff_friendlyness = complex_id*2,
                price = complex_id*2,
    
            )

    def test_view_url_exists_at_desired_location(self):
        
        response = self.client.get(f'/TestCity/{self.complex_id}/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
    
        response = self.client.get(reverse('complexLookup', args=['TestCity', str(self.complex_id)]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('complexLookup', args=['TestCity', str(self.complex_id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'postDisplay.html')
    
    def test_average_likes_for_complex(self):
        response = self.client.get(reverse('complexLookup', args=['TestCity', str(self.complex_id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('city' in response.context)
        print("City Lookup Context")
        print(response.context['city'])
        print("Response context complex likes")
        print(response.context['complex_likes'])
        self.assertEqual(response.context['complex_likes'], 2)
    
    

class TestPostLookupView(TestCase):



    @classmethod
    def setUpTestData(self):
        # Create 13 authors for pagination tests
        number_of_posts = 3

        CA = State.objects.create(name = "California")
        city = City.objects.create(name = "TestCity", state=CA)

        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user1.save()

        complex = Complex.objects.create(
                complex_name='TestComplex',
                city_name=city,
                address='622 Pomona Ave',
                url = 'https://forums.linuxmint.com/viewtopic.php?t=306206',
                zipcode=95928,

            )
        print("created COmplex has id:")
        self.complex_id = complex.id
        self.posts = []
        print(complex.id)
        
        for post_id in range(number_of_posts):
            p = Posts.objects.create(
                user = test_user1,
                complex = complex,
                post_title = "TEsting",
                post_text = "TEsting",
                likes = post_id*2,
                strictness = post_id*2,
                amennities = post_id*2,
                accessibility = post_id*2,
                maintenence = post_id*2,
                grace_period = post_id*2,
                staff_friendlyness = post_id*2,
                price = post_id*2,
            )
            self.posts.append(p)

    def test_view_url_exists_at_desired_location(self):
        for post in self.posts:
            response = self.client.get(f'/TestCity/{self.complex_id}/{post.id}')
            self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        for post in self.posts:
            response = self.client.get(reverse('postLookup', args=['TestCity', str(self.complex_id), str(post.id)]))
            self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        for post in self.posts:
            response = self.client.get(reverse('postLookup', args=['TestCity',str(self.complex_id), str(post.id)]))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'commentDisplay.html')
    
    def test_lists_all_posts(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        for post in self.posts:
            response = self.client.get(reverse('postLookup', args=['TestCity', str(self.complex_id), str(post.id)]))
            self.assertEqual(response.status_code, 200)
            self.assertTrue('city' in response.context)
            print("City Lookup Context")
            print(response.context['city'])
            print("Response context complex likes")
            print(response.context['complex_likes'])
            self.assertEqual(response.context['complex_likes']["likes"], post.likes)
    
    def test_create_comment(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        for post in self.posts:
            response = self.client.post(reverse('postLookup', args=['TestCity', str(self.complex_id), str(post.id)]), data={"comment_text": "this is a comment"})
            self.assertEqual(response.status_code, 200)
            self.assertTrue('city' in response.context)
            
            self.assertEqual(len(response.context['comment_list']), 1)
    
    def test_create_empty_comment(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        for post in self.posts:
            response = self.client.post(reverse('postLookup', args=['TestCity', str(self.complex_id), str(post.id)]), data={"comment_text": ""})
            self.assertEqual(response.status_code, 200)
            self.assertTrue('city' in response.context)
            
            self.assertEqual(len(response.context['comment_list']), 0)

# class TestAdd_PostView(TestCase):
#     pass
class TestJoinView(TestCase):
    def setUp(self):
        pass
    def test_getreq(self):
        response = self.client.post(reverse('join'))        
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
    def test_postSucc(self):
        url = reverse('join')
        response = self.client.post(url, {'email': 'test@gmail.com', 'first_name':'John', 'last_name':'Smith', 'username': 'testuser1',
            'password1': 'secret','password2': 'secret'})
        self.assertEqual(response.status_code, 200)
    
        
class TestUser_LoginView(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        self.user = User.objects.create_user(**self.credentials)
        
        
    def test_ReachPage(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
    def test_badUser(self):
        url = reverse('login')
        response = self.client.post(url, {'username': 'testuser2',
            'password': 'secret4','next' : ''})
        self.assertEqual(response.status_code, 200)
        
    def test_login(self):
        url = reverse('login')
        response = self.client.post(url, {'username': 'testuser',
            'password': 'secret','next' : ''})
        self.assertEqual(response.status_code, 302)

class TestUser_LogoutView(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        self.user = User.objects.create_user(**self.credentials)
        self.client = Client()
        self.client.login(username='testuser', password='secret')
        
    def test_logout(self):
        response = self.client.get(reverse('logout'), data={'next': ''})
        self.assertEqual(response.status_code, 302)
        
    # How to catch django.urls.exceptions.NoReverseMatch exception
    # def test_url(self):
        
    #     response = self.client.get(reverse('logout'), data={'next': '  a  '})
    #     self.assertEqual(response.status_code, 302)

        
class TestCreateComplexView(TestCase):
    def setUp(self):
        self.state = State.objects.create(name = "California")
        self.city = City.objects.create(name = 'Chico', state = self.state)
    def test_invalidForm(self):
        response = self.client.post(reverse('createComplex'))        
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        
    def test_getreq(self):
        response = self.client.get(reverse('createComplex'))        
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
    
    #Calls API
    def test_validForm(self):
        ComPk = self.state.pk
        Citypk = self.city.pk
        formdata = {'complexName':'Timbers IV', 
                    'url':'https://www.google.com/',
                    'address':'123 Nord Avenue',
                    'state': str(ComPk),
                    'city':str(Citypk),
                    'zipcode':'95926'}
        response = self.client.post(reverse('createComplex'),formdata)
        self.assertEqual(response.status_code, 302)        

        
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


