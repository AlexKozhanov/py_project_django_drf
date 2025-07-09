from django.urls import reverse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
# Viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters, status

from Ims.models import Course
from users.models import User, Payment
from users.serializers import (
    UserSerializer,
    PaymentSerializer)
# Generic
from rest_framework.views import APIView
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView)
from rest_framework.permissions import AllowAny
# Swagger
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


# Viewsets
from users.services import create_stripe_product, create_stripe_price, create_stripe_session


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_summary="Получение профиля",
        operation_description="Получение профиля пользователя. Доступно только владельцу.",
        tags=["Пользователи"],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Детали платежа",
        operation_description="Детали платежа. Для администраторов — любой платеж, для пользователей — только свои.",
        tags=["Платежи"],
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


# Generic
class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()

    @swagger_auto_schema(
        operation_summary="Регистрация пользователя",
        operation_description="Создание нового пользователя. Доступно без аутентификации.",
        tags=["Пользователи"],
        responses={201: UserSerializer, 400: "Неверные данные"},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class PaymentListAPIView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_method',)
    ordering_fields = ('payment_date',)
    search_fields = ('payment_method',)


class PaymentCreateAPIView(CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    @swagger_auto_schema(
        operation_summary="Регистрация платежа",
        operation_description="Создание нового платежа. Доступно без аутентификации.",
        tags=["Пользователи"],
        responses={201: UserSerializer, 400: "Неверные данные"},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class PaymentRetrieveAPIView(RetrieveAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentUpdateAPIView(UpdateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentDestroyAPIView(DestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    @swagger_auto_schema(
        operation_summary="Удаление пользователя",
        operation_description="Удаление текущего пользователя. Доступно только владельцу.",
        tags=["Пользователи"],
        responses={204: "No Content", 403: "Forbidden"},
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class CoursePaymentAPIView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        operation_summary="Оплата курса",
        operation_description="Создает платежную сессию Stripe для оплаты курса.",
        tags=["Платежи"],
        responses={
            200: openapi.Response(
                description="Ссылка на оплату",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "payment_link": openapi.Schema(type=openapi.TYPE_STRING)
                    },
                ),
            ),
            404: "Курс не найден",
        },
    )
    def post(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        user = request.user

        # Создаем продукт и цену в Stripe
        product_id = create_stripe_product(course)
        price_id = create_stripe_price(product_id, 500)

        # Создаем сессию оплаты
        # success_url = request.build_absolute_uri(reverse("users:payment-success"))
        success_url = "http://127.0.0.1:8000/"
        # cancel_url = request.build_absolute_uri(reverse("users:payment-cancel"))
        cancel_url = "http://127.0.0.1:8000/"
        session_data = create_stripe_session(price_id, success_url, cancel_url)

        # Сохраняем платеж в БД
        # payment = Payment.objects.create(
        #     user_name=user,
        #     paid_course=course,
        #     payment_amount=course.price,
        #     payment_method="card",
        #     stripe_product_id=product_id,
        #     stripe_price_id=price_id,
        #     stripe_session_id=session_data["session_id"],
        #     stripe_payment_link=session_data["payment_link"],
        # )

        return Response(
            {"payment_link": session_data["payment_link"]}, status=status.HTTP_200_OK
        )
