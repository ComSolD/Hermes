from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import render


class HomePage(APIView):

    def get(self, request, *args, **kwargs):
        
        return Response({"message": "Гермес - путеводитель по статистике!"})
