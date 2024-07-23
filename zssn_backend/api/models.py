from django.db import models

# Create your models here.
from django.db import models


class Survivor(models.Model):
    id = models.AutoField(primary_key=True)
    is_infected = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    last_location_latitude = models.FloatField()
    last_location_longitude = models.FloatField()
    reported_by = models.ManyToManyField(
        'self', symmetrical=False, related_name='reporter', blank=True)

    def __str__(self):
        return self.name


class Inventory(models.Model):
    id = models.AutoField(primary_key=True)
    survivor = models.ForeignKey(
        Survivor, related_name='inventory', on_delete=models.CASCADE)
    is_locked = models.BooleanField(default=False)
    item_name = models.CharField(max_length=100)
    item_quantity = models.IntegerField()
    item_quantity_blocked = models.IntegerField(default=0)

    def __str__(self):
        return self.item_name


class TradeOffer(models.Model):
    id = models.AutoField(primary_key=True)
    requesterId = models.ForeignKey(
        Survivor, related_name='trade_offers_made', on_delete=models.CASCADE)
    receiverId = models.ForeignKey(
        Survivor, related_name='trade_offers_received', on_delete=models.CASCADE)
    totalPrice = models.IntegerField()
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"TradeOffer from {self.requesterID.name} to {self.receiverID.name} with status {self.status}"


class TradeOfferItems(models.Model):
    id = models.AutoField(primary_key=True)
    TradeOfferId = models.ForeignKey(
        TradeOffer, related_name='trade_offer_items', on_delete=models.CASCADE)
    SurvivorId = models.ForeignKey(
        Survivor, related_name='trade_offer_items', on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    item_quantity = models.IntegerField()

    def __str__(self):
        return f"{self.item_name} - {self.item_quantity} (TradeOffer ID: {self.TradeOfferId.id})"

