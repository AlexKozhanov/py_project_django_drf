from django.urls import path
from rest_framework.routers import SimpleRouter

from users.views import UserViewSet, \
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
    path("payment/", PaymentListAPIView.as_view(), name='payment_list'),
    path("payment/create/", PaymentCreateAPIView.as_view(), name='payment_create'),
    path("payment/<int:pk>/", PaymentRetrieveAPIView.as_view(), name='payment_retrieve'),
    path("payment/<int:pk>/update/", PaymentUpdateAPIView.as_view(), name='payment_update'),
    path("payment/<int:pk>/delete/", PaymentDestroyAPIView.as_view(), name='payment_delete'),
]

urlpatterns += router.urls
