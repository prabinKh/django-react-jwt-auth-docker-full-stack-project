
from django.contrib.auth import authenticate
from django.urls import path
from .views import *
urlpatterns = [

    
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomRefreshTokenView.as_view(), name='token_refresh'),
    path('note/',get_note,name='get_note'),
    path('logout/', logout, name='logout'),
    path('authenticated/', is_authenticated, name='authenticate'),
    path('register/', register, name='register')
]