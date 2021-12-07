from django.contrib.auth.models import User
from django.db.migrations import serializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from login.models import ListUser


class RegisteredUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']
        # extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('id',)


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)



    # def create(self, validated_data):
    #     user = User.objects.create(
    #         username=validated_data['username'],
    #         email=validated_data['email'],
    #         first_name=validated_data['first_name'],
    #         last_name=validated_data['last_name']
    #     )
    #
    #     user.set_password(validated_data['password'])
    #     user.save()
    #
    #     return user

    # extra_kwargs = {
    #     'password': {'write_only': True},
    # }

    # def create(self, validated_data):
    #     user = User.objects.create_user(validated_data['first_name'],
    #                                     validated_data['last_name'],
    #                                     validated_data['username'],
    #                                     validated_data['email'],
    #                                     validated_data['password'])
    #     return user

#
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = '__all__'
