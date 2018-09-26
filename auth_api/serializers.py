from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from data_api.models import Practitioner
User = get_user_model()


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id_no", "username", "telecom")


class UserRegSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        label="用户名", help_text="用户名",
        required=True, allow_blank=False,
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message="用户已经存在")])

    password = serializers.CharField(
        style={'input_type': 'password'}, help_text="密码", label="密码",
        write_only=True,
    )

    def create(self, validated_data):
        userpro = super(UserRegSerializer, self).create(validated_data=validated_data)
        userpro.set_password(validated_data["password"])
        userpro.save()

        practitioner = Practitioner.objects.create(user=userpro,name=validated_data["username"])
        practitioner.save()

        return userpro

    class Meta:
        model = User
        fields = ("username", "password")

