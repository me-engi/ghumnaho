# users/urls.py

from django.contrib.auth import views as auth_views
from django.urls import path

from .views import (CustomerForgetPassword, CustomerLogin, CustomerLogout,
                    CustomerProfile, CustomerRegistration,
                    ShopOwnerForgetPassword, ShopOwnerLogin, ShopOwnerLogout,
                    ShopOwnerProfile, ShopOwnerRegistration,
                    TourguideForgetPassword, TourguideLogin, TourguideLogout,
                    TourguideProfile, TourguideRegistration)

urlpatterns = [
    # Customer URLs
    path('api/customers/register/', CustomerRegistration.as_view(), name='customer-register'),
    path('api/customers/login/', CustomerLogin.as_view(), name='customer-login'),
    path('api/customers/logout/', CustomerLogout.as_view(), name='customer-logout'),
    path('api/customers/profile/', CustomerProfile.as_view(), name='customer-profile'),
    path('api/customers/forgetpassword/', CustomerForgetPassword.as_view(), name='customer-forget-password'),

    # Tour Guide URLs
    path('api/tourguides/register/', TourguideRegistration.as_view(), name='tourguide-register'),
    path('api/tourguides/login/', TourguideLogin.as_view(), name='tourguide-login'),
    path('api/tourguides/logout/', TourguideLogout.as_view(), name='tourguide-logout'),
    path('api/tourguides/profile/', TourguideProfile.as_view(), name='tourguide-profile'),
    path('api/tourguides/forgetpassword/', TourguideForgetPassword.as_view(), name='tourguide-forget-password'),

    # Shop Owner URLs
    path('api/shopowners/register/', ShopOwnerRegistration.as_view(), name='shopowner-register'),
    path('api/shopowners/login/', ShopOwnerLogin.as_view(), name='shopowner-login'),
    path('api/shopowners/logout/', ShopOwnerLogout.as_view(), name='shopowner-logout'),
    path('api/shopowners/profile/', ShopOwnerProfile.as_view(), name='shopowner-profile'),
    path('api/shopowners/forgetpassword/', ShopOwnerForgetPassword.as_view(), name='shopowner-forget-password'),

    # Password reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
