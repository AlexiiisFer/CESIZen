from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views_api import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# API Routeur

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'activities', ActivityViewSet)
router.register(r'information', InformationViewSet)





urlpatterns = [
    path('', lambda request: redirect('home/', permanent=False)),
    path('home/', views.home, name='home'),

# Routes pour les utilisateurs

    path('signUp/', views.signUp, name='signUp'),
    path('login/', views.custom_login, name='login'),
    path('settings/', views.settings, name='settings'),
    path('profile_update/', views.profile_update, name='profile_update'),
    path('logout/', views.custom_logout, name='logout'),

    path('admin_user/', views.admin_user, name='administrator_user'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('add_user/', views.add_user, name='add_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('toggle_user/<int:user_id>/', views.toggle_user_active, name='toggle_user_active'),

# Routes pour les activités

    path('activities/', views.activity_list, name='activities'),
    path('activites/<int:pk>/', views.activity_detail, name='activity_detail'),
    path('activites/<int:pk>/favori/', views.toggle_favorite, name='toggle_favorite'),

    path('admin_activities/', views.administrator_activities, name='administrator_activities'),
    path('add_activity/', views.add_activity, name='add_activity'),
    path('edit_activity/<int:activity_id>/', views.edit_activity, name='edit_activity'),
    path('delete_activity/<int:activity_id>/', views.delete_activity, name='delete_activity'),
    path('toggle_activity/<int:activity_id>/', views.toggle_activity, name='toggle_activity'),


# Routes pour les informations

    path('informations/', views.information_list, name='informations'),
    path('informations/<int:info_id>/', views.information_detail, name='information_detail'),

    path('informations/add/', views.add_information, name='add_information'),
    path('information/<int:info_id>/edit/', views.edit_information, name='edit_information'),
    path('toggle_information/<int:info_id>/', views.toggle_information, name='toggle_information'),
    path('delete_information/<int:info_id>/', views.delete_information, name='delete_information'),

# Routes pour l'API
    path('api/', include(router.urls)),

        
    path('api/login/', CustomLoginView.as_view(), name='custom_login'),
    path('api/register/', UserRegistrationView.as_view(), name='user_registration'),


    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/user/', GetUserView.as_view(), name='get_user'),


]