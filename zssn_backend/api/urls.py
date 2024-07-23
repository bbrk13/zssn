# urls.py
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'trade_offers', views.TradeOfferViewSet)
router.register(r'survivors', views.SurvivorViewSet)

urlpatterns = [
    path('', include(router.urls))
]
