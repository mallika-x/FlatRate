from django.shortcuts           import render
from rest_framework.parsers     import JSONParser
from rest_framework.views       import APIView
from rest_framework.response    import Response

from FlatRateBackend.models import *
from .constants             import *

# Errors
BAD_FIELDS_POST = Response({"error": "bad_post_request_fields"})
SAVE_ERROR      = Response({"error": "could not save"})
GOOD            = Response(["good"])

# GET REQUESTS
class APITryLogin(APIView):
    """
    username - email of user attempting to log in
    """
    def get(self, request):
        try:
            uname = request.GET.get("username")
        except:
            return BAD_FIELDS

        resp = None
        if User.objects.filter(email = uname).exists():
            resp = Response({"access": "approved"})
        else:
            resp = Response({"access": "denied"})

        return resp

# POST REQUESTS
class APIPostNewUser(APIView):
    """
    fnames  - new user's given name(s) as a single string
    sname   - new user's surname
    pii     - new user's personal documents as b64
    email   - new user's email
    photo   - new user's photo as b64
    leaseid - lease ID from RTA or "0" if n/a
    """
    def post(self, request):
        try:
            c       = request.POST
            fnames  = c.get("fnames")
            snames  = c.get("sname")
            email   = c.get("email")
            leaseid = c.get("leaseid")
            pii     = request.FILES.get("pii")
            photo   = request.FILES.get("photo")
        except:
            return BAD_FIELDS

        add = User(fnames = fnames, snames = snames, email = email, pii = pii, photo = photo)
        try:
            add.save()
        except:
            return SAVE_ERROR

        creds = SocialCredits(user = add, score = DEFAULT_SOCIAL_CREDITS)
        try:
            creds.save()
        except:
            add.delete()
            return SAVE_ERROR

        if (leaseid):
            search = Lease.objects.filter(leaseID = leaseid)
            if search.exists():
                new_mate = Flatmates(lease = search, user = add)
                try:
                    new_mate.save()
                except:
                    creds.delete()
                    add.delete()
                    return SAVE_ERROR
            else:
                creds.delete()
                add.delete()
                return Response({"error": "invalid-lease-id"})

        # no else?


        return GOOD

# NEVER TOUCH THIS
class APIBurnEverything(APIView):
    def post(self, request):
        tables = [
                User,
                SocialCredits,
                #Lease,
                #Flatmates,
                #Chores,
                #AciveChores,
                #PastChores,
                #Schedule,
                #ScheduleSet,
                #Notifications
        ]
        for t in tables:
            for r in t.objects.all():
                r.delete()

        return Response({"Killed everything"})
