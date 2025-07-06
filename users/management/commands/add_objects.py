from django.core.management.base import BaseCommand
from users.models import Payment
from Ims.models import Course, Lesson
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Add data to database"

    def handle(self, *args, **options):
        User.objects.all().delete()
        Lesson.objects.all().delete()
        Course.objects.all().delete()
        Payment.objects.all().delete()

        # Создаем тестовых юзеров
        user1 = User.objects.create(
            email="student1@example.com",
            phone_number="123",
            country="Russia",
        )

        user2 = User.objects.create(
            email="student2@example.com",
            phone_number="321",
            country="USA",
        )

        # Создаем тестовые курсы
        course1 = Course.objects.create(
            name="Python",
            description="Полный курс по Python",
        )

        course2 = Course.objects.create(
            name="Django",
            description="Полный курс по Django",
        )

        # Создаем тестовые уроки
        lesson1 = Lesson.objects.create(
            name="Основы Python",
            course=course1,
            description="Введение в язык Python",
            # link="https://example.com/python-basics",
        )

        lesson2 = Lesson.objects.create(
            name="Python Tests",
            course=course1,
            description="Работа с Тестированием",
            # link="https://example.com/django-orm",
        )

        lesson3 = Lesson.objects.create(
            name="Основы Django",
            course=course2,
            description="Введение в язык Django",
            # video_link="https://example.com/html-css",
        )

        # Создаем тестовые платежи
        payment_data = [
            {
                "user_name": user1,
                "payment_date": "2025-07-01",
                "paid_course": course1,
                "paid_lesson": lesson1,
                "payment_amount": 15000,
                "payment_method": "transfer",
            },
            {
                "user_name": user1,
                "payment_date": "2025-07-02",
                "paid_course": course1,
                "paid_lesson": lesson2,
                "payment_amount": 2000,
                "payment_method": "cash",
            },
            {
                "user_name": user2,
                "payment_date": "2025-07-03",
                "paid_course": course2,
                "paid_lesson": lesson3,
                "payment_amount": 12000,
                "payment_method": "transfer",
            },
            {
                "user_name": user2,
                "payment_date": "2025-07-04",
                "paid_course": course2,
                "paid_lesson": lesson3,
                "payment_amount": 1500,
                "payment_method": "cash",
            },
        ]

        for data in payment_data:
            Payment.objects.create(**data)

        self.stdout.write(self.style.SUCCESS("Тестовые данные успешно созданы!"))
