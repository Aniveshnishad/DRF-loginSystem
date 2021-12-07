from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, generics, request
from rest_framework.decorators import api_view
from rest_framework.generics import UpdateAPIView
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import Token
from rest_framework_simplejwt.views import TokenObtainPairView

from login.models import ListUser
from login.serializers import RegisteredUserSerializer, UpdateUserSerializer, ChangePasswordSerializer


class Registered_User(APIView):
    def get(self, request, format=None):
        details = User.objects.all()
        serializer = RegisteredUserSerializer(details, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = RegisteredUserSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']

            details = User.objects.all()
            for i in details:
                registered_email = i.email
            if email != registered_email:
                serializer.save()
                # return Response(status=status.HTTP_400_BAD_REQUEST)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "This Email is already registered."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Profile(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            user = request.user
            return user
        except User.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        details = request.user
        serializer = RegisteredUserSerializer(details)
        return Response(serializer.data)

    def put(self, request, format=None):
        user = request.user
        serializer = UpdateUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
            # email = serializer.validated_data['email']
            #
            # details = User.objects.all()
            # for i in details:
            #     registered_email = i.email
            # if email != registered_email:
            #     serializer.save()
            #     # return Response(status=status.HTTP_400_BAD_REQUEST)
            #     return Response({"msg":"Updated successfully","user":serializer.data},status=status.HTTP_201_CREATED)
            # else:
            #     return Response({"error": "This Email is already registered"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        user = request.user

        user.delete()
        return Response({"msg": "User deleted Successfully"}, status=status.HTTP_204_NO_CONTENT)


class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": "Wrong password"}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': [serializer.data]
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

