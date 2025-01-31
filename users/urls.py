from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users import views

app_name = 'users'

urlpatterns = [
    path('listuser/', views.UserListAPIView.as_view(), name='user-list'),
    path('register/', views.UserRegisterationAPIView.as_view(),
         name="create-user"),
    path('login/', views.UserLoginAPIView.as_view(), name="login-user"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('logout/', views.UserLogoutAPIView.as_view(), name='logout-user'),
    path('', views.UserAPIView.as_view(), name='user-info'),
    path('profile/', views.UserProfileAPIView.as_view(),
         name='user-profile'),
    path('profile/avatar/', views.UserAvatarAPIView.as_view(),
         name='user-avatar'),
    path('profile/<int:pk>/bookmarks/', views.UserBookmarkAPIView.as_view(),
         name='user-bookmark'),
    path('password/change/', views.PasswordChangeAPIView.as_view(),
         name='change-password'),
]
