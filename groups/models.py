from django.db import models
from django.urls import reverse
# hepls to remove extra characters like alphanumeric or underscore or hyphens
# the use of this is if you have string and want to use as URL then it`s going to remove spaces and add dashes ...
from django.utils.text import slugify
# install misaka in terminal
# import misaka

from django.contrib.auth import get_user_model
User = get_user_model()

# this is how we can use custom template tag
# this helps us so, we can use related_name to grab that model with get_related_name
from django import template
register = template.Library()


# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=255,unique=True)
    slug = models.SlugField(allow_unicode=True,unique=True)
    description = models.TextField(blank=True,default='')
    description_html = models.TextField(editable=False,default='',blank=True)
    members = models.ManyToManyField(User,through='GroupMember')

    def __str__(self):
        return self.name

    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        # self.description_html = misaka.html(self.description)
        self.description_html = self.description
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('groups:single',kwargs={'slug':self.slug})

    class Meta:
        ordering = ['name']


class GroupMember(models.Model):
        group = models.ForeignKey(Group, related_name='memberships',on_delete=None)
        user = models.ForeignKey(User,related_name='user_groups',on_delete=None)

        def __str__(self):
            return self.user.username

        class Meta:
            unique_together = ('group','user')
