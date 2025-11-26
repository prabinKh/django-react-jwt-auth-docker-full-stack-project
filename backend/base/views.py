from operator import truediv
from django.http import response
from django.shortcuts import render

# Create your views here.

# from .authentication import CookieJWTAuthentication  # ← Import it

from django.contrib.auth.models import User
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializer import NoteSerializer, UserRegistrationSerializer
from .models import *


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            
            # If login credentials are wrong, super().post() already returns 401
            if response.status_code != 200:
                return response

            tokens = response.data
            access_token = tokens['access']
            refresh_token = tokens['refresh']

            res = Response()
            res.data = {'success': True}

            # Access Token Cookie (short-lived)
            res.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,          # Now safe to enable
                secure=True,            # Set False in local dev if needed
                samesite='None',
                path='/',
                # max_age=5 * 60          # 5 minutes (matches JWT default)
            )

            # Refresh Token Cookie (long-lived)
            res.set_cookie(
                key='refresh_token',
                value=refresh_token,    # FIXED: now correct token
                httponly=True,
                secure=True,
                samesite='None',
                path='/',
                # max_age=60 * 60 * 24 * 30  # 30 days
            )

            return res

        except Exception as e:
            # NEVER swallow errors silently in development!
            return Response({
                'success': False,
                'error': str(e)                    # Remove this line in production
            }, status=400)   

class CustomRefreshTokenView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.COOKIES.get('refresh_token')

            # Fix 1: request.data is immutable → make a mutable copy
            mutable_data = request.data.copy()
            mutable_data['refresh'] = refresh_token
            request._full_data = mutable_data

            # Fix 2: typo in set_cookie (not set_cookies) + correct key name
            response = super().post(request, *args, **kwargs)

            access_token = response.data['access']

            res = Response()
            res.data = {'refreshed': True}
            res.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=True,
                samesite='None',
                path='/'
            )
            return res

        except:
            return Response({'refreshed': False})


@api_view(['POST'])
def logout(request):
    try:
        res= Response()
        res.data = {'success': True}
        res.delete_cookie('access_token', path='/', samesite='None')
        res.delete_cookie('refresh_token', path='/', samesite='None')
        return res
    except:
        return Response({'success':False})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @authentication_classes([CookieJWTAuthentication]) 
def get_note(request):
    user = request.user
    notes = Note.objects.filter(owner=user)
    serializer = NoteSerializer(notes, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def is_authenticated(request):
    return Response({'authenticated': True})

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserRegistrationSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)
