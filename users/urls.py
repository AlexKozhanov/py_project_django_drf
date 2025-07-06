from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from users.views import UserViewSet, \
    UserCreateAPIView, \
    PaymentListAPIView, \
    PaymentCreateAPIView, \
    PaymentRetrieveAPIView, \
    PaymentUpdateAPIView, \
    PaymentDestroyAPIView
from users.apps import UsersConfig

app_name = UsersConfig.name

router = SimpleRouter()
router.register('', UserViewSet)

urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name='register'),
    path("payment/", PaymentListAPIView.as_view(), name='payment_list'),
    path("payment/create/", PaymentCreateAPIView.as_view(), name='payment_create'),
    path("payment/<int:pk>/", PaymentRetrieveAPIView.as_view(), name='payment_retrieve'),
    path("payment/<int:pk>/update/", PaymentUpdateAPIView.as_view(), name='payment_update'),
    path("payment/<int:pk>/delete/", PaymentDestroyAPIView.as_view(), name='payment_delete'),
    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
]

urlpatterns += router.urls
