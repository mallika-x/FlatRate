from django.shortcuts           import render
from rest_framework.parsers     import JSONParser, MultiPartParser, FormParser
from rest_framework.views       import APIView
from rest_framework.response    import Response

from django.http import FileResponse

from FlatRateBackend.models import *
from .constants             import *

from random     import randint
from datetime   import datetime
from csv        import reader, writer
from os         import path

import  matplotlib.pyplot   as      plt
from    matplotlib.colors   import  LinearSegmentedColormap

flatten = lambda ll: [] if len(ll) == 0 else ll[0] + flatten(ll[1:])
ct2n    = lambda i: ChoreTypes.objects.filter(id = i)[0].name
d2s     = lambda d: d.strftime(DATE_FMT)
u2n     = lambda u: u.fnames.split()[0] + " " + u.sname

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
                #ChoreTallies,
                PastChores,
                ActiveChores,
                Chores,
                #Lease,
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
        search = User.objects.filter(email = uname)
        if search.exists():
            leaseid = Flatmates.objects.filter(user = search[0])[0].lease.leaseID
            resp = Response({"access": "approved", "leaseid": leaseid})
        else:
            resp = Response({"access": "denied"})

        return resp

class APIPostNewUser(APIView):
    """
    fnames  - new user's given name(s) as a single string
    sname   - new user's surname
    leaseid - lease ID from RTA or 0 if n/a
    email   - new user's email
    address - new user's address
    """
    def post(self, request):
        try:
            c       = request.POST
            fnames  = c.get("fnames")
            sname   = c.get("sname")
            email   = c.get("email")
            leaseid = int(c.get("leaseid"))
            address = c.get("address").replace("  ", "")
        except:
            return NEXIST_FLD

        if User.objects.filter(email = email).exists():
            return Response({"error": "duplicate_user"})

        add = User(fnames = fnames, sname = sname, email = email)
        add.save()

        if not SocialCredits.objects.filter(user = add).exists():
            creds = SocialCredits(user = add, score = DEFAULT_SOCIAL_CREDITS)
            creds.save()

        if not ChoreTallies.objects.filter(user = add).exists():
            tally = ChoreTallies(user = add, completed = 0, skipped = 0)
            tally.save()

        if (leaseid):
            search = Lease.objects.filter(leaseID = leaseid)
            if search.exists():
                lease = search[0]
                new_mate = Flatmates(lease = lease, user = add)
                new_mate.save()
            else:
                addrSearch = Lease.objects.filter(address = address)
                if addrSearch.exists():
                    lease = addrSearch[0]
                    newMate = Flatmates(lease = lease, user = add)
                    newMate.save()
                else:
                    lease = Lease(leaseID = leaseid, address = address)
                    lease.save()
                    newMates = Flatmates(lease = lease, user = add)
                    newMates.save()
        else:
            addrSearch = Lease.objects.filter(address = address)
            if addrSearch.exists():
                lease = addrSearch[0]
                newMate = Flatmates(lease = lease, user = add)
                newMate.save()
            else:
                leaseid = -1 * randint(1, BIG_ENOUGH)
                lease = Lease(leaseID = leaseid, address = address)
                lease.save()
                newMates = Flatmates(lease = ease, user = add)
                newMates.save()

        return Response({"good": lease.leaseID})


#class APIResolveAddress(APIView):
#    """
#    uname   - email of user
#    address - address of their house/flat
#    """

#    def post(self, request):
#        try:
#            uname   = request.POST.get("uname")
#            addr    = request.POST.get("address").lower().replace("  ", " ")
#            user    = User.objects.filter(email = uname).all()[0]
#        except:
#            return BAD_FIELDS

#        lease = Lease.objects.filter(address = addr)
#        if (lease.exists()):
#            new_mate = Flatmates(user = user, lease = lease.all()[0])
#            new_lease_id = new_mate.lease.leaseID
#        else:
#            new_lease_id = -1 * randint(1, LARGE_ENOUGH)
#            new_lease = Lease(address = addr, leaseID = new_lease_id)
#            new_lease.save() # just pray for no collisions
#            new_mates = Flatmates(lease = new_lease, user = user)
#            new_mates.save()

#        return Response({"good": new_lease_id})

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

        lease = Flatmates.objects.filter(user = user)[0].lease
        mates = Flatmates.objects.filter(lease = lease)
        fmusers = [f.user for f in mates]
        tallies = [ChoreTallies.objects.filter(user = m)[0] for m in fmusers]
        names = [u.fnames.split()[0] for u in fmusers]
        completed = [[t.completed] for t in tallies]
        skipped = [[t.skipped] for t in tallies]

        self._draw_ratios(names, lease.leaseID, completed, skipped)


        return GOOD

    def _draw_ratios(self, names, leaseid, completed, skipped):
        cmapg=LinearSegmentedColormap.from_list('rg',["r", "y", "g"], N=256)
        cmapb=LinearSegmentedColormap.from_list('rg',["g", "y", "r"], N=256)
        size = len(names)

        fig, axs = plt.subplots(1,2)
        a1 = axs[0].imshow(completed, cmap=cmapg,
                    vmin=0, vmax=size, aspect='auto',
                    interpolation='nearest')
        a2 = axs[1].imshow(skipped, cmap=cmapb,
                    vmin=0, vmax=size, aspect='auto',
                    interpolation='nearest')

        for i in range(size):
            axs[0].annotate(str(completed[i])[1:-1], xy=(0, i), ha='center', va='center', color='black')
            axs[1].annotate(str(skipped[i])[1:-1], xy=(0, i), ha='center', va='center', color='black')

        for ax,l in zip(axs,['Completed','Skipped',]):
            ax.set_xticks([])
            ax.set_xlabel(l)
        axs[0].set_yticks(list(range(size)))
        axs[0].tick_params(length = 0)
        axs[0].set_yticklabels(names[:size])
        axs[1].set_yticks([])

        plt.savefig(f"media/{leaseid}.png", transparent = True)

class APIGetChoreDetails(APIView):
    """
    choreid - ID for the chore to get details of
    """
    def get(self, request):
        try:
            choreid = int(request.GET.get("choreid"))
            chore   = Chores.objects.filter(id = choreid)[0]
        except:
            return BAD_FIELDS

        return Response({"id": choreid, "type": chore.choreType.id, "weight": chore.weight, "responsible": chore.responsible.email})

class APIGetChoreHistory(APIView):
    """
    No params, just returns a csv file. Might get a bit huge.
    completion  assignee    completer   name    weight
    """

    def get(self, request):
        existing = []
        if path.exists(HISTORY_PATH):
            f = open(HISTORY_PATH, "r")
            existing = list(reader(f))[1:]
            f.close()
        past = PastChores.objects.all()
        agg = [(t, t.chore) for t in past]
        fmted = [[d2s(p.doneDate), u2n(p.responsible), u2n(p.completer),  ct2n(c.choreType.id), c.weight] for p, c in agg]
        tot = existing + fmted
        tot.sort(key = lambda r: r[0])

        f = open(HISTORY_PATH, "w")
        w = writer(f)
        w.writerow(HISTORY_HEADER)
        for r in tot:
            w.writerow(r)
        f.close()

        for p in PastChores.objects.all():
            c = p.chore
            c.delete()
            p.delete()

        f = open(HISTORY_PATH, "rb")
        return FileResponse(f, filename = "history.csv", as_attachment = True)

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
        fmates = list(Flatmates.objects.filter(lease = lease)) # wtf?
        mates = [f.user.email for f in fmates if f.user != user]

        return Response({"emails": mates})

class APIChangeLease(APIView):
    """
    uname   - email of user to change lease ID
    leaseid - new lease ID
    address - address of new tenancy
    """
    def post(self, request):
        try:
            leaseid = int(request.POST.get("leaseid"))
            uname   = request.POST.get("uname")
            user    = User.objects.filter(email = uname)[0]
            address = request.POST.get("address")[0].replace("  ", " ")
        except:
            return BAD_FIELDS

        fmates      = Flatmates.objects.filter(user = user)[0]
        oldLease    = fmates.lease
        if oldLease.leaseID == leaseid:
            return Response({"error": "same_lease_id"})

        newLease = Lease.objects.filter(leaseID = leaseid)
        if newLease.exists():
            fmates.lease = newLease[0]
            fmates.save()
            return Response({"good": newLease[0].leaseID})
        else:
            leaseCand = Lease.objects.filter(address = address)
            if leaseCand.exists():
                fmates.lease = leaseCand[0]
                fmates.save()
                return Response({"good": leaseCand[0].leaseID})
            else:
                new_lease_id = -1 * randint(1, LARGE_ENOUGH)
                newLease = Lease(address = address, leaseID = new_lease_id)
                newLease.save() # just pray for no collisions
                fmates.lease = newLease
                fmates.save()
                return Response({"good": new_lease_id})
        return Response({"error": "unknown_err"})

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

        try:
            f = open(f"media/{leaseid}.png", "rb")
            return FileResponse(f, filename = "tallies.png", as_attachment = True)
        except:
            return Response({"error": "tallies_not_generated_yet_do_a_chore_first"})


class APIGetSocialCredits(APIView):
    """
    uname   - email of user to get the social credit score of
    """
    def get(self, request):
        try:
            uname = request.GET.get("uname")
            user = User.objects.filter(email = uname)[0]
        except:
            return BAD_FIELDS

        score = SocialCredits.objects.filter(user = user)[0].score
        return Response({uname: score})
