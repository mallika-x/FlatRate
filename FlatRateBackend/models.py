from django.db import models

from .constants import *

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

class Lease(models.Model):
    leaseID = models.IntegerField(primary_key = True) # TODO format?
    address = models.CharField(max_length = DB_MAXLEN)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields = ["address"], name = "unique_addresses")]

class Flatmates(models.Model):
    lease   = models.ForeignKey(Lease, on_delete = models.CASCADE,  related_name = "flatmates_lease")
    user    = models.ForeignKey(User, on_delete = models.PROTECT,   related_name = "flatmates_user")

    class Meta:
        unique_together = ("lease", "user")

class ChoreTypes(models.Model):
    name    = models.CharField(max_length = DB_MAXLEN)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields = ["name"], name = "unique_chore_types")
        ]

class Chores(models.Model):
    choreType   = models.ForeignKey(ChoreTypes, on_delete = models.PROTECT,         related_name = "chore_types_enumed")
    weight      = models.IntegerField(choices = CHORE_PRIORITIES)
    responsible = models.ForeignKey(User, null = True, on_delete = models.PROTECT,  related_name = "chore_users_responsible")

class ActiveChores(models.Model):
    chore   = models.ForeignKey(Chores, on_delete = models.CASCADE, related_name = "chores_active")
    expiry  = models.DateTimeField(null = True)

class PastChores(models.Model):
    chore       = models.ForeignKey(Chores, on_delete = models.CASCADE,             related_name = "chores_past")
    responsible = models.ForeignKey(User, null = True, on_delete = models.PROTECT,  related_name = "chores_past_responsibility")
    completer   = models.ForeignKey(User, on_delete = models.PROTECT,               related_name = "chores_past_completer")
    doneDate    = models.DateField(auto_now_add = True)

class Schedule(models.Model):
    flatmates   = models.ForeignKey(Flatmates, on_delete = models.CASCADE, related_name = "flatmats_schedule")
    initDate    = models.DateField(auto_now_add = True)
    duration    = models.IntegerField()

class ScheduleSet(models.Model):
    schedule    = models.ForeignKey(Schedule, on_delete = models.CASCADE,   related_name = "schedule_to_scheduleset")
    chore       = models.ForeignKey(Chores, on_delete = models.CASCADE,     related_name = "chore_to_scheduleset")

class NotifType(models.Model):
    text    = models.CharField(max_length = DB_MAXLEN, choices = NOTIF_BODIES)

class Notifications(models.Model):
    user        = models.ForeignKey(User, on_delete = models.PROTECT,                   related_name = "user_notifications")
    notifType   = models.ForeignKey(NotifType, on_delete = models.CASCADE,              related_name = "notification_type")
    chore       = models.ForeignKey(Chores, null = True, on_delete = models.CASCADE,    related_name = "chore_notifications")
