from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from .models import Device, DeviceLog

User = get_user_model()


# -----------------------------
# User Authentication Serializers
# -----------------------------
class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ("name", "email", "password", "role")

    def create(self, validated_data):
        return User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            name=validated_data["name"],
            role=validated_data.get("role", "user")
        )


class UserOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "name", "email", "role")


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            request=self.context.get("request"),
            email=data.get("email"),
            password=data.get("password")
        )
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        data["user"] = user
        return data


# -----------------------------
# Device Serializers
# -----------------------------
class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ["id", "owner", "name", "type", "status", "last_active_at", "created_at", "updated_at"]
        read_only_fields = ["id", "owner", "created_at", "updated_at", "last_active_at"]

class DeviceLogSerializer(serializers.ModelSerializer):
    device = serializers.PrimaryKeyRelatedField(queryset=Device.objects.all())

    class Meta:
        model = DeviceLog
        fields = ["id", "device", "data", "timestamp"]
