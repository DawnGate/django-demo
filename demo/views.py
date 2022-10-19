from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from datetime import datetime

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import FormParser
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .models import Deposit, User, Wallet, Withdrawn
from .serializers import UserSerializer, WalletSerializer


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
        user_serializer =  UserSerializer(data={'xid': customer_xid})
        if not user_serializer.is_valid():
            return Response({
                "status": "error",
                "message": user_serializer.errors
            }, status = status.HTTP_400_BAD_REQUEST)
        new_user =user_serializer.save()
        print(new_user)
        # create new wallet
        wallet_serializer = WalletSerializer( data = {"owned_by" : new_user.id})
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

def middlewareAuthen(request):
    header_author = request.META.get("HTTP_AUTHORIZATION")
    if not header_author:
        return (False, Response({"status": "error", "message": "Authorization"}, status=status.HTTP_404_NOT_FOUND))
    [token_string, token_raw] = header_author.split(" ")
    if not token_string == "Token" or not token_raw :
        return (False,Response({"status": "error", "message": "Authorization not correct format"}, status=status.HTTP_403_FORBIDDEN))
    try:
        found_token = Token.objects.get(pk = token_raw)
    except:
        return (False, Response({"status": "error", "message": "Fail authorization"}, status=status.HTTP_403_FORBIDDEN))
    user = found_token.user
    wallet = Wallet.objects.get(owned_by = user)
    return (True, (user,wallet))

class ActiveWallet(APIView):
    def post(self, request):
        (status_return, res_result) = middlewareAuthen(request)
        if not status_return: return res_result
        (_, wallet) = res_result
        if wallet.enabled_at and not wallet.disabled_at:
           return Response({"status": "error", "message": "Already enabled"}, status=status.HTTP_400_BAD_REQUEST) 
        wallet.enabled_at = datetime.now()
        wallet.disabled_at = None 
        wallet.status = "ENA"
        wallet.save()
        res_data = {
            "id": str(wallet.pk),
            "owned_by": str(wallet.owned_by),
            "status": wallet.get_status_display(),
            "enabled_at": wallet.enabled_at.isoformat(),
            "balance": wallet.balance,
        }
        return Response({"status": "success", "data": {
            "wallet": res_data 
        }}, status=status.HTTP_200_OK)

    def get(self,request):
        (status_return, res_result) = middlewareAuthen(request)
        if not status_return: return res_result
        (_, wallet) = res_result
        if wallet.disabled_at:
           return Response({"status": "error", "message": "This wallet has disabled"}, status=status.HTTP_400_BAD_REQUEST) 
        res_data = {
            "id": str(wallet.pk),
            "owned_by": str(wallet.owned_by),
            "status": wallet.get_status_display(),
            "enabled_at": wallet.enabled_at.isoformat(),
            "balance": wallet.balance,
        }
        return Response({"status": "success", "data": {
            "wallet": res_data 
        }}, status=status.HTTP_200_OK)

    def patch(self,request):

        (status_return, res_result) = middlewareAuthen(request)
        if not status_return: return res_result
        try: 
            is_disabled = request.data["is_disabled"]
            if is_disabled != "true":
                raise ValueError("is_disable must be true")
        except:
            return Response({
                "status": "fail", 
                "data": {
                    "is_disabled": "This field is required and only accept true value"
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        (_, wallet) = res_result
        if wallet.enabled_at and wallet.disabled_at:
           return Response({"status": "error", "message": "Already disabled"}, status=status.HTTP_400_BAD_REQUEST) 
        if not wallet.enabled_at:
           return Response({"status": "error", "message": "Wallet not enabled"}, status=status.HTTP_400_BAD_REQUEST) 
        wallet.disabled_at = datetime.now()
        wallet.status = "DIS"
        wallet.save()
        res_data = {
            "id": str(wallet.pk),
            "owned_by": str(wallet.owned_by),
            "status": wallet.get_status_display(),
            "enabled_at": wallet.enabled_at.isoformat(),
            "balance": wallet.balance,
        }
        return Response({"status": "success", "data": {
            "wallet": res_data 
        }}, status=status.HTTP_200_OK)

class CreateDeposit(APIView):
    def post(self, request):
        (status_return, res_result) = middlewareAuthen(request)
        
        if not status_return: return res_result
        try: 
            amount = request.data["amount"]
            ref_id = request.data["reference_id"]
            if not amount or not ref_id or int(amount) <= 0:
                raise ValueError("amount and redId")
        except:
            return Response({
                "status": "fail", 
                "data": {
                    "amount": "amount required",
                    "reference_id": "reference_id required"
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        (user, wallet) = res_result
        if wallet.disabled_at:
           return Response({"status": "error", "message": "This wallet has disabled"}, status=status.HTTP_400_BAD_REQUEST) 
        try:
            deposit = Deposit(ref_id = ref_id, deposit_by = user, amount = int(amount), status = "SUCC")
            deposit.save()
            wallet.balance += int(amount)
            wallet.save()
        except:
            return Response({"status": "error", "message": "Some problem occur maybe ref_id has already exist"}, status=status.HTTP_400_BAD_REQUEST)
        res_data = {
            "id": str(deposit.pk),
            "deposit_by": str(deposit.deposit_by),
            "status": deposit.get_status_display(),
            "deposit_at": deposit.deposit_at.isoformat(),
            "amount": deposit.amount,
            "reference_id": deposit.ref_id
        } 
        return Response({"status": "success", "data": {
            "deposit": res_data 
        }}, status=status.HTTP_200_OK)

class CreateWidthdrawn(APIView):
    def post(self, request):
        (status_return, res_result) = middlewareAuthen(request)
        
        if not status_return: return res_result
        try: 
            amount = request.data["amount"]
            ref_id = request.data["reference_id"]
            if not amount or not ref_id or int(amount) <= 0:
                raise ValueError("amount and redId")
        except:
            return Response({
                "status": "fail", 
                "data": {
                    "amount": "amount required",
                    "reference_id": "reference_id required"
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        (user, wallet) = res_result
        if wallet.disabled_at:
           return Response({"status": "error", "message": "This wallet has disabled"}, status=status.HTTP_400_BAD_REQUEST) 
        try:
            can_withdrawn = int(amount) <= wallet.balance
            withdrawn = Withdrawn(ref_id = ref_id, withdrawn_by = user, amount = int(amount), status = "SUCC" if can_withdrawn else "FAIL")
            withdrawn.save()
            if can_withdrawn: 
                wallet.balance -= int(amount)
                wallet.save()
        except Exception as e:
            print(e)
            return Response({"status": "error", "message": "Some problem occur maybe ref_id has already exist"}, status=status.HTTP_400_BAD_REQUEST)
        res_data = {
            "id": str(withdrawn.pk),
            "withdrawn_by": str(withdrawn.withdrawn_by),
            "status": withdrawn.get_status_display(),
            "withdrawn_at": withdrawn.withdrawn_at.isoformat(),
            "amount": withdrawn.amount,
            "reference_id": withdrawn.ref_id
        } 
        return Response({"status": "success", "data": {
            "withdrawal": res_data 
        }}, status=status.HTTP_200_OK)