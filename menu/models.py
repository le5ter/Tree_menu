from django.db import models
from django.urls import reverse


class MenuItem(models.Model):
    text = models.CharField(max_length=100)
    menu_name = models.CharField(max_length=50)
    url = models.CharField(max_length=200, blank=True, null=True)
    named_url = models.CharField(max_length=100, blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def get_url(self):
        if self.url:
            return self.url
        elif self.named_url:
            return reverse(self.named_url)
        else:
            return '#'

    def __str__(self):
        return self.text
