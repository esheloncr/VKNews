from .views import ArticleAPIView
from rest_framework import routers

app_name = "News"

router = routers.SimpleRouter()
router.register(r'articles', ArticleAPIView)

urlpatterns = [] + router.urls