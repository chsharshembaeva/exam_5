from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, Author
from .serializers import RegisterSerializer


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        if user:
            Author.objects.create(user=user)

#
# class ObtainAuthToken(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({'token': token.key})













