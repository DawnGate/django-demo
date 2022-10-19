from rest_framework import serializers

from .models import User, Wallet, Deposit, Withdrawn

class UserSerializer(serializers.ModelSerializer):
    class Meta:  
        model = User
        fields = ['xid']

class WalletSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Wallet
        fields = ['status', 'enabled_at', 'disabled_at', 'balance', 'owned_by']

    def create(self, validated_data):
        owned_by = validated_data.pop('owned_by')
        wallet = Wallet.objects.create(owned_by = owned_by)
        return wallet

class DepositSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Deposit
        fields = ['amount', 'ref_id', 'widthdrawn_by', 'amount', 'withdrawn_at', 'status']

class WidthdrawnSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Withdrawn
        fields = ['amount', 'ref_id', 'deposit_by', 'amount', 'deposit_at', 'status']

