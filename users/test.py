import logging
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Profile
from recipe.models import Recipe, RecipeCategory

User = get_user_model()

class UserAPITestCase(APITestCase):

    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass'
        )
        # Ensure Profile only gets created once per test run
        self.profile,created=Profile.objects.get_or_create(user=self.user)
        self.category = RecipeCategory.objects.create(name='Dessert')
        self.recipe = Recipe.objects.create(
            author=self.user,
            category=self.category,
            title='Test Recipe',
            desc='A short description of the test recipe.',
            cook_time='00:30:00',
            ingredients='Flour, Sugar, Eggs',
            procedure='Mix and bake.'
        )       
        self.client.force_authenticate(user=self.user)

    def test_user_registration(self):
        self.logger.info('Testing user register endpoint')
        url = '/api/user/register/'
        data = {
            'username': 'newuser2',
            'email': 'newuser2@example.com',
            'password': 'newpass'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)  # Adjust count as needed
        self.assertIn('tokens', response.data)

    def test_user_login(self):
        url = '/api/user/login/'
        data = {
            'email': 'test2@example.com',
            'password': 'testpass'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tokens', response.data)

    def test_user_logout(self):
        url = '/api/user/logout/'
        refresh = RefreshToken.for_user(self.user)
        data = {'refresh': str(refresh)}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

    def test_user_detail(self):
        url = '/api/user/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test2@example.com')

    def test_user_list(self):
        url = '/api/user/listuser/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Adjust expected length based on setup
        self.assertGreaterEqual(len(response.data['results']), 1)

    def test_user_profile(self):
        url = '/api/user/profile/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['bookmarks'], [])

    def test_user_bookmarks(self):
        url = f'/api/user/profile/{self.user.id}/bookmarks/'
        data = {'id': self.recipe.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_password_change(self):
        url = '/api/user/password/change/'
        data = {
            'old_password': 'testpass',
            'new_password': 'newtestpass'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user.check_password('newtestpass'))
