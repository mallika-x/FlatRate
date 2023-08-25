from django.db import models

# General constants
DB_MAXLEN   = 255

# User constants
#https://www.rfc-editor.org/errata/eid1690 -- 320 but mariadb mandates <=255
EMAILMAXLEN     = 255
#https://www.bdm.vic.gov.au/births/naming-your-child/naming-restrictions#toolong
FNAMESMAXLEN    = 38
SNAMEMAXLEN     = 38

# Social Credits Constants
DEFAULT_SOCIAL_CREDITS = 200

# Chore Constants
NO_PRIORITY         = 0
LOW_PRIORITY        = 5
MEDIUM_PRIORITY     = 10
HIGH_PRIORITY       = 20
CHORE_PRIORITIES    = [(NO_PRIORITY,        "No Priority"),
                       (LOW_PRIORITY,       "Low Priority"),
                       (MEDIUM_PRIORITY,    "Medium Priority"),
                       (HIGH_PRIORITY,      "High Priority")]

class User(models.Model):
    """
    I like this better than the default.
    This is proof of concept so we don't need auth etc.
    All foreign keys to this table should be PROTECT because once you're
    in the social credits matrix you should never be able to escape.
    """
    email   = models.EmailField(max_length = EMAILMAXLEN, primary_key = True)
    fnames  = models.CharField(max_length = FNAMESMAXLEN)
    snames  = models.CharField(max_length = SNAMEMAXLEN)
    pii     = models.FileField() # see if this works without upload_to param
    photo   = models.ImageField()   # this too

class SocialCredits(models.Model):
    user    = models.ForeignKey(User, on_delete = models.PROTECT, related_name = "user_social_credits")
    score   = models.IntegerField()

# Should look into scrapping this and using actual notifs.
# Does expo even allow this? TODO find out
class Notifications(models.Model):
    user    = models.ForeignKey(User, on_delete = models.PROTECT, related_name = "user_notifications")
    # Icon? Enumerated type? Consult with MM TODO
    body    = models.CharField(max_length = DB_MAXLEN)

class Lease(models.Model):
    leaseID = models.IntegerField(primary_key = True) # TODO format?
    address = models.CharField(max_length = DB_MAXLEN)

class Flatmates(models.Model):
    lease   = models.ForeignKey(Lease, on_delete = models.CASCADE, related_name = "flatmates_lease")
    user    = models.ForeignKey(User, on_delete = models.PROTECT, related_name = "flatmates_user")

    class Meta:
        unique_together = ("lease", "user")

class ChoreTypes(models.Model):
    name    = models.CharField(max_length = DB_MAXLEN)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields = ["name"], name = "unique_chore_types")
        ]

class Chores(models.Model):
    choreType   = models.ForeignKey(ChoreTypes, on_delete = models.PROTECT, related_name = "chore_types_enumed")
    weight      = models.IntegerField(choices = CHORE_PRIORITIES)
    responsible = models.ForeignKey(User, null = True, on_delete = models.PROTECT, related_name = "chore_users_responsible")

