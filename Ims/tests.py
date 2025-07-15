# from django.test import TestCase
# Т.к. мы используем rest_framework то использовать TestCase нельзя,
# используем PITestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import Group
from django.urls import reverse
from users.models import User
from Ims.models import Course, Lesson, Subscription


class LessonCRUDTestCase(APITestCase):
    maxDiff = None

    def setUp(self):
        """Подготовка тестовых данных."""
        # Создаем группу модераторов
        self.moder_group = Group.objects.create(name="moders")
        # Создаем пользователей с использованием email вместо username
        # подсос будет обычным юзером, а фраер модератором
        self.owner = User.objects.create(email='podsos@example.com', password='test123')
        self.moder = User.objects.create(email='fraer@example.com', password='test123456')
        self.moder.groups.add(self.moder_group)
        # Создаем тестовые курсы и уроки
        # У подсоса будет урок, а у фраера курс
        self.course = Course.objects.create(
            name='TestCourse',
            owner=self.moder)
        self.lesson = Lesson.objects.create(
            name='TestLesson',
            course=self.course,
            link='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            owner=self.owner)
        # Подключаем пользователя, если он один
        # self.client.force_authenticate(user=self.owner)

    def test_course_retrieve_by_moder(self):
        """Разрешение на просмотр курса фраером."""
        self.client.force_authenticate(user=self.moder)
        url = reverse('course:course-detail', args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('name'), self.course.name)
        self.assertEqual(data.get('name'), 'TestCourse')

    def test_course_create_by_moder(self):
        """Запрет создания курса фраером."""
        self.client.force_authenticate(user=self.moder)
        url = reverse('course:course-list')
        data = {
            'name': 'TestCourse2',
            'owner': self.moder,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Course.objects.all().count(), 1)

    # def test_course_update_by_moder(self):
    #     """Разрешение обновления курса фраером."""
    #     self.client.force_authenticate(user=self.moder)
    #     url = reverse('course:course-detail', args=(self.course.pk,))
    #     data = {
    #         'name': 'TestCourse2.1'
    #     }
    #     response = self.client.patch(url, data)
    #     data = response.json()
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(data.get('name'), 'TestCourse2.1')

    def test_course_delete_by_moder(self):
        """Разрешение удаления курса фраером."""
        self.client.force_authenticate(user=self.moder)
        url = reverse('course:course-detail', args=(self.course.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.all().count(), 0)

    def test_course_delete_by_owner(self):
        """Разрешение удаления урока подсосом."""
        self.client.force_authenticate(user=self.owner)
        url = reverse('course:course-detail', args=(self.course.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # def test_lesson_list(self):
    #     """Просмотр урока фраером."""
    #     pass
    # #     self.client.force_authenticate(user=self.moder)
    # #     url = reverse('course:course-list')
    # #     response = self.client.get(url)
    # #     data = response.json()
    # #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    # #     result = {
    # #         'count': 1,
    # #         'next': None,
    # #         'previous': None,
    # #         'results': [{
    # #             'id': self.course.pk,
    # #             'lessons_in_course': [{
    # #                 'id': self.lesson.pk,
    # #                 'name': self.lesson.name,
    # #                 'link': self.lesson.link,
    # #                 'description': self.lesson.description,
    # #                 'png': self.lesson.png,
    # #                 'course': self.lesson.course,
    # #                 'owner': self.lesson.owner
    # #             }],
    # #             'name': self.course.name,
    # #             'description': self.course.description,
    # #             'png': self.course.png,
    # #             'owner': self.course.owner}]
    # #     }
    # #     result1 = [{
    # #             'id': self.course.pk,
    # #             'lessons_in_course': [{
    # #                 'id': self.lesson.pk,
    # #                 'name': self.lesson.name,
    # #                 'link': self.lesson.link,
    # #                 'description': self.lesson.description,
    # #                 'png': None,
    # #                 'course': self.lesson.course,
    # #                 'owner': self.lesson.owner
    # #             }],
    # #             'name': self.course.name,
    # #             'description': self.course.description,
    # #             'png': None,
    # #             'owner': self.course.owner}
    # #     ]
    # #     # self.assertEqual(data, result)
    # #     self.assertEqual(data.get('results'), result1)

    # def test_lesson_create_by_owner(self):
    #     """Создание урока владельцем урока."""
    #     pass
    #     # self.client.force_authenticate(user=self.owner)
    #     # url = reverse("course:lesson_create")
    #     # data = {
    #     #     'name': 'TestLesson22'
    #     # }
    #     # response = self.client.post(url, data)
    #     # self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    #     # self.assertEqual(Lesson.objects.count(), 2)

    def test_lesson_create_by_moder(self):
        """Запрет создания урока фраером."""
        self.client.force_authenticate(user=self.moder)
        data = {
            "name": "New Lesson",
            "course": self.course.pk,
            "video_link": "https://youtube.com/new",
        }
        response = self.client.post(reverse("course:lesson_create"), data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_update_by_owner(self):
        """Обновление урока владельцем."""
        self.client.force_authenticate(user=self.owner)
        data = {"name": "Updated Lesson"}
        response = self.client.patch(
            reverse("course:lesson_update", kwargs={"pk": self.lesson.pk}), data=data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.name, "Updated Lesson")

    def test_lesson_delete_by_owner(self):
        """Разрешение удаления урока подсосом."""
        self.client.force_authenticate(user=self.owner)
        url = reverse('course:lesson_delete', args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_lesson_delete_by_moder(self):
        """Запрет удаления урока фраером."""
        self.client.force_authenticate(user=self.owner)
        url = reverse('course:course-detail', args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    class SubscriptionTestCase(APITestCase):
        def setUp(self):
            """Подготовка тестовых данных для подписок."""
            self.user = User.objects.create(email="user@test.com", password="testpass")
            self.course = Course.objects.create(name="Test Course")
            self.subscription_url = reverse("materials:subscriptions")

        def test_subscription_create_and_delete(self):
            """Тест создания и удаления подписки."""
            self.client.force_authenticate(user=self.user)
            # Создание подписки
            response = self.client.post(
                self.subscription_url, data={"course_id": self.course.pk}
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data["message"], "Подписка добавлена")
            self.assertTrue(
                Subscription.objects.filter(user=self.user, course=self.course).exists()
            )

            # Удаление подписки
            response = self.client.post(
                self.subscription_url, data={"course_id": self.course.pk}
            )
            self.assertEqual(response.data["message"], "Подписка удалена")
            self.assertFalse(
                Subscription.objects.filter(user=self.user, course=self.course).exists()
            )
