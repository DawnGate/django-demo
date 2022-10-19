from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.parsers import FormParser
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .models import User, Wallet
from .serializers import UserSerializer, WalletSerializer

import json


class InitUser(APIView):
    parser_classes = [FormParser]
    def post(self, request):
        try: 
            customer_xid = request.data["customer_xid"]
        except:
            return Response({
                "status": "fail", 
                "data": {
                    "customer_xid": "customer_xid is required"
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        # create new user
        user_serializer =  UserSerializer(data={'id': customer_xid})
        if not user_serializer.is_valid():
            return Response({
                "status": "error",
                "message": user_serializer.errors
            }, status = status.HTTP_400_BAD_REQUEST)
        new_user =user_serializer.save()
        print(user_serializer.data)
        # create new wallet
        wallet_serializer = WalletSerializer( data = {"owned_by" : user_serializer.data['id']})
        if not wallet_serializer.is_valid():
            return Response({
                "status": "error",
                "message": wallet_serializer.errors
            }, status = status.HTTP_400_BAD_REQUEST)
        wallet_serializer.save()
        #create authen code for user
        token = Token.objects.create(user=new_user)
        return Response({
            "status": "success",
            "data": {
                "token": token.key
            }
        }, status=status.HTTP_200_OK) 