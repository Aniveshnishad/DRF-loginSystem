from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from app.models import Banks


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banks
        fields = ['bank_name', 'branch_name', 'bank_address', 'IFSC_code']
