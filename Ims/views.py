from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from Ims.models import Course
from Ims.serializers import CourseSerializer


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
