from rest_framework.serializers import ModelSerializer

from Ims.models import Course


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"
