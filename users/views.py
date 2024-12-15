from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from .serializers import LoginResponseSerializer, LoginSerializer, RegisterResponseSerializer, RegistrationSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import RoleChoices, User
from django.core.exceptions import PermissionDenied


class RegistrationView(APIView):
    @swagger_auto_schema(request_body=RegistrationSerializer,
                         responses={200: RegisterResponseSerializer(), 400: 'Errors'}) 
    
    def post(self, request: Request):
        if request.data.get('role') == RoleChoices.ADMIN and (request.user.is_anonymous or not request.user.role == RoleChoices.ADMIN):
            raise PermissionDenied("Лише адміністратор може реєструвати/створювати адміністраторів")
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user: User = serializer.save()
            return Response({
                'username': user.username,
                'role': user.role
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={200: LoginResponseSerializer(), 400: 'Errors'}
    )
    
    def post(self, request: Request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data.get('user')

            refresh= RefreshToken.for_user(user)

            refresh.payload['role'] = user.role
            refresh.payload['username'] = user.username
            refresh.payload['email'] = user.email
            
            access_token = str(refresh.access_token)

            return Response({'access_token': access_token,
                             'refresh_token': str(refresh)}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
