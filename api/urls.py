from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import TaskViewSet, ChangeViewSet, UserViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'tasks/(?P<task_id>[^/.]+)/changes', ChangeViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/', UserViewSet.as_view({'post': 'create'})),
    path(
        'v1/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'),
    path(
        'v1/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),

]
