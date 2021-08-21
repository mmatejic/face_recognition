from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User


class Verify(APIView):
    def get(self, request, format=None):
        # DO SOMETHING
        return Response({"name": "Test Name", "surname": "Test Surname", "allowed": True})
