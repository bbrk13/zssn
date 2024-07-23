from django.contrib import admin
from .models import Survivor, Inventory, TradeOffer, TradeOfferItems

# Register your models here.
admin.site.register(Survivor)
admin.site.register(Inventory)
admin.site.register(TradeOffer)
admin.site.register(TradeOfferItems)