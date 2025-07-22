from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Slider, Movie, MovieImage, Profile

class UsernameTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data =  super().validate(attrs)
        data['username'] = self.user.username
        data['avatar'] = self.user.profile.avatar.url if self.user.profile.avatar else None
        return data
    
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    repeat_password = serializers.CharField(write_only=True)
    fullname = serializers.CharField(write_only=True)
    avatar = serializers.ImageField(write_only=True, required = False)
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeat_password', 'fullname', 'avatar']

    def validate(self, data):
        if data['password'] != data['repeat_password']:
            raise serializers.ValidationError("The passwords are not the same")
        return data
    
    def create(self, validated_data):
        full_name = validated_data.pop('fullname')
        password = validated_data.pop('password')
        validated_data.pop('repeat_password')
        name_parts = full_name.strip().split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ""
        avatar = validated_data.pop('avatar', None)
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            password=password,
            **validated_data
        )
        if avatar:
            user.profile.avatar = avatar
            user.profile.save()
        return user 

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    
    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            raise ValidationError('Token keçərli deyil və ya artıq qara siyahıdadır.')

class MovieImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieImage
        fields = ['id', 'image']

class MovieSerializer(serializers.ModelSerializer):
    images = MovieImageSerializer(many=True, read_only=True)
    class Meta:
        model = Movie
        fields = '__all__'

class SliderSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    class Meta:
        model = Slider
        exclude = ['is_active']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['avatar']