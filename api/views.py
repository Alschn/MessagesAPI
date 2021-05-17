from django.db.models import F
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
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
    lookup_field = 'id'

    def get_queryset(self):
        return Message.objects.filter(id=self.kwargs[self.lookup_field])

    def retrieve(self, request, *args, **kwargs):
        """GET method handler - retrieve message with given id"""
        qs = self.get_queryset()
        if not qs.exists():
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        # use F expression to avoid race conditions
        qs.update(views=F('views') + 1)
        message = qs.first()
        # msg.views += 1
        # msg.save(update_fields=['views'])
        return Response(self.serializer_class(message).data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """PUT/PATCH method handler - update message with given id"""

        msg = self.get_object()
        msg.content = request.data.get('content')
        msg.views = 0
        msg.save(update_fields=['content', 'views'])
        return Response(self.serializer_class(msg).data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        """DELETE method handler - delete message with given it
        Inherits default behaviour.
        """
        return super().delete(request, *args, **kwargs)

# class MessagesApiView(APIView):
#     def get(self, request, *args, **kwargs):
#         """List all existing messages."""
#
#         messages = Message.objects.all()
#         serializer = MessageSerializer(messages, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def post(self, request, *args, **kwargs):
#         """Create new message."""
#
#         request_data = {
#             "content": request.data.get('content')
#         }
#         serializer = MessageSerializer(data=request_data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class MessageDestroyView(DestroyAPIView):
#     queryset = Message.objects.all()
#     serializer_class = MessageSerializer
#     lookup_field = 'id'
#
#
# class MessageUpdateView(UpdateAPIView):
#     queryset = Message.objects.all()
#     serializer_class = MessageSerializer
#     lookup_field = 'id'
#
#
# class MessageDetailsView(RetrieveAPIView):
#     queryset = Message.objects.all()
#     serializer_class = MessageSerializer
#     lookup_field = 'id'
#
#     def retrieve(self, request, *args, **kwargs):
#         msg = self.get_object()
#         msg.views += 1
#         msg.save(update_fields=['views'])
#         return Response(self.serializer_class(msg).data, status=status.HTTP_200_OK)


# class BaseManageView(APIView):
#     """
#     Dispatches requests to the appropriate views based on method.
#     Allowed methods: GET, DELETE, PUT, PATCH
#     GET         api/messages/<id>
#     DELETE      api/messages/<id>
#     PUT/PATCH   api/messages/<id>
#     """
#
#     VIEWS_BY_METHOD = {
#         'GET': MessageDetailsView.as_view,
#         'DELETE': MessageDestroyView.as_view,
#         'PUT': MessageUpdateView.as_view,
#         'PATCH': MessageUpdateView.as_view
#     }
#
#     def dispatch(self, request, *args, **kwargs):
#         if request.method in self.VIEWS_BY_METHOD:
#             return self.VIEWS_BY_METHOD[request.method]()(request, *args, **kwargs)
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

# class MessagesDetailApiView(GenericAPIView):
#     serializer_class = MessageSerializer
#     lookup_field = 'id'
#     queryset = Message.objects.all()
#
#     def get(self, request, *args, **kwargs):
#         """Retrieve message with given id."""
#         obj = self.get_object()
#         if obj:
#             obj.views += 1
#             obj.save(update_fields=['views'])
#             serializer = self.serializer_class(obj)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response({'error': f'Message not found'}, status=status.HTTP_404_NOT_FOUND)
#
#     def patch(self, request, *args, **kwargs):
#         """Update message with given id."""
#         obj = self.get_object()
#         if obj:
#             obj.content = request.data.get('content')
#             obj.views = 0
#             obj.save(update_fields=['content', 'views'])
#
#         return Response({'test': 'update'}, status=status.HTTP_204_NO_CONTENT)
#
#     def delete(self, request, *args, **kwargs):
#         """Delete a message with given id."""
#
#         return Response({'test': 'delete'}, status=status.HTTP_204_NO_CONTENT)
