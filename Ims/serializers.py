from rest_framework.serializers import ModelSerializer, \
    SerializerMethodField

from Ims.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    lessons_in_course = SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_lessons_in_course(self, course):
        lessons = course.lesson_set.all()
        return LessonSerializer(lessons, many=True).data


class CourseDetailSerializer(ModelSerializer):
    count_lesson_in_course = SerializerMethodField()
    lessons_in_course = SerializerMethodField()

    def get_count_lesson_in_course(self, course):
        return course.lesson_set.count()

    def get_lessons_in_course(self, course):
        lessons = course.lesson_set.all()
        return LessonSerializer(lessons, many=True).data

    class Meta:
        model = Course
        fields = (
            'name',
            'description',
            'count_lesson_in_course',
            'lessons_in_course',
        )


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
