from django.urls import path
from .views import ( UserProfileView  , RegisterView, 
                    LoginView, LogoutView , KYCSubmissionView , 
                    KYCAdminApprovalView ,GenerateAPIKeyView,
                    ResetAPIKeyView, RevokeAPIKeyView
                    
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
     path('kyc/', KYCSubmissionView.as_view(), name='kyc-submission'),
    # Admin can approve or reject KYC
    path('kyc/admin/<int:user_id>/', KYCAdminApprovalView.as_view(), name='kyc-admin-approval'),
    path('api-key/generate/', GenerateAPIKeyView.as_view(), name='generate-api-key'),
    path('api-key/reset/', ResetAPIKeyView.as_view(), name='reset-api-key'),
    path('api-key/revoke/', RevokeAPIKeyView.as_view(), name='revoke-api-key'),

]
