# Viewsets
from rest_framework.viewsets import ModelViewSet

from Ims.models import Course, Lesson
from Ims.serializers import CourseSerializer, \
    LessonSerializer, \
    CourseDetailSerializer
# Generic
from rest_framework.generics import ListAPIView, \
    CreateAPIView, \
    RetrieveAPIView, \
    UpdateAPIView, \
    DestroyAPIView


# Viewsets
class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    # serializer_class = CourseSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseSerializer

# Generic
class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
