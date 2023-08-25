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

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)

    @action(detail=False, methods=['POST'])
    def custom_action(self, request, *args, **kwargs):
        return Response({'message': 'Custom action successful'}, status=status.HTTP_200_OK)

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
