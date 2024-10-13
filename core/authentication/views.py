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
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated
# View to retrieve and update the user's profile
# 
# 

# Dummy Serializer for LogoutView (used for documentation purposes)
@method_decorator(csrf_exempt, name='dispatch')
class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
    

@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]  # Allow anyone to register

@method_decorator(csrf_exempt, name='dispatch')
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
    
    
    
@method_decorator(csrf_exempt, name='dispatch')    
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
        # 
@method_decorator(csrf_exempt, name='dispatch')        # 
class KYCSubmissionView(generics.UpdateAPIView):
    serializer_class = KYCSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

# Admin view to approve/reject KYC
# 
# 
@method_decorator(csrf_exempt, name='dispatch')# 
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
    
