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
from django.contrib.auth.models import User
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated
# View to retrieve and update the user's profile
# Dummy Serializer for LogoutView (used for documentation purposes)
class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id=None):
        # Use provided user_id or fallback to current authenticated user
        if user_id is None:
            user_id = request.user.id

        try:
            user = User.objects.get(id=user_id)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user_id = self.kwargs.get('user_id', self.request.user.id)
        return User.objects.get(id=user_id)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]  # Allow anyone to register

class LoginView(TokenObtainPairView):
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
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user_id = self.kwargs.get('user_id', self.request.user.id)
        return Profile.objects.get(user__id=user_id)

# Admin view to approve/reject KYC
class KYCAdminApprovalView(generics.UpdateAPIView):
    serializer_class = KYCSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_object(self):
        user_id = self.kwargs.get('user_id')
        return Profile.objects.get(user__id=user_id)

    def patch(self, request, *args, **kwargs):
        profile = self.get_object()
        kyc_status = request.data.get('kyc_status')
        if kyc_status in ['APPROVED', 'REJECTED']:
            profile.kyc_status = kyc_status
            profile.save()
            return Response({'message': f'KYC status set to {kyc_status}'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid KYC status'}, status=status.HTTP_400_BAD_REQUEST)
