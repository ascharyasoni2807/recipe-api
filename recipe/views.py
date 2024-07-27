import logging
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from utils.pagination import CustomPageNumberPagination

from .models import Recipe, RecipeLike
from .serializers import RecipeLikeSerializer, RecipeSerializer
from .permissions import IsAuthorOrReadOnly

logger = logging.getLogger("recipe")


class RecipeListAPIView(generics.ListAPIView):
    """
    Get: a collection of recipes
    """
    logger.info("Listing all recipes")
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (AllowAny,)
    filterset_fields = ('category__name', 'author__username')
    pagination_class = CustomPageNumberPagination
    logger.info("Successfully listed recipes")



class RecipeCreateAPIView(generics.CreateAPIView):
    """
    Create: a recipe
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthenticated,)
    logger.info("Successfully created a new recipe")
    
    def perform_create(self, serializer):
        logger.info("Create recipe for user {self.request.user.username}")
        serializer.save(author=self.request.user)


class RecipeAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Get, Update, Delete a recipe
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrReadOnly,)


class RecipeLikeAPIView(generics.CreateAPIView):
    """
    Like, Dislike a recipe
    """
    serializer_class = RecipeLikeSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        logger.info(f"User {request.user.username} attempting to like recipe ID: {pk}")
        recipe = get_object_or_404(Recipe, id=self.kwargs['pk'])
        new_like, created = RecipeLike.objects.get_or_create(
            user=request.user, recipe=recipe)
        if created:
            new_like.save()
            logger.info(f"User {request.user.username} liked recipe ID: {pk}")
            return Response(status=status.HTTP_201_CREATED)
        logger.warning(f"User {request.user.username} already liked recipe ID: {pk}")
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        logger.info(f"User {request.user.username} attempting to dislike recipe ID: {pk}")
        recipe = get_object_or_404(Recipe, id=self.kwargs['pk'])
        like = RecipeLike.objects.filter(user=request.user, recipe=recipe)
        if like.exists():
            like.delete()
            logger.info(f"User {request.user.username} disliked recipe ID: {pk}")
            return Response(status=status.HTTP_200_OK)
        logger.warning(f"User {request.user.username} has not liked recipe ID: {pk} yet")
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
