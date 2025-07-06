# Viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from users.models import User, Payment
from users.serializers import UserSerializer, \
    PaymentSerializer
# Generic
from rest_framework.generics import ListAPIView, \
    CreateAPIView, \
    RetrieveAPIView, \
    UpdateAPIView, \
    DestroyAPIView
from rest_framework.permissions import AllowAny


# Viewsets
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Generic
class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()

class PaymentListAPIView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_method', )
    ordering_fields = ('payment_date', )
    search_fields = ('payment_method', )

class PaymentCreateAPIView(CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentRetrieveAPIView(RetrieveAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentUpdateAPIView(UpdateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentDestroyAPIView(DestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
