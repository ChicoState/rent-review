from django.test import TestCase

from website.models import Cities, Posts, Comments


class CitiesTestCase(TestCase):
    def setUp(self):
        Cities.objects.create(
            name="Clemens's City", 
            complex_name = "Clemens's Mantion",
            address = "123 W Avenue",
            url = "google.com",
            zipcode = 94081)
        Cities.objects.create(
            name="Tim's City", 
            complex_name = "Tim's Mantion",
            address = "124 W Avenue",
            url = "google.com",
            zipcode = 94082)

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        c = Cities.objects.get(name="Clemens's City")
        t = Cities.objects.get(name="Tim's City")
        self.assertEqual(c, "Clemens's City")
        self.assertEqual(t, "Tim's City") 

# class PostsTestCase(TestCase):
#     def setUp(self):
#         Animal.objects.create(name="lion", sound="roar")
#         Animal.objects.create(name="cat", sound="meow")

#     def test_animals_can_speak(self):
#         """Animals that can speak are correctly identified"""
#         lion = Animal.objects.get(name="lion")
#         cat = Animal.objects.get(name="cat")
#         self.assertEqual(lion.speak(), 'The lion says "roar"')
#         self.assertEqual(cat.speak(), 'The cat says "meow"')

# class CommentsTestCase(TestCase):
#     def setUp(self):
#         Animal.objects.create(name="lion", sound="roar")
#         Animal.objects.create(name="cat", sound="meow")

#     def test_animals_can_speak(self):
#         """Animals that can speak are correctly identified"""
#         lion = Animal.objects.get(name="lion")
#         cat = Animal.objects.get(name="cat")
#         self.assertEqual(lion.speak(), 'The lion says "roar"')
#         self.assertEqual(cat.speak(), 'The cat says "meow"')

