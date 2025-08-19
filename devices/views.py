from django.shortcuts import render
from .serializers import DeviceSerializer
from .serializers import LoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,viewsets
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .models import Device, DeviceLog
from .serializers import SignupSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from django.db.models import Sum
from datetime import timedelta
from .serializers import DeviceSerializer, DeviceLogSerializer

class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all().order_by('-created_at')
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['type', 'status']
    search_fields = ['name']

    def perform_create(self, serializer):
        # Automatically assign the logged-in user as owner
        serializer.save(owner=self.request.user)

    # Heartbeat
    @action(detail=True, methods=['get', 'post'])
    def heartbeat(self, request, pk=None):
        device = self.get_object()
        if request.method == "POST":
            status_value = request.data.get("status")
            device.heartbeat(status=status_value)
            return Response({
                "success": True,
                "message": "Device heartbeat recorded",
                "last_active_at": device.last_active_at
            })
        else:  # GET method
            return Response({
                "success": True,
                "device": {
                    "id": str(device.id),
                    "name": device.name,
                    "status": device.status,
                    "last_active_at": device.last_active_at
                }
            })
    # Logs
    @action(detail=True, methods=['post', 'get'])
    def logs(self, request, pk=None):
        device = self.get_object()
        if request.method == 'POST':
            serializer = DeviceLogSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(device=device)
            return Response({"success": True, "log": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            limit = int(request.query_params.get("limit", 10))
            logs = device.logs.all()[:limit]
            serializer = DeviceLogSerializer(logs, many=True)
            return Response({"success": True, "logs": serializer.data})

    # Usage
    @action(detail=True, methods=['get'])
    def usage(self, request, pk=None):
        device = self.get_object()
        range_param = request.query_params.get("range", "24h")
        try:
            hours = int(range_param.rstrip("h"))
        except ValueError:
            hours = 24
        since = timezone.now() - timedelta(hours=hours)
        total = device.logs.filter(timestamp__gte=since, event="units_consumed") \
                           .aggregate(total_units=Sum("value"))["total_units"] or 0
        return Response({
            "success": True,
            "device_id": str(device.id),
            "total_units_last_24h": total
        })


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        # Use SimpleJWT to generate valid tokens
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role
            }
        }, status=status.HTTP_200_OK)


class SignupView(APIView):
    permission_classes = [AllowAny]   #allow signup without token

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
