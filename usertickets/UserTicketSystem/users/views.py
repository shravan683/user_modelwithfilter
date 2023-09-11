
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework import viewsets, filters
import django_filters.rest_framework
from django.contrib.auth import authenticate
from .models import Ticket
from .serializers import TicketSerializer
from rest_framework.permissions import BasePermission
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import AuthenticationFailed


class IsTicketOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class TicketFilter(django_filters.FilterSet):
    id_gt = django_filters.NumberFilter(field_name='id', lookup_expr='gt')
    id_lt = django_filters.NumberFilter(field_name='id', lookup_expr='lt')

    class Meta:
        model = Ticket
        fields = ['id_gt', 'id_lt']

class TicketViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsTicketOwner]

    serializer_class = TicketSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', 'description']
    filterset_class = TicketFilter
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        if not queryset.exists():
            error_message = "No matching tickets found."
            return Response({'error': error_message}, status=status.HTTP_404_NOT_FOUND)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'])
    def custom_action(self, request, *args, **kwargs):
        return Response({'message': 'Custom action successful'}, status=status.HTTP_200_OK)

    def handle_exception(self, exc):
        if isinstance(exc, AuthenticationFailed):
            return Response({'error': 'Invalid token. Please provide a valid token.'},
                            status=status.HTTP_401_UNAUTHORIZED)
         return super().handle_exception(exc)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is not None:
        token, created = Token.objects.get_or_create(user=user)

        if created:
            print("New token created:", token.key)
        else:
            print("Existing token retrieved:", token.key)

        return Response({'token': token.key, 'message': 'Login successful'}, status=status.HTTP_200_OK)

    return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
