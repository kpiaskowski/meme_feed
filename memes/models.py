from django.db import models


class Meme(models.Model):
    post_id = models.CharField(max_length=400, primary_key=True)
    post_url = models.URLField(max_length=600)
    image_url = models.URLField(max_length=600)
    views = models.IntegerField(default=0)
    valid = models.BooleanField(default=True)
    pub_date = models.DateTimeField(auto_now=True)
