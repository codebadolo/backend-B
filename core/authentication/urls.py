from django.urls import path
from .views import ( UserProfileView  , RegisterView, 
                    LoginView, LogoutView , KYCSubmissionView , 
                    KYCAdminApprovalView 
                     ,UserDetailView
                    
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
     path('auth/user-detail/<int:user_id>/', UserDetailView.as_view(), name='user-detail'),
    path('auth/user-profile/<int:user_id>/', UserProfileView.as_view(), name='user-profile'),
    path('auth/kyc/submit/<int:user_id>/', KYCSubmissionView.as_view(), name='kyc-submit'),
    path('auth/kyc/admin/<int:user_id>/', KYCAdminApprovalView.as_view(), name='kyc-admin-approval'),
    #path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('kyc/', KYCSubmissionView.as_view(), name='kyc-submission'),
    # Admin can approve or reject KYC
    #path('api/user/details/',UserDetailView.as_view(), name='user_details'),
    #path('kyc/admin/<int:user_id>/', KYCAdminApprovalView.as_view(), name='kyc-admin-approval'),
   

]
