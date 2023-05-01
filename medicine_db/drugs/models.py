from django.db import models
from django.contrib import admin


class XMLSiteMap(models.Model):
    name = models.CharField(max_length=120, blank=True)
    url = models.URLField(unique=True)
    excluded = models.BooleanField(default=False)
    # parent = models.ForeignKey('Provider', null=True, on_delete=models.SET_NULL)
    parent = models.ForeignKey('Provider', null=True, on_delete=models.CASCADE, related_name='sitemap')
    sitemap_parser_code = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.url

    @admin.display(boolean=True, description="Included in parsing?")
    def included(self):
        return not self.excluded

    @admin.display(boolean=True, description="Has parser code?")
    def has_parser_code(self):
        if self.sitemap_parser_code:
            return True
        return False


class Provider(models.Model):
    name = models.CharField(max_length=120, blank=True)
    url = models.URLField(unique=True)
    # robots = models.URLField(unique=True)
    excluded = models.BooleanField(default=False)
    # sitemap = models.ForeignKey(XMLSiteMap, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        if self.name:
            return self.name
        return self.url
    
    @admin.display(boolean=True, ordering="sitemap", description="Has parsable sitemaps?")
    def has_sitemaps(self):
        if self.sitemap.all():
            return True
        return False


class ProviderCategory(models.Model):
    name = models.CharField(max_length=120, blank=True)
    slug = models.SlugField(blank=True)
    url = models.URLField(null=True)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='categories', null=True)

class Drug(models.Model):
    class StatusCodes(models.TextChoices):
        AWAITING = 'awaiting', 'Ожидает классификации'
        IN_REVIEW = 'in_review', 'На рассмотрении'
        EXCLUDED = 'excluded', 'Исключен'
        READY = 'classified', 'Классифицирован'

    name = models.CharField(max_length=120, blank=True)
    slug = models.SlugField(blank=True)
    url = models.URLField(null=True)
    categories = models.ManyToManyField(ProviderCategory, related_name='drugs')
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='drugs', null=True)
    status = models.CharField(max_length=20, choices=StatusCodes.choices, default=StatusCodes.AWAITING)

    # Описание
    description = models.TextField(blank=True, null=True)
    # Противопоказания
    warning = models.TextField(blank=True, null=True)
    tags = models.TextField(blank=True, null=True)
    cats = models.TextField(blank=True, null=True)
    # categories 

    def __str__(self):
        if self.name:
            return self.name
        if self.slug:
            return self.slug
        return self.url