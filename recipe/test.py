import logging
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from recipe.models import Recipe, RecipeCategory

logger = logging.getLogger("recipe")

class RecipeModelTestCase(TestCase):

    def setUp(self):
        logger.info("Setting up the test case")
        self.user = get_user_model().objects.create_user(
            username='test',
            email='test@test.com',
            password='test@123'
        )
        self.category = RecipeCategory.objects.create(
            name='Dessert'
        )
        self.recipe = Recipe.objects.create(
            author=self.user,
            category=self.category,
            picture='uploads/test.jpg',
            title='Test Recipe',
            desc='A short description of the test recipe.',
            cook_time='00:30:00',
            ingredients='Flour, Sugar, Eggs',
            procedure='Mix and bake.',
            created_at=timezone.now(),
            updated_at=timezone.now()
        )

    def test_recipe_creation(self):
        logger.info("Testing recipe creation")
        self.assertEqual(self.recipe.title, 'Test Recipe')
        self.assertEqual(self.recipe.author, self.user)
        self.assertEqual(self.recipe.category, self.category)
        self.assertEqual(self.recipe.picture, 'uploads/test.jpg')
        self.assertEqual(self.recipe.desc, 'A short description of the test recipe.')
        self.assertEqual(self.recipe.cook_time, '00:30:00')
        self.assertEqual(self.recipe.ingredients, 'Flour, Sugar, Eggs')
        self.assertEqual(self.recipe.procedure, 'Mix and bake.')
        logger.info("Recipe creation test passed")

    def test_recipe_string_representation(self):
        logger.info("Testing recipe string representation")
        self.assertEqual(str(self.recipe), 'Test Recipe')
        logger.info("Recipe string representation test passed")

    def test_get_total_number_of_likes(self):
        logger.info("Testing get total number of likes")
        self.assertEqual(self.recipe.get_total_number_of_likes(), 0)
        logger.info("Get total number of likes test passed")

    def test_get_total_number_of_bookmarks(self):
        logger.info("Testing get total number of bookmarks")
        self.assertEqual(self.recipe.get_total_number_of_bookmarks(), 0)
        logger.info("Get total number of bookmarks test passed")

    def test_ordering(self):
        logger.info("Testing recipe ordering")
        another_recipe = Recipe.objects.create(
            author=self.user,
            category=self.category,
            picture='uploads/test2.jpg',
            title='Another Test Recipe',
            desc='Another short description.',
            cook_time='01:00:00',
            ingredients='Flour, Sugar, Eggs, Butter',
            procedure='Mix, bake, and cool.',
            created_at=timezone.now(),
            updated_at=timezone.now()
        )
        recipes = Recipe.objects.all()
        self.assertEqual(recipes[0], another_recipe)
        self.assertEqual(recipes[1], self.recipe)
        logger.info("Recipe ordering test passed")
