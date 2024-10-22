from rest_framework import serializers

class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class ResetPassowrdSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only = True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

