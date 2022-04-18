from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db.models.query_utils import Q
from .serializers import RegisterSerializer, UserSerializer, PasswordResetSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from  rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token

# Create your views here.
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        status_code = status.HTTP_201_CREATED
        response = {
            'success': 'True',
            'status code': status_code,
            'message': 'User registered  successfully',
        }

        return Response(response, status=status_code)

class LoginView(APIView):
    def post(self, request, format=None):
        username = request.data.get("username")
        password = request.data.get("password")
        if username is None or password is None:
            return Response({'error': "Please provide both username and password"}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'Error': 'Wrong Credentials'}, status=status.HTTP_400_BAD_REQUEST)

class UserView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_queryset(self):
        id = self.request.user.id
        return User.objects.get(id=id)

    def get(self, request):
        user = self.get_queryset()
        serializer = self.serializer_class(user)        
        return Response(serializer.data)  

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        id = self.request.user.id
        return User.objects.get(id=id)
    
    def get(self, request, format=None):
        user = self.get_queryset()
        user.auth_token.delete()
        return Response({
            'success': 'True',
            'message': 'User logged out successfully',
        }, status=status.HTTP_200_OK)  


class PasswordResetView(APIView):
    serializer_class =  PasswordResetSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data.get('username')
        email = serializer.data.get('email')

        user = User.objects.get(Q(email=email),Q(username=username))
        if user.exists():
            





# class ChangePasswordView(generics.CreateAPIView):
#     permission_classes = (IsAuthenticated,)
#     serializer_class =  PasswordSerializer

#     def post(self, request, format=None):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         username = serializer.data.get('username')
#         password = serializer.data.get('password')
                
#         user = User.objects.get(username=username)
#         if user is not None:
#             user.set_password(password)
#             user.save()
#             return Response({'Success': 'Your password was successfully updated'}, status=status.HTTP_200_OK)
#         else:
#             return Response({'Error': 'Wrong. Check up and try again'}, status=status.HTTP_400_BAD_REQUEST)


