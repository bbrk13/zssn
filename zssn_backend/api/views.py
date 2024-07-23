# views.py
from rest_framework import viewsets, filters, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.http import JsonResponse
from django.views import View
import json
from .models import Survivor, Inventory, TradeOffer, TradeOfferItems
from .serializers import SurvivorSerializer, TradeOfferSerializer2
import logging

logger = logging.getLogger(__name__)


class TradeOfferPagination(PageNumberPagination):
    page_size = 4


class TradeOfferViewSet(viewsets.ModelViewSet):
    queryset = TradeOffer.objects.all().order_by('id')
    serializer_class = TradeOfferSerializer2
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    pagination_class = TradeOfferPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        id = self.request.query_params.get('survivorId', None)
        if id is not None:
            queryset = queryset.filter(
                requesterId=id) | queryset.filter(receiverId=id)
        return queryset


class SurvivorPagination(PageNumberPagination):
    page_size = 12


class SurvivorViewSet(viewsets.ModelViewSet):
    queryset = Survivor.objects.all().filter(
        is_infected=False).order_by('id')
    serializer_class = SurvivorSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    pagination_class = SurvivorPagination
