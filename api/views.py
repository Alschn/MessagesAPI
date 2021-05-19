from django.db.models import F
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from api.models import Message
from api.serializers import MessageSerializer


class ListCreateMessageAPIView(ListCreateAPIView):
    """
    Allowed methods: GET, POST
    GET   api/messages  - lists all messages
    POST  api/messages  - creates message with given content
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        """GET method handler
        Inherits default behaviour of ListCreateAPIView's list method
        """
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """POST method handler.
        Inherits default behaviour of ListCreateAPIView's create method
        """
        return super().create(request, *args, **kwargs)


class GetUpdateDeleteMessageAPIView(RetrieveUpdateDestroyAPIView):
    """
    Allowed methods: GET, DELETE, PUT, PATCH
    GET         api/messages/<id>
    DELETE      api/messages/<id>
    PUT/PATCH   api/messages/<id>
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'id'

    def get_queryset(self):
        return Message.objects.filter(id=self.kwargs[self.lookup_field])

    def retrieve(self, request, *args, **kwargs):
        """GET method handler - retrieve message with given id"""
        qs = self.get_queryset()
        if not qs.exists():
            return Response({'error': 'Message not found!'}, status=status.HTTP_404_NOT_FOUND)

        qs.update(views=F('views') + 1)  # use F expression to avoid race conditions
        instance = qs.first()  # there will be only one object since id is unique
        return Response(self.get_serializer(instance).data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """PUT/PATCH method handler - update message with given id"""
        message = self.get_object()
        serializer = self.get_serializer(message, data={
            'content': request.data.get('content'),
            'views': 0,
        })
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        """DELETE method handler - delete message with given it
        Inherits default behaviour.
        """
        return super().delete(request, *args, **kwargs)
