# serializers.py
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Survivor, Inventory, TradeOffer, TradeOfferItems

ITEM_PRICES = {
    'water': 4,
    'food': 3,
    'medication': 2,
    'ammunition': 1
}


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ['id', 'is_locked', 'item_name',
                  'item_quantity', 'item_quantity_blocked']


class SurvivorSerializer(serializers.ModelSerializer):
    inventory = InventorySerializer(many=True)

    class Meta:
        model = Survivor
        fields = ['id', 'is_infected', 'name', 'age', 'gender',
                  'last_location_latitude', 'last_location_longitude', 'reported_by', 'inventory']

    def create(self, validated_data):
        inventory_data = validated_data.pop('inventory', [])
        reported_by_data = validated_data.pop('reported_by', [])
        survivor = Survivor.objects.create(**validated_data)
        for item in inventory_data:
            Inventory.objects.create(survivor=survivor, **item)
        survivor.reported_by.set(reported_by_data)
        return survivor

    def validate_last_location_latitude(self, value):
        if value < -90 or value > 90:
            raise ValidationError('Latitude must be between -90 and 90')
        return value

    def validate_last_location_longitude(self, value):
        if value < -180 or value > 180:
            raise ValidationError('Longitude must be between -180 and 180')
        return value

    def update(self, instance, validated_data):
        reported_by_data = validated_data.pop('reported_by', [])
        updated_instance = super().update(instance, validated_data)

        if reported_by_data:
            for survivor in reported_by_data:
                id = survivor.pk  # Extract the primary key from the Survivor object
                if updated_instance.reported_by.filter(pk=id).exists():
                    raise ValidationError(
                        f"You already reported this person with ID {id}")
                elif updated_instance.pk == id:
                    raise ValidationError("You cannot report yourself")
                else:
                    updated_instance.reported_by.add(survivor)

        reported_by_count = updated_instance.reported_by.count()

        if reported_by_count >= 3:
            updated_instance.is_infected = True
            updated_instance.save()

            Inventory.objects.filter(
                survivor=updated_instance).update(is_locked=True)

            # Find all trade offers related to the infected survivor
            trade_offers_requester = TradeOffer.objects.filter(
                requesterId=updated_instance.id)
            trade_offers_receiver = TradeOffer.objects.filter(
                receiverId=updated_instance.id)
            trade_offers = trade_offers_requester.union(trade_offers_receiver)

            for offer in trade_offers:
                # Retrieve and process trade offer items for the requester
                requester_items = TradeOfferItems.objects.filter(
                    TradeOfferId=offer.id, SurvivorId=offer.requesterId.id)
                for item in requester_items:
                    inventory_item = Inventory.objects.get(
                        survivor=offer.requesterId, item_name=item.item_name)
                    inventory_item.item_quantity_blocked -= item.item_quantity
                    inventory_item.save()

                # Retrieve and process trade offer items for the receiver
                receiver_items = TradeOfferItems.objects.filter(
                    TradeOfferId=offer.id, SurvivorId=offer.receiverId.id)
                for item in receiver_items:
                    inventory_item = Inventory.objects.get(
                        survivor=offer.receiverId, item_name=item.item_name)
                    inventory_item.item_quantity_blocked -= item.item_quantity
                    inventory_item.save()

                # Delete trade offer items
                requester_items.delete()
                receiver_items.delete()

                # Delete the trade offer
                offer.delete()
        return updated_instance


class TradeOfferSerializer2(serializers.ModelSerializer):
    requesterName = serializers.CharField(
        source='requesterId.name', read_only=True)
    receiverName = serializers.CharField(
        source='receiverId.name', read_only=True)
    requesterItems = serializers.SerializerMethodField()
    receiverItems = serializers.SerializerMethodField()

    class Meta:
        model = TradeOffer
        fields = ['id', 'requesterId', 'requesterName', 'receiverId',
                  'receiverName', 'requesterItems', 'receiverItems', 'totalPrice', 'status']

    def get_requesterItems(self, obj):
        items = TradeOfferItems.objects.filter(
            TradeOfferId=obj.id, SurvivorId=obj.requesterId.id)
        return {item.item_name: item.item_quantity for item in items}

    def get_receiverItems(self, obj):
        items = TradeOfferItems.objects.filter(
            TradeOfferId=obj.id, SurvivorId=obj.receiverId.id)
        return {item.item_name: item.item_quantity for item in items}

    def create(self, validated_data):

        requester_id = validated_data.get('requesterId').id
        receiver_id = validated_data.get('receiverId').id
        requester_items = self.initial_data.get('requesterItems')
        receiver_items = self.initial_data.get('receiverItems')
        total_trade_price = validated_data.get('totalPrice')
        trade_status = validated_data.get('status')

        if requester_items is None or receiver_items is None:
            raise ValidationError(
                {'error': 'Both requesterItems and receiverItems fields are required.'})

        # Check if requester and receiver exist and are not infected
        try:
            requester = Survivor.objects.get(
                id=requester_id, is_infected=False)
        except Survivor.DoesNotExist:
            raise ValidationError(
                {'error': 'Requester does not exist or is infected'})

        try:
            receiver = Survivor.objects.get(
                id=receiver_id, is_infected=False)
        except Survivor.DoesNotExist:
            raise ValidationError(
                {'error': 'Receiver does not exist or is infected'})

        # Check if both sides have the same trade points
        requester_total_points = sum(ITEM_PRICES.get(
            item) * quantity for item, quantity in requester_items.items())
        receiver_total_points = sum(ITEM_PRICES.get(
            item) * quantity for item, quantity in receiver_items.items())

        if requester_total_points != receiver_total_points:
            raise ValidationError({'error': 'Trade points do not match'})

        # Check if requester has enough non-blocked items
        for item_name, quantity in requester_items.items():
            inventory_item = Inventory.objects.get(
                survivor=requester, item_name=item_name)
            if inventory_item.item_quantity - inventory_item.item_quantity_blocked < quantity:
                raise ValidationError(
                    {'error': f'Requester does not have enough non-blocked {item_name}'})

        # Check if receiver has enough non-blocked items
        for item_name, quantity in receiver_items.items():
            inventory_item = Inventory.objects.get(
                survivor=receiver, item_name=item_name)
            if inventory_item.item_quantity - inventory_item.item_quantity_blocked < quantity:
                raise ValidationError(
                    {'error': f'Receiver does not have enough non-blocked {item_name}'})

        # Update item_quantity_blocked fields for requester
        for item_name, quantity in requester_items.items():
            inventory_item = Inventory.objects.get(
                survivor=requester, item_name=item_name)
            inventory_item.item_quantity_blocked += quantity
            inventory_item.save()

        # Update item_quantity_blocked fields for receiver
        for item_name, quantity in receiver_items.items():
            inventory_item = Inventory.objects.get(
                survivor=receiver, item_name=item_name)
            inventory_item.item_quantity_blocked += quantity
            inventory_item.save()

        # Create TradeOffer
        trade_offer = TradeOffer.objects.create(
            requesterId=requester,
            receiverId=receiver,
            totalPrice=total_trade_price,
            status=trade_status
        )

        # Create TradeOfferItems for requester
        for item_name, quantity in requester_items.items():
            TradeOfferItems.objects.create(
                TradeOfferId=trade_offer,
                SurvivorId=requester,
                item_name=item_name,
                item_quantity=quantity
            )

        # Create TradeOfferItems for receiver
        for item_name, quantity in receiver_items.items():
            TradeOfferItems.objects.create(
                TradeOfferId=trade_offer,
                SurvivorId=receiver,
                item_name=item_name,
                item_quantity=quantity
            )

        return trade_offer

    def update(self, instance, validated_data):
        tradeStatus = validated_data.get('status', instance.status)

        if instance.status == tradeStatus:
            raise serializers.ValidationError(
                {'error': 'Trade status is already the same'})

        if tradeStatus == "Cancel":
            requester_items = TradeOfferItems.objects.filter(
                TradeOfferId=instance, SurvivorId=instance.requesterId)
            receiver_items = TradeOfferItems.objects.filter(
                TradeOfferId=instance, SurvivorId=instance.receiverId)

            for item in requester_items:
                inventory_item = Inventory.objects.get(
                    survivor=instance.requesterId, item_name=item.item_name)
                inventory_item.item_quantity_blocked -= item.item_quantity
                inventory_item.save()

            for item in receiver_items:
                inventory_item = Inventory.objects.get(
                    survivor=instance.receiverId, item_name=item.item_name)
                inventory_item.item_quantity_blocked -= item.item_quantity
                inventory_item.save()

            requester_items.delete()
            receiver_items.delete()
            instance.delete()

            return instance

        if tradeStatus == "Approved":
            requester_items = TradeOfferItems.objects.filter(
                TradeOfferId=instance, SurvivorId=instance.requesterId)
            receiver_items = TradeOfferItems.objects.filter(
                TradeOfferId=instance, SurvivorId=instance.receiverId)

            for item in receiver_items:
                inventory_item_receiver = Inventory.objects.get(
                    survivor=instance.receiverId, item_name=item.item_name)
                inventory_item_requester, created = Inventory.objects.get_or_create(
                    survivor=instance.requesterId, item_name=item.item_name)
                inventory_item_requester.item_quantity += item.item_quantity
                inventory_item_receiver.item_quantity -= item.item_quantity
                inventory_item_receiver.item_quantity_blocked -= item.item_quantity
                inventory_item_requester.save()
                inventory_item_receiver.save()

            for item in requester_items:
                inventory_item_requester = Inventory.objects.get(
                    survivor=instance.requesterId, item_name=item.item_name)
                inventory_item_receiver, created = Inventory.objects.get_or_create(
                    survivor=instance.receiverId, item_name=item.item_name)
                inventory_item_receiver.item_quantity += item.item_quantity
                inventory_item_requester.item_quantity -= item.item_quantity
                inventory_item_requester.item_quantity_blocked -= item.item_quantity
                inventory_item_receiver.save()
                inventory_item_requester.save()

            requester_items.delete()
            receiver_items.delete()
            instance.delete()

            return instance

        instance.status = tradeStatus
        instance.save()
        return instance
