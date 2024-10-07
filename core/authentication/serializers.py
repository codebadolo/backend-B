from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'profile_image', 'country', 'city', 'address', 'phone_number', 'date_of_birth',
            'kyc_document_type', 'kyc_document_image', 'kyc_status'
        )

class KYCSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('kyc_document_type', 'kyc_document_image', 'kyc_status')
        read_only_fields = ['kyc_status']


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'profile')

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        profile = instance.profile

        # Update user fields
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        # Update profile fields
        profile.profile_image = profile_data.get('profile_image', profile.profile_image)
        profile.country = profile_data.get('country', profile.country)
        profile.city = profile_data.get('city', profile.city)
        profile.address = profile_data.get('address', profile.address)
        profile.phone_number = profile_data.get('phone_number', profile.phone_number)
        profile.date_of_birth = profile_data.get('date_of_birth', profile.date_of_birth)
        profile.save()

        return instance


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    profile = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'profile')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        # Create associated profile instance for the user
        Profile.objects.create(user=user)
        return user