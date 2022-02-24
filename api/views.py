#django
from django.contrib.auth import login

#rest-framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView,ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

#serializers
from .serializers import RegisterSerializer,UserSerializer,RefreshTokenSerializer



def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token = get_tokens_for_user(user)
        login(request, user)
        return Response({
            "user"  : UserSerializer(user,context=serializer).data,
            "token" : token
        },status= status.HTTP_201_CREATED)

class BlacklistTokenUpdateView(GenericAPIView):
    permission_classes = [AllowAny]
    authentication_classes = ()
    serializer_class = RefreshTokenSerializer

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)