from rest_framework import generics, permissions
from django.contrib.auth.models import User
from .serializers import UserSerializer , KYCSerializer, EmptySerializer
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Profile 
from rest_framework import generics
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import APIKey
from .serializers import APIKeySerializer
from rest_framework.views import APIView

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated
# View to retrieve and update the user's profile
# 
# 
class UserDetailView(APIView):
    def get(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({"error": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(id=user_id)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

# Dummy Serializer for LogoutView (used for documentation purposes)

class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
    


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]  # Allow anyone to register

class LoginView(TokenObtainPairView):
    '''    @swagger_auto_schema(
        operation_description="Login to the application to obtain access and refresh tokens",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password')
            }
        ),
        responses={200: openapi.Response('Success')}
    )'''
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    
    
    
class LogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        # Avoid schema generation when generating Swagger/OpenAPI docs
    def get_serializer_class(self):
        if getattr(self, 'swagger_fake_view', False):
            return EmptySerializer
        return None    
        # View for users to submit their KYC documents
        #        # 
class KYCSubmissionView(generics.UpdateAPIView):
    serializer_class = KYCSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

# Admin view to approve/reject KYC
# 
#  
class KYCAdminApprovalView(generics.UpdateAPIView):
    serializer_class = KYCSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_object(self):
        user_id = self.kwargs.get('user_id')
        return Profile.objects.get(user__id=user_id)

    def patch(self, request, *args, **kwargs):
        profile = self.get_object()
        status = request.data.get('kyc_status')
        if status in ['APPROVED', 'REJECTED']:
            profile.kyc_status = status
            profile.save()
            return Response({'message': f'KYC status set to {status}'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid KYC status'}, status=status.HTTP_400_BAD_REQUEST)
    

class GenerateAPIKeyView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        api_key, created = APIKey.objects.get_or_create(user=user)
        if not created:
            api_key.key = APIKey.generate_key()
            api_key.save()
        return Response({"api_key": api_key.key}, status=status.HTTP_201_CREATED)

class ResetAPIKeyView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        try:
            api_key = user.api_key
            api_key.key = APIKey.generate_key()
            api_key.save()
            return Response({"api_key": api_key.key}, status=status.HTTP_200_OK)
        except APIKey.DoesNotExist:
            return Response({"error": "API key not found"}, status=status.HTTP_404_NOT_FOUND)

class RevokeAPIKeyView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        try:
            api_key = user.api_key
            api_key.is_active = False
            api_key.save()
            return Response({"message": "API key revoked"}, status=status.HTTP_200_OK)
        except APIKey.DoesNotExist:
            return Response({"error": "API key not found"}, status=status.HTTP_404_NOT_FOUND)
