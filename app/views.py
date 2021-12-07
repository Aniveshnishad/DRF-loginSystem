from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from app.models import Banks
from app.serializers import BankSerializer


@api_view(['GET', 'POST'])
def bank_list(request):
    if request.method == "GET":
        banks = Banks.objects.all()
        bankSerializers = BankSerializer(banks, many=True)
        return JsonResponse(bankSerializers.data, safe=False)
    elif request.method == "POST":
        data = JSONParser().parse(request)
        bankSerializers = BankSerializer(data=data)
        if bankSerializers.is_valid():
            bank_name = bankSerializers.validated_data['bank_name']
            branch_name = bankSerializers.validated_data['branch_name']

            data = Banks.objects.filter(bank_name=bank_name, branch_name=branch_name)
            if data:
                return JsonResponse(bankSerializers.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            else:
                bankSerializers.save()
            return JsonResponse(bankSerializers.data, status=status.HTTP_201_CREATED)
        return JsonResponse(bankSerializers.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE', 'GET'])
def banks_actions(request, branch_name):
    try:
        details = Banks.objects.get(branch_name=branch_name)
    except Banks.DoesNotExist:
        return JsonResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        Bank_details = BankSerializer(details)
        return Response(Bank_details.data)
    elif request.method == "PUT":
        bank_details = BankSerializer(details, data=request.data)
        if bank_details.is_valid():
            bank_details.save()
            return Response(bank_details.data)
        return Response(bank_details.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        details.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
