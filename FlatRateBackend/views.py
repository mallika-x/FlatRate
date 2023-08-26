from django.shortcuts           import render
from rest_framework.parsers     import JSONParser, MultiPartParser, FormParser
from rest_framework.views       import APIView
from rest_framework.response    import Response

from FlatRateBackend.models import *
from .constants             import *

from random     import randint
from datetime   import datetime

# Errors
NEXIST_FLD  = Response({"error": "field doesn't exist"})
BAD_FIELDS  = Response({"error": "bad_request_fields"})
SAVE_ERROR  = Response({"error": "could not save"})
GOOD        = Response(["good"])

# NEVER TOUCH THIS
class APIBurnEverything(APIView):
    def post(self, request):
        tables = [
                SocialCredits,
                Lease,
                #Flatmates,
                Chores,
                ActiveChores,
                #PastChores,
                #Schedule,
                #ScheduleSet,
                #Notifications
                User
        ]
        for t in tables:
            for r in t.objects.all():
                r.delete()

        return Response({"Killed everything"})

# Account things
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

class APIPostNewUser(APIView):
    """
    fnames  - new user's given name(s) as a single string
    sname   - new user's surname
    leaseid - lease ID from RTA or 0 if n/a
    email   - new user's email
    """
    def post(self, request):
        try:
            c       = request.POST
            fnames  = c.get("fnames")
            sname   = c.get("sname")
            email   = c.get("email")
            leaseid = int(c.get("leaseid"))
        except:
            return NEXIST_FLD

        add = User(fnames = fnames, sname = sname, email = email)
        try:
            add.save()
        except:
            print("no")
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
                #creds.delete()
                #add.delete()
                return Response({"accepted": "needs-address"})
        else:
            return Response({"accepted": "needs-address"})


        return GOOD

class APIResolveAddress(APIView):
    """
    uname   - email of user
    address - address of their house/flat
    """

    def post(self, request):
        try:
            uname   = request.POST.get("uname")
            addr    = request.POST.get("address").lower().replace("  ", " ")
            user    = User.objects.filter(email = uname).all()[0]
        except:
            return BAD_FIELDS

        lease = Lease.objects.filter(address = addr)
        if (lease.exists()):
            new_mate = Flatmates(user = user, lease = lease.all()[0])
        else:
            new_lease_id = -1 * randint(1, LARGE_ENOUGH)
            new_lease = Lease(address = addr, leaseID = new_lease_id)
            new_lease.save() # just pray for no collisions
            new_mates = Flatmates(lease = new_lease, user = user)
            new_mates.save()

        return GOOD

# Chore things
class APIGetChoreTypes(APIView):
    """No params, returns list<str>"""
    def get(self, request):
        return Response({c.id: c.name for c in ChoreTypes.objects.all()})

class APICreateChore(APIView):
    """
    type    - ID of chore type, see api-get-chore-types
    weight  - 0/5/10/20
    owner   - user responsible or "" for none responsible
    expiry  - date & time chore is due
    """
    def post(self, request):
        try:
            c       = request.POST
            print(1)
            ctype   = int(c.get("type"))
            print(2)
            weight  = int(c.get("weight"))
            print(3)
            owner   = c.get("owner")
            print(4, c.get("expiry"))
            expiry  = datetime.strptime(c.get("expiry"), DATETIME_FMT)
            print(5)
            rtype   = ChoreTypes.objects.filter(id = ctype)[0]
            userrsp = User.objects.filter(email = owner)[0]
        except:
            return BAD_FIELDS

        add = Chores(choreType = rtype, weight = weight, responsible = userrsp)
        try:
            add.save()
        except:
            return SAVE_ERROR

        active = ActiveChores(chore = add, expiry = expiry)
        try:
            active.save()
        except:
            add.delete()
            return SAVE_ERROR

        return GOOD

class APIGetUserChores(APIView):
    """
    uname   - email of user to get the chores for.
    Returns chore IDs to query further
    """
    def get(self, request):
        try:
            uname   = request.GET.get("uname")
            user    = User.objects.filter(email = uname)[0]
        except:
            return BAD_FIELDS

        chores = Chores.objects.filter(responsible = user)
        return Response([c.id for c in chores])
