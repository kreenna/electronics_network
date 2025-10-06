from rest_framework.routers import SimpleRouter

from elements.apps import ElementsConfig

app_name = ElementsConfig.name

router = SimpleRouter()

urlpatterns = router.urls