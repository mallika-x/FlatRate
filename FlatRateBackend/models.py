from django.db import models

GMAILMAXLEN = 320

class User(models.Model):
    """I like this better than the default"""
    email   = models.EmailField(max_length = GMAILMAXLEN, primary_key = True)
    fnames  = models.CharField(max_length = FNAMES_MAXLEN)
    snames  = models.CharField(max_length = SNAMES_MAXLEN)
    pii     = models.FileField() # see if this works without upload_to param
    photo   = models.ImageField()   # this too
