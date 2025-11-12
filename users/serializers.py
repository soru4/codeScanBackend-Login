from rest_framework import serializers
from django.contrib.auth.models import User # <-- Use default User model

class UserRegistrationSerializer(serializers.ModelSerializer):
    # Field to confirm password during registration
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        # Fields for registration (username is the login ID)
        fields = ('username', 'email', 'password', 'password2')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }

    def validate(self, data):
        # Ensure passwords match
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return data

    def create(self, validated_data):
        # Uses the built-in default User model method to hash the password securely
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        # --- Email Verification Hook ---
        # If implementing email verification:
        # user.is_active = False  # Set to False by default
        # user.save()
        # Trigger email sending here with a verification link (deep link)
        return user