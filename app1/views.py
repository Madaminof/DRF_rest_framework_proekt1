
from .models import Data
from .serializers import DataSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets


class DataViewsets(viewsets.ModelViewSet):
    queryset = Data.objects.all()
    serializer_class = DataSerializer


