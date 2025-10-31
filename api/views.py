from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status, generics
from .serializers import UsernameTokenObtainPairSerializer, RegisterSerializer, LogoutSerializer, SliderSerializer, MovieSerializer, ProfileSerializer
from rest_framework.views import APIView
from .models import Slider, Movie, Profile
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

class LoginView(TokenObtainPairView):
    serializer_class = UsernameTokenObtainPairSerializer

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)            
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': "Qeydiyyat ugurla həyata keçirildi",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    'username': user.username,
                    'user_id': user.id,
                }
                
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LogoutView(APIView):
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': "Ugurlu"}, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class SliderView(generics.ListAPIView):
    queryset = Slider.objects.filter(is_active=True).select_related('movie').order_by('order')
    serializer_class  = SliderSerializer

class MovieView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class  = MovieSerializer

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        profile = request.user.profile
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Avatar has been updated"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)