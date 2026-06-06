from django.db import models
import random
import secrets

class URLMapping(models.Model):
    original_url = models.URLField()
    short_url = models.CharField(max_length=10,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    click_count = models.PositiveIntegerField(default=0)
    expired_at = models.DateTimeField(null=True,blank=True)


    def __str__(self):
        return self.original_url
    

    def save(self,*args,**kwargs):
        if not self.short_url:
            self.short_url = self.generate_short_url()
        super().save(*args,**kwargs)

    def generate_short_url(self):
        base62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

        while True:
            code = "".join(
                secrets.choice(base62)
                for _ in range(6)
            )
            if not URLMapping.objects.filter(
                short_url=code
            ).exists():
                return code