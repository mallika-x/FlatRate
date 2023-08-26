from django.shortcuts import render
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response

from FlatRateBackend.models import *

# Errors
BAD_FIELDS_POST = Response({"error": "bad_post_request_fields"})
SAVE_ERROR      = Response({"error": "could not save"})
GOOD            = Response(["good"])

# GET REQUESTS

# POST REQUESTS
class APIPostNewUser(APIView):
    """
    fnames  - new user's given name(s) as a single string
    sname   - new user's surname
    pii     - new user's personal documents as b64
    email   - new user's email
    photo   - new user's photo as b64
    """
    def post(self, request):
        try:
            c       = request.POST
            fnames  = c.get("fnames")
            snames  = c.get("sname")
            email   = c.get("email")
            pii     = request.FILES.get("pii")
            photo   = request.FILES.get("photo")
        except:
            return BAD_FIELDS

        add = User(fnames = fnames, snames = snames, email = email, pii = pii, photo = photo)
        try:
            add.save()
        except:
            return SAVE_ERROR

        return GOOD
