from rest_framework import generics
from rest_framework.filters import SearchFilter
from accounts.models import VetProfile
from vet.serializers import VetSingleSerializer

#from django_filters.rest_framework import DjangoFilterBackend


class VetSearchView(generics.ListAPIView):
    queryset = VetProfile.objects.all()
    serializer_class = VetSingleSerializer
    filter_backends = [SearchFilter]
    search_fields = ['first_name', 'last_name', 'about']