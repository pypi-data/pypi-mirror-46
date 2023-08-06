from django.conf import settings
from django.db import models

from djangoldp.models import Model
from djangoldp_skill.models import Skill


class JobOffer(Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    skills = models.ManyToManyField(Skill, blank=True)
    creationDate = models.DateField(auto_now_add=True)
    closingDate = models.DateField(blank=True, null=True)

    class Meta:
        auto_author = 'author'
        nested_fields = ["skills"]
        container_path = 'job-offers/'
        rdf_type = 'hd:joboffer'
        depth = 0

    def __str__(self):
        return '{} ({})'.format(self.title, self.author.get_full_name())
