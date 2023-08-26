from django.shortcuts           import render
from rest_framework.parsers     import JSONParser, MultiPartParser, FormParser
from rest_framework.views       import APIView
from rest_framework.response    import Response

from FlatRateBackend.models import *
from .constants             import *

from random     import randint
from datetime   import datetime

flatten = lambda ll: [] if len(ll) == 0 else ll[0] + flatten(ll[1:])

# Errors
NEXIST_FLD  = Response({"error": "field doesn't exist"})
BAD_FIELDS  = Response({"error": "bad_request_fields"})
SAVE_ERROR  = Response({"error": "could not save"})
GOOD        = Response(["good"])

# NEVER TOUCH THIS
class APIBurnEverything(APIView):
    def post(self, request):
        tables = [
                #SocialCredits,
                #Flatmates,
                ChoreTallies,
                PastChores,
                ActiveChores,
                Chores,
                Lease,
                #Schedule,
                #ScheduleSet,
                #Notifications
                #User
        ]
        for t in tables:
            for r in t.objects.all():
                if t != Lease or "Bracken Ridge" not in r.address:
                    # This is abyssmal
                    try:
                        r.delete()
                    except:
                        pass

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
        tally = ChoreTallies(user = add, completed = 0, skipped = 0)
        creds.save()
        tally.save()

        if (leaseid):
            search = Lease.objects.filter(leaseID = leaseid)
            if search.exists():
                new_mate = Flatmates(lease = search[0], user = add)
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
            new_lease_id = new_mate.lease.leaseID
        else:
            new_lease_id = -1 * randint(1, LARGE_ENOUGH)
            new_lease = Lease(address = addr, leaseID = new_lease_id)
            new_lease.save() # just pray for no collisions
            new_mates = Flatmates(lease = new_lease, user = user)
            new_mates.save()

        return Response({"good": new_lease_id})

# Chore things
class APIGetChoreTypes(APIView):
    """No params, returns list<str>"""
    def get(self, request):
        return Response({c.id: c.name for c in ChoreTypes.objects.all()})

class APICreateChore(APIView):
    """
    type    - ID of chore type, see api-get-chore-types
    weight  - 0/5/10/20
    owner   - user responsible
    expiry  - date & time chore is due
    """
    def post(self, request):
        try:
            c       = request.POST
            ctype   = int(c.get("type"))
            weight  = int(c.get("weight"))
            owner   = c.get("owner")
            expiry  = datetime.strptime(c.get("expiry"), DATETIME_FMT)
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
        activeChores = [c for c in chores if ActiveChores.objects.filter(chore = c).exists()]
        return Response([c.id for c in activeChores])

class APIGetOthersChores(APIView):
    """
    leaseid - lease ID corresponding to the flatmates group
    exclude - email of the person not to include
    """
    def get(self, request):
        try:
            leaseID = int(request.GET.get("leaseid"))
            uname   = request.GET.get("exclude")
            lease   = Lease.objects.filter(leaseID = leaseID)[0]
            exclude = User.objects.filter(email = uname)[0]
        except:
            return BAD_FIELDS

        mates       = Flatmates.objects.filter(lease = lease)
        others      = [m.user for m in mates if m.user != exclude]
        totChores   = [list(Chores.objects.filter(responsible = m)) for m in others]
        flat        = flatten(totChores)

        return Response([f.id for f in flat if ActiveChores.objects.filter(chore = f).exists()])

class APICompleteChore(APIView):
    """
    chore       - id of chore to complete
    completer   - email of user who completed it
    """
    def post(self, request):
        try:
            choreid = int(request.GET.get("chore"))
            uname   = request.GET.get("completer")
            chore   = Chores.objects.filter(id = choreid)[0]
            user    = User.objects.filter(email = uname)[0]
        except:
            return BAD_FIELDS

        active = ActiveChores.objects.filter(chore = chore)
        if not active.exists():
            return Response({"error": "chore-nonactive"})
        activeChore = active[0]

        if chore.responsible is not None and chore.responsible != user:
            badSC = SocialCredits.objects.filter(user = chore.responsible)[0]
            badSC.score -= chore.weight // 2
            badSC.delete()
            badSC.save()

            badtally = ChoreTallies.objects.filter(user = chore.responsible)[0]
            badtally.skipped += 1
            badtally.save()

            goodtally = ChoreTallies.objects.filter(user = user)[0]
            goodtally.completed += 1
            goodtally.save()

            goodSC = SocialCredits.objects.filter(user = user)[0]
            goodSC.score += chore.weight
            goodSC.save()
        elif chore.responsible is not None and chore.responsible == user:
            now = datetime.now()
            if now <= activeChore.expiry:
                goodtally = ChoreTallies.objects.filter(user = user)[0]
                goodtally.completed += 1
                goodtally.save()

        activeChore.delete()
        newPast = PastChores(chore = chore, responsible = chore.responsible, completer = user)
        newPast.save()

        return GOOD

class APIGetTallies(APIView):
    """
    leaseid - lease ID for flatmates to get the tallies for
    """
    def get(self, request):
        try:
            leaseid = int(request.GET.get("leaseid"))
            lease   = Lease.objects.filter(leaseID = leaseid)[0]
        except:
            return BAD_FIELDS

        mates = Flatmates.objects.filter(lease = lease)
        fmusers = [f.user for f in mates]
        tallies = [ChoreTallies.objects.filter(user = m)[0] for m in fmusers]
        uids = [u.email for u in fmusers]
        tallyNums = [(t.completed, t.skipped) for t in tallies]
        out = dict(zip(uids, tallyNums))

        return Response(out)


class APIGetFlatmates(APIView):
    """
    uname   - email of user to get the flatmates of
    """
    def get(self, request):
        try:
            uname = request.GET.get("uname")
            user = User.objects.filter(email = uname)[0]
        except:
            return BAD_FIELDS

        lease = Flatmates.objects.filter(user = user)[0].lease
        mates = [f.user.email for f in Flatmates.objects.filter(lease = lease) if f.user != user]

        return Response(mates)
