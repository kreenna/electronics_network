from rest_framework.routers import SimpleRouter

from elements.apps import ElementsConfig
from .views import FactoryViewSet, RetailNetworkViewSet, IndividualEntrepreneurViewSet

app_name = ElementsConfig.name

router = SimpleRouter()

router.register(r'factories', FactoryViewSet, basename='factories')
router.register(r'networks', RetailNetworkViewSet, basename='networks')
router.register(r'individual_entrepreneurs', IndividualEntrepreneurViewSet, basename='individual_entrepreneurs')

urlpatterns = router.urls
