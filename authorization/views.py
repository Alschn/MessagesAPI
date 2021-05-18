from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from authorization.serializers import RegisterUserSerializer, UserSerializer


class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User Created Successfully!",
        })
