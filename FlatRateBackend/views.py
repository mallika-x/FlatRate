from django.shortcuts import render
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response

class APITestGet(APIView):
    def get(self, request):
        return Response({"text": "it worked :)"})
