from rest_framework import generics
from rest_framework.filters import SearchFilter
from ..models import Product
from ..serializers import ProductGetSerializer

#from django_filters.rest_framework import DjangoFilterBackend


class ProductSearchView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductGetSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']