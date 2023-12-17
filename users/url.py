from django.urls import path

from users.views import CreateUserAPIView, VerifyAPIView, GetNewVerification

urlpatterns = [
    path('signup/', CreateUserAPIView.as_view(), ),
    path('verify/', VerifyAPIView.as_view(), ),
    path('new-code/', GetNewVerification.as_view())
]




