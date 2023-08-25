from django.db import models

# User constants
#https://www.rfc-editor.org/errata/eid1690 -- 320 but mariadb mandates <=255
EMAILMAXLEN     = 255
#https://www.bdm.vic.gov.au/births/naming-your-child/naming-restrictions#toolong
FNAMESMAXLEN    = 38
SNAMEMAXLEN     = 38

# Social Credits Constants
DEFAULT_SOCIAL_CREDITS = 200

class User(models.Model):
    """I like this better than the default"""
    email   = models.EmailField(max_length = EMAILMAXLEN, primary_key = True)
    fnames  = models.CharField(max_length = FNAMESMAXLEN)
    snames  = models.CharField(max_length = SNAMEMAXLEN)
    pii     = models.FileField() # see if this works without upload_to param
    photo   = models.ImageField()   # this too

class SocialCredits(models.Model):
    user    = models.ForeignKey(User, on_delete = models.PROTECT, related_name = "social_credits_score")
    score   = models.IntegerField()
