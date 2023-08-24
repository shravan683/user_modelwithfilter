
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TicketViewSet, login_view
from rest_framework.authtoken import views

router = DefaultRouter()
router.register(r'tickets', TicketViewSet, basename='ticket')

urlpatterns = [

    path('', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token),
    path('login/', login_view, name='login'),
]
