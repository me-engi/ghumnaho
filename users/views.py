from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import status
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Customer, ShopOwner, Tourguide
from .serializers import (CustomerSerializer, DeliveryBoySerializer,
                          ShopOwnerSerializer)


class ProtectedEndpoint(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get the authenticated user
        user = request.user

        # Example logic: Return a message including the username of the authenticated user
        message = f"Welcome, {user.username}! This is a protected endpoint."
        
        return Response({"message": message})


class CustomerRegistration(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerLogin(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = Customer.objects.filter(username=username).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                status=status.HTTP_200_OK
            )
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class CustomerProfile(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]  # Add IsAuthenticated permission

    def get(self, request):
        customer = request.user
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)


class TourguideRegistration(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = DeliveryBoySerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TourguideLogin(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = Tourguide.objects.filter(username=username).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                status=status.HTTP_200_OK
            )
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class TourguideProfile(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        deliveryboy = request.user
        serializer = DeliveryBoySerializer(deliveryboy)
        return Response(serializer.data)

class ShopOwnerRegistration(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ShopOwnerSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ShopOwnerLogin(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = ShopOwner.objects.filter(username=username).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                status=status.HTTP_200_OK
            )
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class ShopOwnerProfile(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        shopowner = request.user
        serializer = ShopOwnerSerializer(shopowner)
        return Response(serializer.data)


class CustomerLogout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class TourguideLogout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ShopOwnerLogout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
class CustomerForgetPassword(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        customer = Customer.objects.filter(email=email).first()
        if customer:
            # Generate token
            token = default_token_generator.make_token(customer)
            # Send email with password reset link
            reset_url = f"http://yourwebsite.com/reset-password/{urlsafe_base64_encode(force_bytes(customer.pk))}/{token}/"
            message = render_to_string('password_reset_email.html', {'reset_url': reset_url})
            send_mail('Password Reset', message, 'from@example.com', [customer.email])
            return Response({"message": "Password reset email sent"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class TourguideForgetPassword(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        delivery_boy = Tourguide.objects.filter(email=email).first()
        if delivery_boy:
            # Generate token
            token = default_token_generator.make_token(delivery_boy)
            # Send email with password reset link
            reset_url = f"http://yourwebsite.com/reset-password/{urlsafe_base64_encode(force_bytes(delivery_boy.pk))}/{token}/"
            message = render_to_string('password_reset_email.html', {'reset_url': reset_url})
            send_mail('Password Reset', message, 'from@example.com', [delivery_boy.email])
            return Response({"message": "Password reset email sent"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class ShopOwnerForgetPassword(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        shop_owner = ShopOwner.objects.filter(email=email).first()
        if shop_owner:
            # Generate token
            token = default_token_generator.make_token(shop_owner)
            # Send email with password reset link
            reset_url = f"http://yourwebsite.com/reset-password/{urlsafe_base64_encode(force_bytes(shop_owner.pk))}/{token}/"
            message = render_to_string('password_reset_email.html', {'reset_url': reset_url})
            send_mail('Password Reset', message, 'from@example.com', [shop_owner.email])
            return Response({"message": "Password reset email sent"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)