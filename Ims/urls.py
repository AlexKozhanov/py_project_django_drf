from rest_framework.routers import SimpleRouter

from Ims.views import CourseViewSet
from Ims.apps import ImsConfig

app_name = ImsConfig.name

router = SimpleRouter()
router.register('', CourseViewSet)

urlpatterns = []

urlpatterns += router.urls
