from django.urls import path

from users.views import CreateUserAPIView, VerifyAPIView, GetNewVerification, ChangeUserInformationView, LoginAPIView, \
    LoginRefreshView, LogOutView, ResetPasswordView

urlpatterns = [
    path('signup/', CreateUserAPIView.as_view(), ),
    path('verify/', VerifyAPIView.as_view(), ),
    path('new-verify/', GetNewVerification.as_view()),
    path('change-user/', ChangeUserInformationView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('login/refresh/', LoginRefreshView.as_view()),
    path('logout/', LogOutView.as_view()),
    path('reset-pass/', ResetPasswordView.as_view())

]
