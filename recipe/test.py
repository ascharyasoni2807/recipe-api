import logging
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from recipe.models import Recipe, RecipeCategory, RecipeLike
from django.core.files.uploadedfile import SimpleUploadedFile

class RecipeAPITestCase(APITestCase):

    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass'
        )
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

    def test_recipe_list(self):
        self.logger.info('Testing recipe list endpoint')
        response = self.client.get('/api/recipe/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_recipe_create(self):
        self.logger.info('Testing recipe creation endpoint')
        url = '/api/recipe/create/'
        data = {
            'category': {"name":str(self.category)}, 
            'title': 'string',
            'desc': 'string',
            'cook_time': '01:00:00',
            'ingredients': 'string',
            'procedure': 'string'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Recipe.objects.count(), 2)

    def test_recipe_like_success(self):
        self.logger.info('Testing successful recipe like')
        response = self.client.post(f'/api/recipe/{self.recipe.id}/like/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RecipeLike.objects.filter(recipe=self.recipe).count(), 1)
        self.assertTrue(RecipeLike.objects.filter(user=self.user, recipe=self.recipe).exists())
    def test_recipe_like_duplicate(self):
        self.logger.info('Testing duplicate recipe like')
        RecipeLike.objects.create(user=self.user, recipe=self.recipe)
        response = self.client.post(f'/api/recipe/{self.recipe.id}/like/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(RecipeLike.objects.filter(recipe=self.recipe).count(), 1)

    def test_recipe_dislike(self):
        self.logger.info('Testing recipe dislike')
        RecipeLike.objects.create(user=self.user, recipe=self.recipe)
        response = self.client.delete(f'/api/recipe/{self.recipe.id}/like/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(RecipeLike.objects.filter(recipe=self.recipe).count(), 0)

    def test_recipe_dislike_not_liked(self):
        self.logger.info('Testing bad request recipe like')
        response = self.client.delete(f'/api/recipe/{self.recipe.id}/like/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(RecipeLike.objects.filter(recipe=self.recipe).count(), 0)
